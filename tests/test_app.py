"""Testa o app com um modelo falso no lugar do Gemini (roda sem chave de API)."""

from pathlib import Path

import langchain_google_genai
import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


class ModeloFalso(FakeListChatModel):
    """Guarda as mensagens que recebeu, para conferirmos o histórico enviado ao modelo."""

    recebidas: list = []

    def _call(self, messages, *args, **kwargs):
        ModeloFalso.recebidas.append(messages)
        return super()._call(messages, *args, **kwargs)

    def _stream(self, messages, *args, **kwargs):
        ModeloFalso.recebidas.append(messages)
        yield from super()._stream(messages, *args, **kwargs)


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "teste")
    ModeloFalso.recebidas = []
    monkeypatch.setattr(langchain_google_genai, "ChatGoogleGenerativeAI",
                        lambda **kw: ModeloFalso(responses=["Receita 1: omelete", "Receita 2: sem cebola"]))
    at = AppTest.from_file(APP, default_timeout=30)
    at.session_state  # noqa: B018
    return at


def test_saudacao_e_titulo(app):
    app.run()
    assert not app.exception
    assert app.title[0].value == "🍳 CozinhaGPT"
    assert app.chat_message[0].markdown[0].value.startswith("Olá!")


def test_conversa_com_memoria_sem_duplicar_historico(app):
    app.run()
    app.chat_input[0].set_value("ovo e tomate, não gosto de cebola").run()
    app.chat_input[0].set_value("outra receita").run()
    assert not app.exception
    textos = [m.markdown[0].value for m in app.chat_message]
    assert textos[-1] == "Receita 2: sem cebola"

    segunda_chamada = ModeloFalso.recebidas[-1]
    conteudos = [m.content for m in segunda_chamada]
    assert sum("não gosto de cebola" in c for c in conteudos) == 1  # histórico aparece uma vez só
    assert "{history}" not in conteudos[0]


def test_nova_conversa_limpa_o_chat(app):
    app.run()
    app.chat_input[0].set_value("arroz").run()
    app.sidebar.button[0].click().run()
    assert [m.markdown[0].value for m in app.chat_message] == [app.chat_message[0].markdown[0].value]
    assert len(app.chat_message) == 1
