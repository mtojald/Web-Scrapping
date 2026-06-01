import json
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Atlas Insights — SEBRAE", layout="wide", page_icon="📊")

CORES = {
    "bg":           "#efece6",
    "sidebar":      "#1d5a63",
    "sidebar2":     "#174a52",
    "card":         "#cfe7e3",
    "card_border":  "#b2d5d0",
    "ink":          "#16323a",
    "ink2":         "#3b5a60",
    "good":         "#2e8a5e",
    "bad":          "#c84a3b",
    "warn":         "#e7b53b",
    "bar":          "#2a6066",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {CORES['bg']} !important;
    color: {CORES['ink']} !important;
}}

/* Sidebar */
[data-testid="stSidebar"] > div:first-child {{
    background: {CORES['sidebar']};
    border-right: 2px solid #2a8aa3;
}}
[data-testid="stSidebar"] * {{
    color: #eaf6f5 !important;
}}
[data-testid="stSidebar"] .stMultiSelect span {{
    background: {CORES['sidebar2']} !important;
    color: #eaf6f5 !important;
}}

/* Métricas */
[data-testid="stMetric"] {{
    background: {CORES['card']};
    border: 1.5px solid {CORES['card_border']};
    border-radius: 14px;
    padding: 16px 20px;
}}
[data-testid="stMetricLabel"] p {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    color: {CORES['ink2']} !important;
}}
[data-testid="stMetricValue"] {{
    font-size: 26px !important;
    font-weight: 700 !important;
    color: {CORES['ink']} !important;
}}

/* Cards genéricos */
.atlas-card {{
    background: {CORES['card']};
    border: 1.5px solid {CORES['card_border']};
    border-radius: 14px;
    padding: 18px 20px 16px;
}}
.atlas-card h4 {{
    margin: 0 0 2px;
    font-size: 15px;
    font-weight: 700;
    color: {CORES['ink']};
}}
.atlas-card .mono {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: {CORES['ink2']};
    margin-bottom: 10px;
}}

