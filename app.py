import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

# Configuração da Página
st.set_page_config(page_title="Script Master 2026", layout="wide", page_icon="🎬")

st.title("🎬 Script Master: Next Gen (Gemini 2.5)")
st.markdown("A usar o motor: `models/gemini-2.5-flash` para máxima performance.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔑 Configuração")
    gemini_key = st.text_input("Insere a tua Gemini API Key", type="password")
    
    st.divider()
    st.header("🎭 Opções de Vídeo")
    plataforma = st.selectbox("Plataforma", ["Instagram Reels", "TikTok", "YouTube Shorts"])
    estilo = st.selectbox("Estilo", ["Tutorial", "Storytelling", "Venda/UGC", "Humor/Trend"])
    duracao = st.select_slider("Duração Desejada", options=["15s", "30s", "60s"])

# --- FUNÇÃO DE GERAÇÃO ATUALIZADA ---
def gerar_roteiro(tema, plataforma, estilo, duracao, key):
    genai.configure(api_key=key)
    
    # Atualizado para o modelo que confirmaste ter acesso
    model = genai.GenerativeModel(
        model_name="models/gemini-2.5-flash",
        generation_config={"response_mime_type": "application/json"}
    )

    prompt = f"""
    És um guionista de elite para {plataforma}. 
    Cria um roteiro de {duracao} sobre o tema: "{tema}".
    Estilo de conteúdo: {estilo}.
    
    Responde APENAS com este formato JSON:
    {{
      "hook_texto": "texto para o ecrã",
      "hook_visual": "ação inicial rápida",
      "cenas": [
        {{"Cena": 1, "Voz": "o que dizer", "Vídeo": "o que filmar", "Plano": "enquadramento", "Som": "audio/efeito"}},
        {{"Cena": 2, "Voz": "o que dizer", "Vídeo": "o que filmar", "Plano": "enquadramento", "Som": "audio/efeito"}},
        {{"Cena": 3, "Voz": "o que dizer", "Vídeo": "o que filmar", "Plano": "enquadramento", "Som": "audio/efeito"}},
        {{"Cena": 4, "Voz": "o que dizer", "Vídeo": "o que filmar", "Plano": "enquadramento", "Som": "audio/efeito"}}
      ],
      "cta": "chamada para ação final"
    }}
    Usa linguagem dinâmica e focada em retenção.
    """

    response = model.generate_content(prompt)
    return json.loads(response.text)

# --- INTERFACE PRINCIPAL ---
tema_input = st.text_input("Qual o tema do teu próximo vídeo?")

if st.button("🚀 Criar Guia Profissional"):
    if not gemini_key:
        st.error("Por favor, insere a API Key na barra lateral.")
    elif tema_input:
        with st.spinner(f"O Gemini 2.5 está a roteirizar para {plataforma}..."):
            try:
                res = gerar_roteiro(tema_input, plataforma, estilo, duracao, gemini_key)
                
                # Layout de Resultados
                st.divider()
                c1, c2 = st.columns(2)
                with c1:
                    st.success(f"🪝 **Hook de Texto:** {res['hook_texto']}")
                with c2:
                    st.info(f"👁️ **Hook Visual:** {res['hook_visual']}")

                # Tabela de Edição
                st.subheader("📝 Storyboard Editável")
                df = pd.DataFrame(res['cenas'])
                df_editado = st.data_editor(df, use_container_width=True, num_rows="dynamic")
                
                st.warning(f"📣 **CTA:** {res['cta']}")

                # Download
                csv = df_editado.to_csv(index=False).encode('utf-8')
                st.download_button("💾 Exportar para Produção (Excel/CSV)", csv, "meu_guiao_viral.csv", "text/csv")
                
            except Exception as e:
                st.error(f"Erro na geração: {e}")
