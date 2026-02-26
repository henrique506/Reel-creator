import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import time

# Configuração da Página
st.set_page_config(page_title="Script Master Pro", layout="wide", page_icon="🎬")

st.title("🎬 Script Master: Multi-Model Edition")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔑 Configuração")
    gemini_key = st.text_input("Insere a tua Gemini API Key", type="password")
    
    st.divider()
    st.header("🤖 Escolha do Motor")
    # Lista baseada nos teus modelos disponíveis, priorizando os mais estáveis
    model_choice = st.selectbox("Modelo AI", [
        "models/gemini-2.0-flash-lite", 
        "models/gemini-1.5-flash",
        "models/gemini-2.0-flash",
        "models/gemini-flash-latest"
    ], help="Se obtiveres erro 429 (Quota), muda para a versão 'Lite'.")
    
    st.divider()
    st.header("🎭 Opções")
    plataforma = st.selectbox("Plataforma", ["Instagram Reels", "TikTok", "YouTube Shorts"])
    duracao = st.select_slider("Duração", options=["15s", "30s", "60s"])

# --- FUNÇÃO DE GERAÇÃO COM TRATAMENTO DE ERRO ---
def gerar_roteiro(tema, plataforma, model_name, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={"response_mime_type": "application/json"}
    )

    prompt = f"Cria um roteiro para {plataforma} de {duracao} sobre {tema}. Responde apenas JSON: {{'hook_texto': '...', 'hook_visual': '...', 'cenas': [{{'Cena': 1, 'Voz': '...', 'Vídeo': '...', 'Plano': '...', 'Som': '...'}}], 'cta': '...'}}"

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        if "429" in str(e):
            st.error("⚠️ **Limite de Quota Atingido!**")
            st.info("O Google limita pedidos gratuitos por minuto. Espera 60 segundos ou muda para o modelo 'Lite' na barra lateral.")
        raise e

# --- INTERFACE ---
tema_input = st.text_input("Qual o tema do vídeo?")

if st.button("🚀 Gerar Guião"):
    if not gemini_key:
        st.error("Insere a API Key!")
    elif tema_input:
        with st.spinner(f"A usar {model_choice}..."):
            try:
                res = gerar_roteiro(tema_input, plataforma, model_choice, gemini_key)
                
                st.divider()
                st.subheader(f"🪝 Gancho: {res['hook_texto']}")
                
                df = pd.DataFrame(res['cenas'])
                st.data_editor(df, use_container_width=True)
                
                st.success(f"📣 CTA: {res['cta']}")
            except Exception as e:
                # O erro já é tratado na função, mas isto evita que a app 'crash'
                pass
