import streamlit as st
import pandas as pd
from openai import OpenAI
import json

# Configuração da Página
st.set_page_config(page_title="Script Master Pro", layout="wide", page_icon="🎬")

st.title("🎬 Script Master Pro: Edição em Tempo Real")
st.markdown("A IA gera o rascunho, **tu assumes a direção.**")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔑 Configuração")
    api_key = st.text_input("Insere a tua OpenAI API Key", type="password")
    
    st.divider()
    st.header("⚙️ Definições")
    plataforma = st.selectbox("Plataforma", ["Instagram Reels", "TikTok", "YouTube Shorts"])
    tom = st.selectbox("Tom", ["Profissional", "Engraçado", "Inspirador", "Dinâmico"])
    st.info("💡 Dica: Depois de gerar, podes clicar em qualquer célula da tabela para alterar o conteúdo!")

# --- FUNÇÃO DE IA ---
def obter_guiao_ia(tema, plataforma, tom, api_key):
    client = OpenAI(api_key=api_key)
    
    # Prompt técnico para garantir que a IA devolve dados estruturados
    prompt = f"""
    Cria um guião de vídeo curto para {plataforma} sobre "{tema}" em tom {tom}.
    Responde APENAS com um objeto JSON no seguinte formato:
    {{
      "hook_texto": "frase",
      "hook_visual": "descrição",
      "cenas": [
        {{"Cena": 1, "Voz": "texto", "Vídeo": "ação", "Plano": "tipo", "Som": "efeito"}},
        ...
      ],
      "cta": "frase"
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "És um realizador de vídeos virais."},
                  {"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

# --- INTERFACE PRINCIPAL ---
tema_input = st.text_input("Qual é o tema do vídeo?", placeholder="Ex: Como organizar a secretária para produtividade")

if st.button("🚀 Gerar Storyboard Editável"):
    if not api_key:
        st.error("Insere a tua API Key na barra lateral.")
    elif tema_input:
        with st.spinner("A criar o teu guião..."):
            try:
                res = obter_guiao_ia(tema_input, plataforma, tom, api_key)
                
                # Exibir Hooks em destaque
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🪝 Ganchos (Hooks)")
                    st.write(f"**Texto:** {res['hook_texto']}")
                    st.write(f"**Visual:** {res['hook_visual']}")
                with col2:
                    st.subheader("📢 Call to Action")
                    st.info(res['cta'])

                st.divider()
                st.subheader("📝 Tabela de Produção (Clica para Editar)")
                
                # Criar DataFrame a partir do JSON da IA
                df_inicial = pd.DataFrame(res['cenas'])
                
                # O EDITOR MÁGICO
                # O utilizador pode editar, adicionar ou remover linhas aqui
                df_editado = st.data_editor(
                    df_inicial, 
                    num_rows="dynamic", 
                    use_container_width=True
                )

                # Opção de Download do ficheiro final
                st.divider()
                csv = df_editado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 Descarregar Guião Finalizado",
                    data=csv,
                    file_name=f"guiao_{tema_input.replace(' ', '_')}.csv",
                    mime="text/csv",
                )
                
            except Exception as e:
                st.error(f"Erro: {e}")
