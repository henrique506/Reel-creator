import streamlit as st
import pandas as pd
from openai import OpenAI
import json

# Configuração da Página
st.set_page_config(page_title="Script Master Pro", layout="wide", page_icon="🎬")

# --- DEFINIÇÃO DE ESTILOS ---
ESTILOS = {
    "Educativo/Tutorial": "Foca em passos claros (Passo 1, 2, 3). O tom deve ser de autoridade e ajuda.",
    "Storytelling/Vlog": "Cria uma narrativa emocional. Começa com um problema e termina com uma transformação.",
    "Comparação (Este vs Aquele)": "Divide o vídeo em dois lados. Mostra vantagens e desvantagens de forma dinâmica.",
    "Trends/Viral": "Usa frases curtas, cortes rápidos e foca em entretenimento puro e humor.",
    "Venda Direta": "Foca na dor do cliente e apresenta o produto como a única solução possível. CTA forte."
}

st.title("🎬 Script Master Pro: Studio Mode")
st.markdown("Cria guiões profissionais com IA, baseados no teu estilo de conteúdo.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔑 Configuração")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    st.header("🎭 Personalização")
    plataforma = st.selectbox("Plataforma", ["Instagram Reels", "TikTok", "YouTube Shorts"])
    estilo_escolhido = st.selectbox("Modelo de Estilo", list(ESTILOS.keys()))
    tom = st.select_slider("Nível de Energia", options=["Calmo", "Conversacional", "Enérgico", "Explosivo"])

# --- FUNÇÃO DE IA ---
def obter_guiao_ia(tema, plataforma, estilo, tom, api_key):
    client = OpenAI(api_key=api_key)
    detalhe_estilo = ESTILOS[estilo]
    
    prompt = f"""
    Cria um guião de vídeo curto para {plataforma}.
    TEMA: "{tema}"
    ESTILO DE CONTEÚDO: {estilo}. {detalhe_estilo}
    TOM: {tom}.
    
    Responde APENAS com um objeto JSON:
    {{
      "hook_texto": "frase de impacto no ecrã",
      "hook_visual": "o que acontece nos primeiros 2 segundos",
      "cenas": [
        {{"Cena": 1, "Voz": "fala", "Vídeo": "ação visual", "Plano": "tipo de plano", "Som": "audio"}},
        {{"Cena": 2, "Voz": "fala", "Vídeo": "ação visual", "Plano": "tipo de plano", "Som": "audio"}},
        {{"Cena": 3, "Voz": "fala", "Vídeo": "ação visual", "Plano": "tipo de plano", "Som": "audio"}}
      ],
      "cta": "chamada para ação final"
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "És um roteirista premiado de conteúdo curto."},
                  {"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

# --- INTERFACE PRINCIPAL ---
tema_input = st.text_area("O que queres comunicar neste vídeo?", height=100, placeholder="Ex: O segredo para ler 52 livros por ano...")

if st.button("🚀 Gerar Guiao Estruturado"):
    if not api_key:
        st.error("Por favor, adiciona a tua API Key na barra lateral.")
    elif tema_input:
        with st.spinner(f"A aplicar o estilo {estilo_escolhido}..."):
            try:
                res = obter_guiao_ia(tema_input, plataforma, estilo_escolhido, tom, api_key)
                
                # Layout de visualização
                c1, c2, c3 = st.columns(3)
                c1.metric("Gancho Visual", "Retenção Máxima")
                c2.metric("Estilo", estilo_escolhido)
                c3.metric("Plataforma", plataforma)

                with st.expander("🎥 Detalhes do Gancho (Hook)", expanded=True):
                    st.write(f"**Texto no Ecrã:** {res['hook_texto']}")
                    st.write(f"**Ação Inicial:** {res['hook_visual']}")

                st.subheader("📝 Storyboard Editável")
                df_editavel = st.data_editor(pd.DataFrame(res['cenas']), use_container_width=True, num_rows="dynamic")
                
                st.success(f"**CTA Final:** {res['cta']}")
                
                # Download
                st.download_button("💾 Exportar para Produção (CSV)", df_editavel.to_csv(index=False), "guiao_final.csv", "text/csv")
                
            except Exception as e:
                st.error(f"Erro na geração: {e}")
