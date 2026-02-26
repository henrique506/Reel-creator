import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

# Configuração da Página
st.set_page_config(page_title="Script Master AI", layout="wide", page_icon="🎬")

st.title("🎬 Script Master: Gemini Edition")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔑 Configuração")
    gemini_key = st.text_input("Insere a tua Gemini API Key", type="password")
    
    st.divider()
    st.header("🎭 Opções")
    plataforma = st.selectbox("Plataforma", ["Instagram Reels", "TikTok", "YouTube Shorts"])
    estilo = st.selectbox("Estilo", ["Tutorial", "Storytelling", "Venda", "Viral"])

# --- FUNÇÃO DE GERAÇÃO ROBUSTA ---
def gerar_roteiro(tema, plataforma, estilo, key):
    genai.configure(api_key=key)
    
    # Tentamos os nomes mais comuns do modelo 1.5 Flash
    # O 'gemini-1.5-flash' é o ID padrão atual
    model_id = "gemini-1.5-flash" 
    
    model = genai.GenerativeModel(
        model_name=model_id,
        generation_config={"response_mime_type": "application/json"}
    )

    prompt = f"""
    És um guionista de vídeos curtos. Cria um roteiro para {plataforma} sobre {tema}. Estilo {estilo}.
    Responde APENAS com este JSON:
    {{
      "hook_texto": "frase",
      "hook_visual": "descrição",
      "cenas": [
        {{"Cena": 1, "Voz": "fala", "Vídeo": "ação", "Plano": "tipo", "Som": "audio"}},
        {{"Cena": 2, "Voz": "fala", "Vídeo": "ação", "Plano": "tipo", "Som": "audio"}}
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
        st.error("Por favor, insere a API Key!")
    elif tema_input:
        with st.spinner("A ligar ao cérebro do Gemini..."):
            try:
                res = gerar_roteiro(tema_input, plataforma, estilo, gemini_key)
                
                st.info(f"🪝 **Gancho:** {res['hook_texto']}")
                
                # Tabela de Cenas
                df = pd.DataFrame(res['cenas'])
                st.subheader("📝 Roteiro Editável")
                df_final = st.data_editor(df, use_container_width=True, num_rows="dynamic")
                
                st.success(f"📣 **CTA:** {res['cta']}")
                
                # Exportar
                csv = df_final.to_csv(index=False).encode('utf-8')
                st.download_button("💾 Baixar Excel (CSV)", csv, "meu_guiao.csv", "text/csv")
                
            except Exception as e:
                st.error(f"Erro: {e}")
                st.warning("Dica: Verifica se a tua chave API no Google AI Studio (aistudio.google.com) está ativa.")
