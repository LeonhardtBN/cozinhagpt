# 🍳 CozinhaGPT

**CozinhaGPT** é um assistente virtual de culinária desenvolvido em Python. Ele utiliza Inteligência Artificial para sugerir receitas criativas, práticas e personalizadas com base apenas nos ingredientes que o usuário possui em casa.

A aplicação possui uma interface gráfica amigável construída com **Streamlit** e utiliza **LangChain** para gerenciar a memória da conversa e a interação com o modelo GPT da OpenAI.

## ✨ Funcionalidades

- **Geração de Receitas por Ingredientes:** Informe o que tem na geladeira e receba sugestões viáveis.
- **Memória de Conversa:** O assistente lembra do contexto (ex: se você disse que não gosta de cebola no início, ele lembrará nas próximas sugestões).
- **Adaptação a Restrições:** Sugere substituições para dietas veganas, sem glúten ou lactose.
- **Interface Moderna:** Chat interativo estilo WhatsApp/ChatGPT rodando diretamente no navegador via Streamlit.

## 🛠️ Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Streamlit](https://streamlit.io/) (Interface Frontend)
- [LangChain](https://www.langchain.com/) (Orquestração de LLMs)
- [OpenAI API](https://openai.com/) (Modelo `gpt-4o-mini`)

## 🚀 Como rodar o projeto

### Pré-requisitos

Você precisará de uma chave de API da OpenAI.

### Instalação

1. Clone este repositório:
   ```bash
   git clone [https://github.com/seu-usuario/cozinha-gpt.git](https://github.com/seu-usuario/cozinha-gpt.git)
   cd cozinha-gpt
