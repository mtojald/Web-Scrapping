import streamlit as st
import json
from src.bot.bot import scrapBot
from src.bot.reqParams import RESULTADO_PATH

st.set_page_config(
    page_title="Atlas Insights — SEBRAE",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

if "dados_carregados" not in st.session_state:
    with st.spinner("Coletando dados..."):
        try:
            bot = scrapBot()
            dados = bot.scrappersEmSeq()
            with open(RESULTADO_PATH, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            st.session_state["dados_carregados"] = True
        except Exception as e:
            st.error(f"Erro no scraping: {e}")
            st.stop()

pg = st.navigation(
    [
        st.Page("pages/1_dashboard.py",   title="Dashboard",   icon="📊"),
        st.Page("pages/2_publicacoes.py", title="Publicações", icon="📋"),
        st.Page("pages/3_resumo.py",      title="Resumo",      icon="📝"),
    ],
    position="hidden",
)
pg.run()