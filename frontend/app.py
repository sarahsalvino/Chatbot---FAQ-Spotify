import streamlit as st
import requests
import datetime

import os
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000/perguntar")

st.set_page_config(page_title="SpotBot", page_icon="🎧", layout="centered")

# Saudação dinâmica baseada no horário
hora_atual = datetime.datetime.now().hour
if hora_atual < 12:
    saudacao = "Bom dia"
elif hora_atual < 18:
    saudacao = "Boa tarde"
else:
    saudacao = "Boa noite"

#CSS customizado
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 12px;
    }
    div[data-testid="stChatMessageContent"] {
        border-radius: 12px;
    }
    div[data-testid="stChatMessageContent"] p,
    div[data-testid="stChatMessageContent"] li {
        font-size: 18px !important;
        line-height: 1.6;
    }
    [data-testid="stChatMessageAvatarAssistant"],
    [data-testid="stChatMessageAvatarAssistant"] > div,
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #1DB954 !important;
        border-radius: 8px !important;
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        margin-bottom: 8px;
    }
    .logo-circle {
        background-color: #1DB954;
        border-radius: 50%;
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
    }
    .brand-name {
        font-size: 42px;
        font-weight: 800;
        color: white;
    }
    .hero {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 24px;
        margin-top: 20px;
        margin-bottom: 40px;
    }
    .waveform {
        display: flex;
        align-items: center;
        gap: 4px;
        opacity: 0.55;
    }
    .waveform span {
        width: 4px;
        background-color: #1DB954;
        border-radius: 2px;
        display: inline-block;
    }
    .waveform span:nth-child(1) { height: 10px; }
    .waveform span:nth-child(2) { height: 22px; }
    .waveform span:nth-child(3) { height: 34px; }
    .waveform span:nth-child(4) { height: 18px; }
    .waveform span:nth-child(5) { height: 28px; }
    .waveform span:nth-child(6) { height: 14px; }
    .hero-text {
        text-align: center;
    }
    .saudacao {
        font-size: 75px;
        font-weight: 800;
        color: white;
        line-height: 1;
        margin-bottom: 8px;
    }
    .subtitulo {
        font-size: 20px;
        color: #B3B3B3;
        margin-top: 4px;
    }
    div[data-testid="stChatInput"] {
        border-radius: 30px !important;
        padding: 6px 10px !important;
    }
    div[data-testid="stChatInput"] textarea {
        font-size: 18px !important;
        min-height: 50px !important;
    }
</style>
""", unsafe_allow_html=True)

#Cabeçalho com ícone + nome
st.markdown("""
<div class="header-container">
    <div class="logo-circle">🎧</div>
    <div class="brand-name">SpotBot</div>
</div>
""", unsafe_allow_html=True)

#Saudação com "equalizadores" decorativos dos dois lados
st.markdown(f"""
<div class="hero">
    <div class="waveform">
        <span></span><span></span><span></span><span></span><span></span><span></span>
    </div>
    <div class="hero-text">
        <div class="saudacao">{saudacao}!</div>
        <div class="subtitulo">Em que posso te ajudar hoje? :)</div>
    </div>
    <div class="waveform">
        <span></span><span></span><span></span><span></span><span></span><span></span>
    </div>
</div>
""", unsafe_allow_html=True)

#Inicializa o histórico de conversa (só existe durante a sessão)
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

#Exibe o histórico já existente
for msg in st.session_state.mensagens:
    avatar = "🎧" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["conteudo"])

#Campo de entrada do usuário
pergunta = st.chat_input("Digite sua pergunta sobre o Spotify...")

if pergunta:
    st.session_state.mensagens.append({"role": "user", "conteudo": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant", avatar="🎧"):
        with st.spinner("Verificando para te trazer a melhor resposta..."):
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

    st.session_state.mensagens.append({"role": "assistant", "conteudo": conteudo_completo})