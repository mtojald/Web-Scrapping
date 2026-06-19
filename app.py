import json

import streamlit as st

from src.bot.bot import ScrapBot
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
            bot = ScrapBot()
            colecao = bot.coletar_tudo()
            with open(RESULTADO_PATH, "w", encoding="utf-8") as f:
                json.dump(colecao.como_lista_dicts(), f, indent=4, ensure_ascii=False)
            st.session_state["dados_scraping"] = colecao.como_lista_dicts()
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
