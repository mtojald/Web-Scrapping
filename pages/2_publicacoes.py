import json
import re
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime, date
import streamlit as st
import pages.sidebar as sidebar

CORES = sidebar.CORES

# ── CARREGAR DADOS ────────────────────────────────────────────────────────────
try:
    with open("src/JSON/reqPlataformas.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
except FileNotFoundError:
    st.error("Arquivo não encontrado. Execute main.py primeiro.")
    st.stop()

# ── CLASSIFICAR SENTIMENTO ────────────────────────────────────────────────────
def extrair_nota(av):
    m = re.search(r"(\d+(?:[.,]\d+)?)", str(av))
    if not m: return None
    val = float(m.group(1).replace(",", "."))
    return round(val) if val <= 5 else None

def sentimento(item):
    nota = extrair_nota(item.get("avaliacao", ""))
    if nota is not None:
        if nota >= 4: return "Positivo"
        if nota == 3: return "Neutro"
        return "Crítico"
    texto = " ".join([str(item.get("titulo_feedback", "")), str(item.get("comentario_usuario", ""))]).lower()
    pos_kw = ["agradec","parabéns","excelente","ótimo","apoio","expande","cresce","inovação",
              "capacita","fortalec","solução","sucesso","gratuito","benefici"]
    neg_kw = ["erro","falha","problema","trava","não consigo","urgente","crítico",
              "reclamação","bug","sistema","prejuízo","dificuldade","impedimento"]
    p = sum(1 for kw in pos_kw if kw in texto)
    n = sum(1 for kw in neg_kw if kw in texto)
    if n > p: return "Crítico"
    if p > n: return "Positivo"
    return "Neutro"

def tempo_relativo(data_str):
    if not data_str: return "Data desconhecida"
    try:
        d = datetime.strptime(str(data_str)[:10], "%Y-%m-%d").date()
        delta = (date.today() - d).days
        if delta == 0: return "Hoje"
        if delta == 1: return "Há 1 dia"
        if delta < 7:  return f"Há {delta} dias"
        if delta < 30: return f"Há {delta // 7} semana(s)"
        return f"Há {delta // 30} mês(es)"
    except Exception:
        return str(data_str)

def get_fonte_icon(fonte):
    return {"NewsAPI":"📰","YouTube":"▶️","Reddit":"🤖","Twitter":"🐦","Instagram":"📸"}.get(fonte,"🌐")

def get_fonte_bg(fonte):
    return {"NewsAPI":"#fff0f0","YouTube":"#fff0f0","Reddit":"#fff4ef","Twitter":"#e8f4fd","Instagram":"#fce4f0"}.get(fonte,"#f0f4f8")

def badge_html(sent):
    cls = sent.lower().replace(" ","_").replace("í","i")
    icons = {"positivo":"👍","neutro":"😐","critico":"🔴","negativo":"👎","sem_nota":"⚪"}
    icon = icons.get(cls, "•")
    colors = {
        "positivo": ("d4f0e4","2e8a5e","a8ddc4"),
        "neutro":   ("fef8e6","b5870a","f0d98a"),
        "critico":  ("fde8e6","c84a3b","f0b0aa"),
        "negativo": ("fde8e6","c84a3b","f0b0aa"),
        "sem_nota": ("e8edf0","5b7083","c5ced4"),
    }
    bg, fg, border = colors.get(cls, ("e8edf0","5b7083","c5ced4"))
    return (f'<span style="background:#{bg};color:#{fg};border:1.5px solid #{border};'
            f'border-radius:50px;padding:7px 18px;font-size:13px;font-weight:700;'
            f'display:inline-flex;align-items:center;gap:6px">{icon} {sent}</span>')

for item in dados:
    item["sentimento_calc"] = sentimento(item)
    item["tempo_rel"] = tempo_relativo(item.get("data", ""))

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
filtro_fonte = []
filtro_sent  = []
busca        = ""

def sidebar_extra():
    global filtro_fonte, filtro_sent, busca
    fontes_disp = sorted(set(x["fonte"] for x in dados))
    filtro_fonte = st.multiselect("Fonte", options=fontes_disp, default=fontes_disp)
    sents_disp = sorted(set(x["sentimento_calc"] for x in dados))
    filtro_sent = st.multiselect("Sentimento", options=sents_disp, default=sents_disp)
    busca = st.text_input("🔍 Buscar texto", placeholder="Palavra-chave...")

sidebar.render("Publicações", n_publicacoes=len(dados), extra_content=sidebar_extra)

# ── CSS EXTRA ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
.pub-section-header {{
    display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700;
    color:#1d5a63;letter-spacing:0.04em;margin-bottom:16px;text-transform:uppercase;
}}
.pub-section-header::before {{ content:"❖";font-size:14px;color:#2a8aa3; }}
.pub-card {{
    background:#ffffff;border:1.5px solid {CORES['card_border']};
    border-radius:16px;padding:20px;margin-bottom:18px;
}}
.pub-card-header {{ display:flex;align-items:center;gap:12px;margin-bottom:14px; }}
.pub-source-icon {{
    width:42px;height:42px;border-radius:50%;display:flex;
    align-items:center;justify-content:center;font-size:22px;flex-shrink:0;
}}
.pub-title {{ font-size:15px;font-weight:700;color:{CORES['ink']};line-height:1.35; }}
.pub-body {{
    font-size:13.5px;color:#2a2a2a;line-height:1.55;margin-bottom:14px;
    background:#f8f9fa;border-radius:8px;padding:10px 14px;
    border-left:3px solid {CORES['card_border']};font-style:italic;
}}
.pub-author {{ font-size:12px;color:#5b7083;text-align:right;margin-bottom:14px;font-weight:500; }}
.badge-row {{ display:flex;justify-content:space-between;align-items:center; }}
.pub-time {{ font-size:11.5px;color:#8a9baa;font-family:'JetBrains Mono',monospace; }}
</style>
""", unsafe_allow_html=True)

# ── FILTRAR ───────────────────────────────────────────────────────────────────
filtrados = [
    x for x in dados
    if x["fonte"] in filtro_fonte
    and x["sentimento_calc"] in filtro_sent
    and (not busca or busca.lower() in (
        str(x.get("titulo_feedback","")) + str(x.get("comentario_usuario",""))
    ).lower())
]

st.markdown("<div class='pub-section-header'>Publicações</div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:12px;color:#5b7083;margin-bottom:18px'>{len(filtrados)} publicações encontradas</div>", unsafe_allow_html=True)

if not filtrados:
    st.info("Nenhuma publicação encontrada com os filtros aplicados.")
else:
    col_esq, col_dir = st.columns(2)
    for i, item in enumerate(filtrados):
        fonte     = item.get("fonte", "?")
        titulo    = (item.get("titulo_feedback") or "Sem título").replace("\n"," ")[:80]
        corpo     = item.get("comentario_usuario") or ""
        sent      = item["sentimento_calc"]
        tempo     = item["tempo_rel"]
        url       = item.get("url", "#")
        avaliacao = item.get("avaliacao", "")
        icon      = get_fonte_icon(fonte)
        icon_bg   = get_fonte_bg(fonte)
        autor_raw = re.sub(r"^(Fonte:|Canal:|fonte:)", "", str(avaliacao)).strip() or "Anônimo"
        corpo_display = (corpo[:220] + "…") if len(corpo) > 220 else corpo

        card_html = f"""
        <div class="pub-card">
            <div class="pub-card-header">
                <div class="pub-source-icon" style="background:{icon_bg}">{icon}</div>
                <div class="pub-title">{titulo}</div>
            </div>
            <div class="pub-body">"{corpo_display}"</div>
            <div class="pub-author">~{autor_raw}</div>
            <div class="badge-row">
                {badge_html(sent)}
                <span class="pub-time">{tempo}</span>
            </div>
        </div>
        """
        target_col = col_esq if i % 2 == 0 else col_dir
        with target_col:
            st.markdown(card_html, unsafe_allow_html=True)
            if url and url != "#":
                st.markdown(
                    f"<div style='margin-top:-10px;margin-bottom:8px;text-align:right'>"
                    f"<a href='{url}' target='_blank' style='font-size:11px;color:#2a6066;text-decoration:none'>🔗 Ver original</a>"
                    f"</div>", unsafe_allow_html=True)