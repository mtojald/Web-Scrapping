import streamlit as st
from src.bot.bot import scrapBot

st.set_page_config(
    page_title="Atlas Insights — SEBRAE",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

@st.cache_data(show_spinner="Coletando dados...")
def rodar_scraping():
    bot = scrapBot()
    bot.rodar_scraping()

rodar_scraping()

pg = st.navigation(
    [
        st.Page("pages/1_dashboard.py",   title="Dashboard",   icon="📊"),
        st.Page("pages/2_publicacoes.py", title="Publicações", icon="📋"),
        st.Page("pages/3_resumo.py",      title="Resumo",      icon="📝"),
    ],
    position="hidden",
)
pg.run()