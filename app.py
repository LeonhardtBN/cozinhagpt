import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# 1. Configuração da Página
st.set_page_config(page_title="CozinhaGPT", page_icon="🍳")
st.title("🍳 CozinheiroGPT")
st.caption("Sua assistente de cozinha prática e criativa.")

# 2. Carregar Variáveis de Ambiente
load_dotenv()

# Verificação básica da API Key para evitar erros
if not os.getenv("OPENAI_API_KEY"):
    st.error("A chave OPENAI_API_KEY não foi encontrada. Verifique seu arquivo .env")
    st.stop()

# 3. Configuração da LLM e Chain (Usamos @st.cache_resource para não recriar a cada interação)
@st.cache_resource
def get_chain():
    template = """Você é CozinhaGPT, uma assistente de cozinha prática, criativa e gentil. 
    Seu objetivo é transformar a lista de ingredientes que o usuário informar em receitas viáveis — 
    com instruções claras, tempo estimado, nível de dificuldade e sugestões de substituições. Seja direto, objetivo e útil. 
    Priorize receitas que usam o máximo possível dos ingredientes fornecidos, 
    evite propor ingredientes difíceis de encontrar sem avisar, 
    e sempre ofereça opções para diferentes restrições alimentares (vegetariano/vegano/sem glúten/lactose) quando possível.

    Historico de conversa:
    {history}

    Entrada do Usuario:
    {input}"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    llm = ChatOpenAI(temperature=0.7, model='gpt-4o-mini')
    chain = prompt | llm
    return chain

# Gerenciamento de Histórico do LangChain
# Usamos st.session_state para garantir que o histórico persista na sessão do Streamlit
if "store" not in st.session_state:
    st.session_state.store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

chain = get_chain()
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# 4. Interface de Chat
# Inicializa o histórico visual do chat (diferente da memória do LangChain)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Olá! Que ingredientes você tem na geladeira hoje?"}]

# Exibe as mensagens anteriores na tela
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Captura a entrada do usuário
if prompt := st.chat_input("Digite os ingredientes (ex: ovo, tomate, queijo)..."):
    
    # Exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Gera a resposta
    with st.chat_message("assistant"):
        with st.spinner("O CozinhaGPT está pensando em uma receita..."):
            response = chain_with_history.invoke(
                {'input': prompt},
                config={'configurable': {'session_id': 'sessao_streamlit_usuario'}}
            )
            st.write(response.content)
    
    # Salva a resposta no histórico visual
    st.session_state.messages.append({"role": "assistant", "content": response.content})