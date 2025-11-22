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
   git clone [https://github.com/LeonhardtBN/cozinhagpt.git](https://github.com/LeonhardtBN/cozinhagpt.git)
   cd cozinhagpt
Crie um ambiente virtual (opcional, mas recomendado):

Bash

python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
Instale as dependências:

Bash

pip install -r requirements.txt
Configure as variáveis de ambiente: Crie um arquivo .env na raiz do projeto e adicione sua chave:

OPENAI_API_KEY=sk-sua-chave-aqui
Execute a aplicação:

Bash

streamlit run app.py
📂 Estrutura do Projeto
cozinha-gpt/
├── app.py           # Código principal da aplicação Streamlit
├── .env             # Arquivo de variáveis de ambiente (não comitar)
├── requirements.txt # Lista de dependências do projeto
└── README.md        # Documentação
🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias nas instruções de prompt ou na interface.

📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.


---

### Dica Adicional: O arquivo `requirements.txt`

Para que o passo 3 da instalação funcione, você deve criar um arquivo chamado `requirements.txt` junto com seu código e colocar o seguinte conteúdo nele:

```text
streamlit
langchain-openai
langchain-core
langchain-community
python-dotenv
openai
