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
    st.header("🎭 Estilo & Plataforma")
    plataforma = st.selectbox("Destino", ["Instagram Reels", "TikTok", "YouTube Shorts"])
    estilo = st.selectbox("Tipo de Conteúdo", ["Tutorial Rápido", "Storytelling Emocional", "Venda/Conversão", "Humor/Trend"])
    criatividade = st.slider("Nível de Criatividade", 0.0, 1.0, 0.7)

# --- LÓGICA DO GEMINI ---
def gerar_roteiro_gemini(tema, plataforma, estilo, key, criatividade):
    # Configurar a API
    genai.configure(api_key=key)
    
    # Configuração do Modelo (Focado no formato JSON)
    generation_config = {
        "temperature": criatividade,
        "top_p": 0.95,
        "response_mime_type": "application/json",
    }
    
    # Correção do Erro 404: Usar o caminho completo do modelo
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        generation_config=generation_config
    )

    # Prompt construído com cuidado para evitar erros de sintaxe no Python
    prompt = (
        f"És um guionista especialista em vídeos curtos para {plataforma}. "
        f"Tema: {tema}. Estilo: {estilo}. "
        "Gera um guião estruturado no seguinte formato JSON estrito: "
        "{"
        "\"hook_texto\": \"frase de impacto\", "
        "\"hook_visual\": \"descrição da primeira cena\", "
        "\"cenas\": ["
        "{\"Cena\": 1, \"Voz\": \"fala\", \"Vídeo\": \"ação\", \"Plano\": \"enquadramento\", \"Som\": \"audio\"}"
        "], "
        "\"cta\": \"chamada para ação final\""
        "}"
    )

    response = model.generate_content(prompt)
    return json.loads(response.text)

# --- INTERFACE PRINCIPAL ---
tema_input = st.text_area("Sobre o que queres falar hoje?", placeholder="Ex: Por que é que o café sabe melhor de manhã?")

if st.button("🚀 Gerar Guião com Gemini"):
    if not gemini_key:
        st.error("Esqueceste-te da API Key na barra lateral!")
    elif tema_input:
        with st.spinner("O Gemini está a escrever o teu próximo viral..."):
            try:
                res = gerar_roteiro_gemini(tema_input, plataforma, estilo, gemini_key, criatividade)
                
                # Exibição de Resumo
                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    st.success("🪝 Gancho de Texto")
                    st.subheader(res.get('hook_texto', 'Sem gancho'))
                with col2:
                    st.info("👁️ Gancho Visual")
                    st.write(res.get('hook_visual', 'Sem descrição'))

                # Tabela Editável
                st.subheader("📝 Storyboard Detalhado (Clica para editar)")
                if 'cenas' in res:
                    df = pd.DataFrame(res['cenas'])
                    df_final = st.data_editor(df, use_container_width=True, num_rows="dynamic")
                    
                    st.warning(f"📣 **CTA Sugerido:** {res.get('cta', 'Sem CTA')}")

                    # Botão de Exportar
                    csv = df_final.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="💾 Descarregar para Excel (CSV)",
                        data=csv,
                        file_name="guiao_gemini.csv",
                        mime="text/csv",
                    )
                else:
                    st.error("A IA não gerou as cenas corretamente. Tenta de novo.")
                
            except Exception as e:
                st.error(f"Erro ao processar: {e}")
