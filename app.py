import streamlit as st

st.set_page_config(
    page_title="Atlas Insights — SEBRAE",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

pg = st.navigation(
    [
        st.Page("pages/1_dashboard.py",   title="Dashboard",   icon="📊"),
        st.Page("pages/2_publicacoes.py", title="Publicações", icon="📋"),
        st.Page("pages/3_resumo.py",      title="Resumo",      icon="📝"),
    ],
    position="hidden",   # esconde o menu padrão — usamos nossa própria sidebar
)

pg.run()