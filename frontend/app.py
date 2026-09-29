import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/perguntar"

st.set_page_config(page_title="Spotify FAQ Chatbot", page_icon="🎧", layout="centered")

# CSS extra para detalhes que o tema padrão não cobre
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 12px;
    }
    div[data-testid="stChatMessageContent"] {
        border-radius: 12px;
    }
    .stButton>button {
        background-color: #1DB954;
        color: black;
        border-radius: 20px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1ed760;
        color: black;
    }
    h1 {
        color: #1DB954;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎧 Spotify FAQ Chatbot")
st.caption("Tire suas dúvidas sobre os recursos do app, direto do suporte oficial")

# Inicializa o histórico de conversa (só existe durante a sessão)
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Exibe o histórico já existente
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["conteudo"])

# Campo de entrada do usuário
pergunta = st.chat_input("Digite sua pergunta sobre o Spotify...")

if pergunta:
    # Adiciona e exibe a pergunta do usuário no histórico
    st.session_state.mensagens.append({"role": "user", "conteudo": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Chama a API e exibe a resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = requests.post(API_URL, json={"pergunta": pergunta}, timeout=900)
                response.raise_for_status()
                dados = response.json()

                resposta_texto = dados["resposta"]
                fontes = dados["fontes"]

                st.markdown(resposta_texto)

                if fontes:
                    st.markdown("**Fontes:**")
                    for fonte in fontes:
                        st.markdown(f"- {fonte}")

                conteudo_completo = resposta_texto
                if fontes:
                    conteudo_completo += "\n\n**Fontes:**\n" + "\n".join(f"- {f}" for f in fontes)

            except requests.exceptions.ConnectionError:
                conteudo_completo = " Não consegui conectar à API. Verifique se o servidor FastAPI está rodando."
                st.error(conteudo_completo)
            except requests.exceptions.Timeout:
                conteudo_completo = " A resposta demorou demais. Tente novamente."
                st.error(conteudo_completo)
            except Exception as e:
                conteudo_completo = f" Ocorreu um erro inesperado: {e}"
                st.error(conteudo_completo)


    # Salva a resposta no histórico
    st.session_state.mensagens.append({"role": "assistant", "conteudo": conteudo_completo})