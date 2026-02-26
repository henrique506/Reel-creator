import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

# Configuração da Página
st.set_page_config(page_title="Script Master: Gemini Edition", layout="wide", page_icon="♊")

st.title("♊ Script Master: Gemini AI")
st.markdown("Cria guiões virais usando o motor mais avançado da Google.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔑 Configuração")
    gemini_key = st.text_input("Insere a tua Gemini API Key", type="password")
    st.info("Obtém a tua chave grátis em: aistudio.google.com")
    
    st.divider()
    st.header("🎭 Personalização")
    plataforma = st.selectbox("Destino", ["Instagram Reels", "TikTok", "YouTube Shorts"])
    estilo = st.selectbox("Tipo", ["Tutorial Rápido", "Storytelling", "Venda", "Humor"])

# --- FUNÇÃO DE GERAÇÃO (CORRIGIDA) ---
def gerar_roteiro(tema, plataforma, estilo, key):
    genai.configure(api_key=key)
    
    # Tentamos o modelo Flash. Se der erro, o código avisa.
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={"response_mime_type": "application/json"}
    )

    prompt = f"""
    Cria um guião de vídeo curto para {plataforma} sobre {tema}. Estilo {estilo}.
    Responde apenas com este JSON:
    {{
      "hook_texto": "frase",
      "hook_visual": "descrição",
      "cenas": [
        {{"Cena": 1, "Voz": "texto", "Vídeo": "ação", "Plano": "tipo", "Som": "audio"}}
      ],
      "cta": "frase"
    }}
    """

    response = model.generate_content(prompt)
    return json.loads(response.text)

# --- INTERFACE ---
tema_input = st.text_input("Qual o tema do vídeo?")

if st.button("🚀 Gerar Guião"):
    if not gemini_key:
        st.error("Insere a tua API Key!")
    elif tema_input:
        with st.spinner("A processar..."):
            try:
                res = gerar_roteiro(tema_input, plataforma, estilo, gemini_key)
                
                st.subheader(f"🪝 Gancho: {res['hook_texto']}")
                
                df = pd.DataFrame(res['cenas'])
                st.data_editor(df, use_container_width=True)
                
                st.success(f"📣 CTA: {res['cta']}")
                
            except Exception as e:
                st.error(f"Erro: {e}")
                st.info("Dica: Se o erro for 404, verifica se a tua chave API no Google AI Studio tem acesso ao modelo Gemini 1.5 Flash.")
