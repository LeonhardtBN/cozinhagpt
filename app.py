import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

MODELO = os.getenv("MODELO", "gemini-3.8-flash")
MENSAGENS_DE_CONTEXTO = 20  # limita o histórico enviado ao modelo (custo e velocidade)
SAUDACAO = "Olá! Que ingredientes você tem na geladeira hoje?"

# 1. Configuração da Página
st.set_page_config(page_title="CozinhaGPT", page_icon="🍳")
st.title("🍳 CozinhaGPT")
st.caption("Sua assistente de cozinha prática e criativa.")

# 2. Carregar Variáveis de Ambiente
load_dotenv()

if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
    st.error("A chave GEMINI_API_KEY não foi encontrada. Verifique seu arquivo .env "
             "(chave gratuita em https://aistudio.google.com/apikey).")
    st.stop()


# 3. Configuração da LLM e Chain (@st.cache_resource para não recriar a cada interação)
@st.cache_resource
def get_chain():
    instrucoes = """Você é CozinhaGPT, uma assistente de cozinha prática, criativa e gentil.
    Seu objetivo é transformar a lista de ingredientes que o usuário informar em receitas viáveis —
    com instruções claras, tempo estimado, nível de dificuldade e sugestões de substituições. Seja direto, objetivo e útil.
    Priorize receitas que usam o máximo possível dos ingredientes fornecidos,
    evite propor ingredientes difíceis de encontrar sem avisar,
    e sempre ofereça opções para diferentes restrições alimentares (vegetariano/vegano/sem glúten/lactose) quando possível.
    Lembre das preferências e restrições que o usuário já contou na conversa.
    Ao final de cada receita, liste os ingredientes que faltam para o usuário comprar, se houver."""

    # O histórico entra só pelo MessagesPlaceholder (antes ele também ia no texto do sistema, duplicado).
    prompt = ChatPromptTemplate.from_messages([
        ("system", instrucoes),
        MessagesPlaceholder(variable_name="history", n_messages=MENSAGENS_DE_CONTEXTO),
        ("human", "{input}"),
    ])
    # Raciocínio "low" deixa a resposta bem mais rápida; poucas tentativas evitam esperas silenciosas no limite gratuito
    llm = ChatGoogleGenerativeAI(model=MODELO, temperature=0.7, thinking_config={"thinking_level": "low"},
                                 max_retries=2, timeout=90)
    return prompt | llm


def mensagem_de_erro(erro: Exception) -> str:
    texto = str(erro)
    if "429" in texto or "RESOURCE_EXHAUSTED" in texto:
        return "O limite gratuito do Gemini foi atingido. Espere um minuto e tente de novo."
    return f"Não consegui gerar a resposta ({type(erro).__name__}). Confira a GEMINI_API_KEY no .env."


def com_aviso_de_espera(pedacos):
    """Mostra "pensando..." até o primeiro pedaço chegar; depois a resposta aparece aos poucos."""
    with st.spinner("Pensando na receita..."):
        primeiro = next(pedacos, None)
    if primeiro is not None:
        yield primeiro
    yield from pedacos


def texto_do_pedaco(pedaco) -> str:
    """Extrai o texto de um pedaço da resposta (o Gemini pode devolver o conteúdo em partes)."""
    conteudo = pedaco.content
    if isinstance(conteudo, str):
        return conteudo
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in conteudo)


# 4. Interface de Chat
with st.sidebar:
    if st.button("Nova conversa", width="stretch"):
        st.session_state.messages = []

if not st.session_state.get("messages"):
    st.session_state.messages = [{"role": "assistant", "content": SAUDACAO}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Digite os ingredientes (ex: ovo, tomate, queijo)..."):
    # Memória da conversa: as mensagens anteriores desta aba, guardadas na sessão do Streamlit
    historico = [("human" if m["role"] == "user" else "ai", m["content"]) for m in st.session_state.messages]
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # A resposta aparece aos poucos (streaming), em vez de esperar a receita inteira
    with st.chat_message("assistant"):
        try:
            resposta = st.write_stream(com_aviso_de_espera(
                texto_do_pedaco(p) for p in get_chain().stream({"history": historico, "input": prompt})
            ))
        except Exception as erro:  # erro da API: mostra o motivo em vez de travar com a bolha vazia
            st.session_state.messages.pop()
            st.error(mensagem_de_erro(erro))
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": resposta})
