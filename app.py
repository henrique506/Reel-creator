import streamlit as st
import pandas as pd
from openai import OpenAI
import json

# Configuração da Página
st.set_page_config(page_title="Script Master AI: Vision", layout="wide", page_icon="🎬")

st.title("🎬 Script Master AI: Vision Edition")
st.markdown("O teu guião, do texto à imagem.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔑 Chaves de Acesso")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    st.header("🎭 Estilo Visual")
    vibe_visual = st.selectbox("Estética das Imagens", 
                                ["Cinemático", "Vlog Realista", "Minimalista/Clean", "Anime/Ilustração", "Estilo Estúdio Profissional"])
    plataforma = st.selectbox("Plataforma", ["Instagram Reels", "TikTok", "YouTube Shorts"])
    estilo_conteudo = st.selectbox("Estilo", ["Tutorial", "Storytelling", "Viral", "Venda"])

# --- FUNÇÃO DE IA (TEXTO) ---
def gerar_guiao_texto(tema, plataforma, estilo, api_key):
    client = OpenAI(api_key=api_key)
    prompt = f"Cria um guião para {plataforma} sobre {tema}. Estilo {estilo}. Responde apenas JSON com: hook_texto, hook_visual, cta, e cenas (lista com Cena, Voz, Vídeo, Plano, Som, Prompt_Imagem_Dalle)."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

# --- FUNÇÃO DE IA (IMAGEM) ---
def gerar_imagem_storyboard(prompt_cena, estilo_visual, api_key):
    client = OpenAI(api_key=api_key)
    full_prompt = f"Storyboard frame: {prompt_cena}. Style: {estilo_visual}. 9:16 aspect ratio feel, professional cinematography."
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=full_prompt,
        size="1024x1024", # Nota: DALL-E 3 gera quadrado, mas podemos simular o enquadramento
        quality="standard",
        n=1,
    )
    return response.data[0].url

# --- INTERFACE PRINCIPAL ---
tema = st.text_input("Tema do Vídeo", placeholder="Ex: Como fazer o pequeno-almoço perfeito em 2 minutos")

if st.button("1. Gerar Estrutura de Texto"):
    if api_key and tema:
        st.session_state.guiao = gerar_guiao_texto(tema, plataforma, estilo_conteudo, api_key)
        st.success("Guião de texto pronto!")

if "guiao" in st.session_state:
    res = st.session_state.guiao
    
    st.subheader("📝 Edita o teu roteiro")
    df_editado = st.data_editor(pd.DataFrame(res['cenas']), use_container_width=True)
    
    st.divider()
    
    if st.button("🎨 2. Gerar Storyboard Visual (IA)"):
        with st.spinner("A desenhar as tuas cenas..."):
            colunas_img = st.columns(len(df_editado))
            for i, row in df_editado.iterrows():
                with colunas_img[i]:
                    st.caption(f"Cena {row['Cena']}")
                    img_url = gerar_imagem_storyboard(row['Prompt_Imagem_Dalle'], vibe_visual, api_key)
                    st.image(img_url, use_column_width=True)
                    st.info(f"🎥 {row['Plano']}")

# Rodapé informando sobre custos
st.sidebar.warning("⚠️ Nota: O DALL-E 3 tem um custo por imagem gerada na tua conta OpenAI.")
