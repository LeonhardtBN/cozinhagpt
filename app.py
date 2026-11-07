import os
import uuid

import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
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
    llm = ChatGoogleGenerativeAI(model=MODELO, temperature=0.7)
    return prompt | llm


# Gerenciamento de Histórico do LangChain, guardado na sessão do Streamlit
if "store" not in st.session_state:
    st.session_state.store = {}
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # uma conversa por aba do navegador


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]


chain_with_history = RunnableWithMessageHistory(
    get_chain(),
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


def texto_do_pedaco(pedaco) -> str:
    """Extrai o texto de um pedaço da resposta (o Gemini pode devolver o conteúdo em partes)."""
    conteudo = pedaco.content
    if isinstance(conteudo, str):
        return conteudo
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in conteudo)


# 4. Interface de Chat
with st.sidebar:
    if st.button("Nova conversa", width="stretch"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []

if not st.session_state.get("messages"):
    st.session_state.messages = [{"role": "assistant", "content": SAUDACAO}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Digite os ingredientes (ex: ovo, tomate, queijo)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # A resposta aparece aos poucos (streaming), em vez de esperar a receita inteira
    with st.chat_message("assistant"):
        resposta = st.write_stream(
            texto_do_pedaco(p) for p in chain_with_history.stream(
                {"input": prompt},
                config={"configurable": {"session_id": st.session_state.session_id}},
            )
        )

    st.session_state.messages.append({"role": "assistant", "content": resposta})