/* Post card */
.post-card {{
    background: #fff;
    border: 1px solid #e3e8ec;
    border-radius: 12px;
    padding: 14px;
    font-size: 13px;
    color: #15202b;
}}
.post-avatar {{
    width: 40px; height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6b8cff, #9b5bff);
    display: inline-flex; align-items: center; justify-content: center;
    color: #fff; font-weight: 700; font-size: 14px;
    float: left; margin-right: 10px;
}}
.post-name {{ font-weight: 700; font-size: 13.5px; }}
.post-handle {{ font-size: 12px; color: #5b7083; }}
.post-body {{ margin: 10px 0 8px; font-size: 13.5px; line-height: 1.4; clear: both; }}
.post-time {{ font-size: 11.5px; color: #5b7083; margin-bottom: 10px; }}
.post-stats {{
    display: flex; gap: 16px;
    padding-top: 10px;
    border-top: 1px solid #eff3f4;
    font-size: 12px; color: #5b7083;
}}

/* Header tag */
.user-tag {{
    background: {CORES['card']};
    color: #174a52;
    font-size: 9px; font-weight: 700;
    letter-spacing: 0.08em;
    padding: 2px 7px; border-radius: 3px;
    display: inline-block; margin-top: 4px;
}}

/* Divider */
hr.atlas {{ border: none; border-top: 1px solid #2a7a89; margin: 8px 0; }}

/* Main bg */
.main .block-container {{
    background: {CORES['bg']};
    padding-top: 1rem;
}}
</style>
""", unsafe_allow_html=True)

# ── CARREGAR DADOS ────────────────────────────────────────────────────────────
try:
    with open("resultado_sebrae_local.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
except FileNotFoundError:
    st.error("arquivo 'resultado_sebrae_local.json' não encontrado. execute main.py primeiro.")
    st.stop()

df = pd.DataFrame(dados)

# ── NOTA / SENTIMENTO ─────────────────────────────────────────────────────────
def extrair_nota(av):
    m = re.search(r"(\d+(?:[.,]\d+)?)", str(av))
    if not m:
        return None
    val = float(m.group(1).replace(",", "."))
    return round(val) if val <= 5 else None

def sentimento(n):
    if n is None: return "Sem nota"
    if n >= 4:    return "Positivo"
    if n == 3:    return "Neutro"
    return "Negativo"

df["nota"]      = df["avaliacao"].apply(extrair_nota)
df["sentimento"] = df["nota"].apply(sentimento)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;background:#174a52;border:1px solid #2a8aa3;border-radius:8px;padding:10px;margin-bottom:12px">
        <div style="width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#f1c27d,#d99a5b);border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">👤</div>
        <div>
            <div style="font-size:13px;font-weight:600;color:#eaf6f5">Atlas Insights</div>
            <span class="user-tag">ATLAS</span>
        </div>
    </div>
    <hr class="atlas"/>
    """, unsafe_allow_html=True)

    fontes = sorted(df["fonte"].unique()) if "fonte" in df.columns else []
    filtro_fonte = st.multiselect("Fonte", options=fontes, default=fontes)

    sentimentos_disponiveis = list(df["sentimento"].unique())
    filtro_sentimento = st.multiselect("Sentimento", options=sentimentos_disponiveis, default=sentimentos_disponiveis)

    st.markdown("<hr class='atlas'/>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:11.5px;line-height:1.8;color:#b8d6d4">
        <div><span style="color:#b8d6d4">Publicações</span> — {len(df)}</div>
        <div><span style="color:#b8d6d4">Fontes</span> — {df['fonte'].nunique() if 'fonte' in df.columns else 1}</div>
        <div><span style="color:#b8d6d4">Busca</span> — SEBRAE</div>
    </div>
    """, unsafe_allow_html=True)

# ── FILTRAR ───────────────────────────────────────────────────────────────────
df_f = df[df["sentimento"].isin(filtro_sentimento)]
if filtro_fonte:
    df_f = df_f[df_f["fonte"].isin(filtro_fonte)]

# ── CALCULAR NPS / CSAT ───────────────────────────────────────────────────────
total = len(df_f)
positivos = len(df_f[df_f["sentimento"] == "Positivo"])
negativos = len(df_f[df_f["sentimento"] == "Negativo"])
nps  = round(((positivos - negativos) / total) * 100) if total > 0 else 0
nps  = max(0, min(100, nps + 50))  # normaliza p/ 0-100
csat = round((positivos / total) * 100) if total > 0 else 0

# ── GAUGE ─────────────────────────────────────────────────────────────────────
def make_gauge(valor, titulo):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        title={"text": titulo, "font": {"size": 14, "family": "DM Sans", "color": CORES["ink"]}},
        number={"suffix": "%", "font": {"size": 22, "family": "DM Sans", "color": CORES["ink"]}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 9, "color": CORES["ink2"]}},
            "bar": {"color": "#1a2c4e", "thickness": 0.25},
            "bgcolor": CORES["card"],
            "borderwidth": 0,
            "steps": [
                {"range": [0,  20], "color": "#d24a3a"},
                {"range": [20, 40], "color": "#e88a3c"},
                {"range": [40, 60], "color": "#e9c13a"},
                {"range": [60, 80], "color": "#8ab94a"},
                {"range": [80,100], "color": "#2e8a5e"},
            ],
        }
    ))
    fig.update_layout(
        height=200, margin=dict(t=30, b=0, l=20, r=20),
        paper_bgcolor=CORES["card"], font_color=CORES["ink"],
    )
    return fig

# ── TÍTULO ────────────────────────────────────────────────────────────────────
st.markdown("<div style='font-size:13px;color:#8a8a83;letter-spacing:0.02em;margin-bottom:4px'>Dashboard</div>", unsafe_allow_html=True)

# ── MÉTRICAS ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Total feedbacks", total)
with c2: st.metric("Positivos", positivos)
with c3: st.metric("Negativos", negativos)
with c4:
    media = df_f["nota"].dropna().mean()
    st.metric("Média (com nota)", f"{media:.1f} ⭐" if not pd.isna(media) else "N/A")

st.markdown("<div style='margin-top:8px'/>", unsafe_allow_html=True)

# ── LINHA 1: GAUGES + POST + RECLAMAÇÕES ─────────────────────────────────────
col_nps, col_post, col_comp = st.columns([1, 1.35, 1.25])

with col_nps:
    st.markdown("<div class='atlas-card'>", unsafe_allow_html=True)
    st.plotly_chart(make_gauge(nps, "Índice NPS"), use_container_width=True, key="nps")
    st.plotly_chart(make_gauge(csat, "Índice CSAT"), use_container_width=True, key="csat")
    st.markdown("</div>", unsafe_allow_html=True)

with col_post:
    st.markdown("<div class='atlas-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Principal publicação</h4><div class='mono'>(Redes e mídias)</div>", unsafe_allow_html=True)

    if not df_f.empty:
        top = df_f.sort_values("data", ascending=False).iloc[0] if "data" in df_f.columns else df_f.iloc[0]
        fonte_sigla = str(top.get("fonte", "NW"))[:2].upper()
        titulo = str(top.get("titulo_feedback", ""))[:60]
        corpo  = str(top.get("comentario_usuario", ""))[:200]
        data   = str(top.get("data", ""))
        av     = str(top.get("avaliacao", ""))

        st.markdown(f"""
        <div class="post-card">
            <div class="post-avatar">{fonte_sigla}</div>
            <div>
                <div class="post-name">{titulo}</div>
                <div class="post-handle">{top.get('fonte','NewsAPI')} · {data}</div>
            </div>
            <div class="post-body">{corpo}{"..." if len(str(top.get("comentario_usuario",""))) > 200 else ""}</div>
            <div class="post-time">{data}</div>
            <div class="post-stats">
                <span>{av}</span>
                <span>Sentimento: <b>{top.get('sentimento','—')}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px'>", unsafe_allow_html=True)
    fig_pie = px.pie(
        df_f, names="sentimento",
        color="sentimento",
        color_discrete_map={"Positivo": CORES["good"], "Neutro": CORES["warn"], "Negativo": CORES["bad"], "Sem nota": "#8ab4af"},
        hole=0.4,
    )
    fig_pie.update_layout(
        height=220, margin=dict(t=10, b=0, l=0, r=0),
        paper_bgcolor=CORES["card"], plot_bgcolor=CORES["card"],
        legend=dict(font=dict(size=11, color=CORES["ink2"])),
        showlegend=True,
    )
    fig_pie.update_traces(textfont_size=11)
    st.plotly_chart(fig_pie, use_container_width=True, key="pie")
    st.markdown("</div></div>", unsafe_allow_html=True)

with col_comp:
    st.markdown("<div class='atlas-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Sentimentos por fonte</h4><div class='mono'>(Canal de Atendimento)</div>", unsafe_allow_html=True)

    if "fonte" in df_f.columns:
        fig_bar = px.histogram(
            df_f, x="fonte", color="sentimento", barmode="group",
            color_discrete_map={"Positivo": CORES["good"], "Neutro": CORES["warn"], "Negativo": CORES["bad"], "Sem nota": "#8ab4af"},
        )
        fig_bar.update_layout(
            height=230, margin=dict(t=10, b=30, l=0, r=0),
            paper_bgcolor=CORES["card"], plot_bgcolor=CORES["card"],
            xaxis=dict(tickfont=dict(size=10, color=CORES["ink2"]), gridcolor="#b2d5d0"),
            yaxis=dict(tickfont=dict(size=10, color=CORES["ink2"]), gridcolor="#b2d5d0"),
            legend=dict(font=dict(size=10, color=CORES["ink2"])),
            bargap=0.2,
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_fonte")

    # Menções ao longo do tempo
    st.markdown("<h4 style='margin-top:10px'>Menções ao longo do tempo</h4><div class='mono'>(Redes e mídias)</div>", unsafe_allow_html=True)
    if "data" in df_f.columns:
        df_time = df_f[df_f["data"].notna() & (df_f["data"] != "")]
        if not df_time.empty:
            df_time2 = df_time.groupby(["data", "sentimento"]).size().reset_index(name="count")
            fig_line = px.line(
                df_time2, x="data", y="count", color="sentimento", markers=True,
                color_discrete_map={"Positivo": CORES["good"], "Neutro": CORES["warn"], "Negativo": CORES["bad"], "Sem nota": "#8ab4af"},
            )
            fig_line.update_layout(
                height=200, margin=dict(t=10, b=30, l=0, r=0),
                paper_bgcolor=CORES["card"], plot_bgcolor=CORES["card"],
                xaxis=dict(tickfont=dict(size=9, color=CORES["ink2"]), gridcolor="#b2d5d0"),
                yaxis=dict(tickfont=dict(size=9, color=CORES["ink2"]), gridcolor="#b2d5d0"),
                legend=dict(font=dict(size=10, color=CORES["ink2"])),
            )
            fig_line.update_traces(line=dict(width=2.5))
            st.plotly_chart(fig_line, use_container_width=True, key="line_tempo")

    st.markdown("</div>", unsafe_allow_html=True)

# ── TABELA ────────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:18px'/>", unsafe_allow_html=True)
st.markdown("<div class='atlas-card'><h4>Feedbacks</h4><div class='mono'>todos os registros coletados</div>", unsafe_allow_html=True)
colunas = ["fonte", "titulo_feedback", "comentario_usuario", "avaliacao", "sentimento", "data"]
colunas_ok = [c for c in colunas if c in df_f.columns]
st.dataframe(
    df_f[colunas_ok].reset_index(drop=True),
    use_container_width=True,
    height=280,
)
st.markdown("</div>", unsafe_allow_html=True)