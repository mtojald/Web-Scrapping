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
    dados = bot.scrappersEmSeq()
    import json
    from src.bot.reqParams import RESULTADO_PATH
    with open(RESULTADO_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)