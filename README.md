# 🍳 CozinhaGPT

**CozinhaGPT** é um assistente virtual de culinária desenvolvido em Python. Ele utiliza Inteligência Artificial para sugerir receitas criativas, práticas e personalizadas com base apenas nos ingredientes que o usuário possui em casa.

A aplicação possui uma interface gráfica amigável construída com **Streamlit** e utiliza **LangChain** para gerenciar a memória da conversa e a interação com o modelo GPT da OpenAI.

---

## ✨ Funcionalidades

- **Geração de receitas por ingredientes:** informe o que tem na geladeira e receba sugestões viáveis.
- **Memória de conversa:** o assistente lembra do contexto (ex: se você disse que não gosta de cebola no início, ele evitará nas próximas sugestões).
- **Adaptação a restrições alimentares:** sugestões para dietas veganas, sem glúten ou lactose.
- **Interface moderna:** chat estilo WhatsApp/ChatGPT rodando diretamente no navegador via Streamlit.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI API](https://openai.com/) – modelo `gpt-4o-mini`

---

## 🚀 Como Rodar o Projeto

### ⚙️ Pré-requisitos  
Você precisará de uma chave de API da OpenAI.

### 📦 Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/LeonhardtBN/cozinhagpt.git
   cd cozinhagpt
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv

   # No Windows:
   venv\Scripts\activate

   # No Linux/Mac:
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto:

   ```bash
   OPENAI_API_KEY=sk-sua-chave-aqui
   ```

5. Execute a aplicação:

   ```bash
   streamlit run app.py
   ```

---

## 📂 Estrutura do Projeto

```text
cozinhagpt/
├── app.py           # Código principal da aplicação Streamlit
├── .env             # Variáveis de ambiente (não comitar)
├── requirements.txt # Dependências do projeto
└── README.md        # Documentação
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir **issues** ou enviar **pull requests** com melhorias na interface ou instruções de prompt.

---

## 📝 Licença

Este projeto está sob a licença **MIT**. Consulte o arquivo `LICENSE` para mais detalhes.

---

### 📌 Dica: conteúdo recomendado para o `requirements.txt`

```text
streamlit
langchain-openai
langchain-core
langchain-community
python-dotenv
openai
```
