"""Sidebar compartilhada entre todas as páginas."""
import streamlit as st

CORES = {
    "bg":          "#efece6",
    "sidebar":     "#1d5a63",
    "sidebar2":    "#174a52",
    "card":        "#cfe7e3",
    "card_border": "#b2d5d0",
    "ink":         "#16323a",
    "ink2":        "#3b5a60",
    "good":        "#2e8a5e",
    "bad":         "#c84a3b",
    "warn":        "#e7b53b",
    "bar":         "#2a6066",
}

BASE_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {CORES['bg']} !important;
    color: {CORES['ink']} !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    background: {CORES['sidebar']};
    border-right: 2px solid #2a8aa3;
}}
[data-testid="stSidebar"] * {{ color: #eaf6f5 !important; }}
[data-testid="stSidebar"] .stMultiSelect span {{
    background: {CORES['sidebar2']} !important;
    color: #eaf6f5 !important;
}}
.main .block-container {{
    background: {CORES['bg']};
    padding-top: 1rem;
}}
.user-tag {{
    background: {CORES['card']}; color: #174a52 !important;
    font-size: 9px; font-weight: 700;
    letter-spacing: 0.08em;
    padding: 2px 7px; border-radius: 3px;
    display: inline-block; margin-top: 4px;
}}
hr.atlas {{ border: none; border-top: 1px solid #2a7a89; margin: 8px 0; }}

/* Nav buttons */
div[data-testid="stSidebar"] .stButton > button {{
    width: 100%;
    background: transparent !important;
    border: none !important;
    color: #eaf6f5 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    text-align: left !important;
    padding: 10px 12px !important;
    border-radius: 8px !important;
    margin-bottom: 2px !important;
    cursor: pointer;
}}
div[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(255,255,255,0.12) !important;
}}
div[data-testid="stSidebar"] .nav-active > button {{
    background: rgba(255,255,255,0.18) !important;
    font-weight: 700 !important;
}}
</style>
"""

PAGES = {
    "Dashboard":   "pages/1_dashboard.py",
    "Publicações": "pages/2_publicacoes.py",
    "Resumo":      "pages/3_resumo.py",
    "Descobertas": None,
}

def render(pagina_atual: str, n_publicacoes: int = 0, extra_content=None):
    """
    Renderiza a sidebar.
    pagina_atual: nome da página ativa (ex: 'Dashboard')
    extra_content: callable opcional executado após os botões de nav (ex: filtros)
    """
    st.markdown(BASE_CSS, unsafe_allow_html=True)

    with st.sidebar:
        # Perfil
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;background:#174a52;
                    border:1px solid #2a8aa3;border-radius:8px;padding:10px;margin-bottom:12px">
            <div style="width:44px;height:44px;border-radius:50%;
                        background:linear-gradient(135deg,#f1c27d,#d99a5b);
                        border:2px solid #fff;display:flex;align-items:center;
                        justify-content:center;font-size:18px;flex-shrink:0">👤</div>
            <div>
                <div style="font-size:13px;font-weight:600;color:#eaf6f5">João Cabral</div>
                <span class="user-tag">SEBRAE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats
        st.markdown(f"""
        <div style="font-size:11.5px;line-height:2;color:#b8d6d4;margin-bottom:6px">
            <div>Publicações — <b style="color:#eaf6f5">{n_publicacoes or 947083}</b></div>
            <div>Pessoas — <b style="color:#eaf6f5">55.144</b></div>
            <div>Data — <b style="color:#eaf6f5">01/04/26 a 30/04/26</b></div>
            <div style="font-size:10px;color:#7ab8b0">(30 dias)</div>
        </div>
        <hr class="atlas"/>
        """, unsafe_allow_html=True)

        # Botões de navegação
        for nome in PAGES:
            ativo = nome == pagina_atual
            # Wrap em div com classe especial se ativo
            if ativo:
                st.markdown("<div class='nav-active'>", unsafe_allow_html=True)
            if st.button(nome, key=f"nav_{nome}", use_container_width=True):
                destino = PAGES[nome]
                if destino:
                    st.switch_page(destino)
            if ativo:
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='atlas'/>", unsafe_allow_html=True)

        # Conteúdo extra (filtros, botões específicos da página)
        if extra_content:
            extra_content()