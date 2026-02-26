import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

st.set_page_config(page_title="Script Master Pro", layout="wide")
st.title("🎬 Script Master: Gemini Edition")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔑 Configuração")
    gemini_key = st.text_input("Insere a tua Gemini API Key", type="password")
    
    # BOTÃO DE DIAGNÓSTICO
    if st.button("🔍 Testar Conexão e Modelos"):
        if not gemini_key:
            st.error("Insere a chave primeiro!")
        else:
            try:
                genai.configure(api_key=gemini_key)
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                st.write("Modelos disponíveis na tua conta:")
                st.code("\n".join(models))
            except Exception as e:
                st.error(f"Erro ao listar modelos: {e}")

# --- FUNÇÃO DE GERAÇÃO INTELIGENTE ---
def gerar_roteiro(tema, plataforma, key):
    genai.configure(api_key=key)
    
    # Tenta encontrar o melhor nome de modelo disponível
    try:
        model_names = [m.name for m in genai.list_models() if '1.5-flash' in m.name]
        selected_model = model_names[0] if model_names else "gemini-1.5-flash"
    except:
        selected_model = "gemini-1.5-flash"

    model = genai.GenerativeModel(
        model_name=selected_model,
        generation_config={"response_mime_type": "application/json"}
    )

    prompt = f"""
    Cria um roteiro para {plataforma} sobre {tema}.
    Responde APENAS com este JSON:
    {{
      "hook_texto": "frase impacto",
      "hook_visual": "descrição",
      "cenas": [
        {{"Cena": 1, "Voz": "fala", "Vídeo": "ação", "Plano": "enquadramento", "Som": "audio"}}
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
        st.error("Insere a API Key!")
    elif tema_input:
        with st.spinner("A criar..."):
            try:
                res = gerar_roteiro(tema_input, "Reels/TikTok", "Viral", gemini_key)
                st.info(f"🪝 Gancho: {res['hook_texto']}")
                st.data_editor(pd.DataFrame(res['cenas']), use_container_width=True)
                st.success(f"📣 CTA: {res['cta']}")
            except Exception as e:
                st.error(f"Erro: {e}")
                st.warning("Se o erro persistir, usa o botão 'Testar Conexão' na lateral para ver os nomes dos modelos.")
