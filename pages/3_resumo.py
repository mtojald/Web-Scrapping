import json
import re
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import requests
from datetime import datetime, date
from collections import defaultdict
import streamlit as st
import pages.sidebar as sidebar

CORES = sidebar.CORES

# ── CARREGAR DADOS ────────────────────────────────────────────────────────────
try:
    with open("src/JSON/resultado_sebrae_local.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
except FileNotFoundError:
    st.error("Arquivo não encontrado. Execute main.py primeiro.")
    st.stop()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
def sidebar_extra():
    if st.button("🔄 Regenerar análise", use_container_width=True):
        if "resumo_cache" in st.session_state:
            del st.session_state["resumo_cache"]

sidebar.render("Resumo", n_publicacoes=len(dados), extra_content=sidebar_extra)

# ── CSS EXTRA ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
.section-header {{
    display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700;
    color:#1d5a63;letter-spacing:0.04em;margin-bottom:16px;text-transform:uppercase;
}}
.section-header::before {{ content:"❖";font-size:14px;color:#2a8aa3; }}
.resumo-card {{
    background:{CORES['card']};border:1.5px solid {CORES['card_border']};
    border-radius:16px;padding:20px 22px;
}}
.resumo-card h4 {{ font-size:15px;font-weight:700;color:{CORES['ink']};margin:0 0 10px;line-height:1.3; }}
.resumo-card p {{ font-size:13.5px;color:#2a3f44;line-height:1.6;margin:0; }}
.intent-card {{
    background:{CORES['card']};border:1.5px solid {CORES['card_border']};
    border-radius:14px;padding:16px 18px;height:100%;
}}
.intent-card h5 {{ font-size:14px;font-weight:700;color:{CORES['ink']};margin:0 0 8px; }}
.intent-card p {{ font-size:12.5px;color:#3b5a60;line-height:1.5;margin:0; }}
.timeline-wrapper {{
    background:{CORES['card']};border:1.5px solid {CORES['card_border']};
    border-radius:16px;padding:24px 28px 20px;
}}
.empreendedor-card {{
    background:{CORES['card']};border:1.5px solid {CORES['card_border']};
    border-radius:16px;padding:22px;text-align:center;height:100%;
}}
.empreendedor-card h4 {{ font-size:14px;font-weight:700;color:{CORES['ink']};margin:0 0 12px; }}
.empreendedor-card p {{
    font-size:12.5px;color:#2a3f44;line-height:1.6;margin:0;
    font-style:italic;text-align:left;
}}
</style>
""", unsafe_allow_html=True)

# ── ANÁLISE ───────────────────────────────────────────────────────────────────
def preparar_contexto(dados):
    por_data = defaultdict(list)
    for item in dados:
        d = item.get("data", "sem_data")
        titulo = item.get("titulo_feedback") or ""
        corpo  = item.get("comentario_usuario") or ""
        por_data[d].append(f"{titulo} — {corpo}"[:200])
    linhas = []
    for dt in sorted(por_data.keys())[-7:]:
        linhas.append(f"\n[{dt}]")
        for t in por_data[dt][:5]:
            linhas.append(f"  • {t}")
    fontes = ", ".join(sorted(set(x["fonte"] for x in dados)))
    return f"Total: {len(dados)}\nFontes: {fontes}\n\nPublicações recentes:{''.join(linhas)}"

def chamar_claude(contexto):
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        return None
    prompt = f"""Você é analista de mídias sociais do SEBRAE. Analise as publicações e retorne APENAS JSON válido, sem markdown.

Dados:
{contexto}

JSON esperado:
{{
  "o_que_mudou": "2-3 frases sobre o que mudou esta semana (tom, volume, temas)",
  "intencoes": [
    {{"titulo": "Buscar X", "descricao": "frase curta"}},
    {{"titulo": "Buscar Y", "descricao": "frase curta"}},
    {{"titulo": "Buscar Z", "descricao": "frase curta"}}
  ],
  "timeline": [
    {{"dia": "Segunda", "evento": "descrição breve"}},
    {{"dia": "Quarta",  "evento": "descrição breve"}},
    {{"dia": "Sexta",   "evento": "descrição breve"}}
  ],
  "empreendedor": {{
    "perfil": "Tipo de empreendedor (setor)",
    "descricao": "2-3 frases sobre frustrações, comportamentos e canais usados"
  }}
}}"""
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"},
        json={"model":"claude-sonnet-4-20250514","max_tokens":1000,
              "messages":[{"role":"user","content":prompt}]},
        timeout=30,
    )
    resp.raise_for_status()
    texto = resp.json()["content"][0]["text"]
    texto = re.sub(r"```(?:json)?|```","",texto).strip()
    return json.loads(texto)

def analise_fallback(dados):
    por_data = defaultdict(list)
    for item in dados:
        por_data[item.get("data","")].append(item)
    dias_semana = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
    timeline = []
    for dt in sorted(por_data.keys())[-3:]:
        try:
            d = datetime.strptime(dt,"%Y-%m-%d")
            dia_nome = dias_semana[d.weekday()]
        except Exception:
            dia_nome = dt
        items_dia = por_data[dt]
        titulos = [x.get("titulo_feedback") or x.get("comentario_usuario","")[:60] for x in items_dia[:2]]
        evento = "; ".join(t for t in titulos if t)[:120] or "Publicações coletadas neste dia."
        timeline.append({"dia": dia_nome, "evento": evento})
    fontes = sorted(set(x["fonte"] for x in dados))
    return {
        "o_que_mudou": (
            f"Foram coletadas {len(dados)} publicações de {', '.join(fontes)} sobre o SEBRAE. "
            "O volume indica atividade constante, com predominância de temas relacionados a capacitação e empreendedorismo."
        ),
        "intencoes": [
            {"titulo":"Buscar Capacitação","descricao":"Usuários buscando cursos, oficinas e materiais de apoio do SEBRAE."},
            {"titulo":"Buscar Informação","descricao":"Empreendedores pesquisando sobre MEI, crédito e regularização de negócios."},
            {"titulo":"Buscar Validação","descricao":"Usuários compartilhando experiências para validar decisões de negócio."},
        ],
        "timeline": timeline or [
            {"dia":"Seg","evento":"Início da semana com publicações sobre capacitação."},
            {"dia":"Qua","evento":"Pico de interações sobre crédito e financiamento."},
            {"dia":"Sex","evento":"Conteúdos de empreendedorismo digital."},
        ],
        "empreendedor": {
            "perfil": "Microempreendedor Iniciante (setor de Serviços)",
            "descricao": "Pequeno empreendedor em fase de formalização. Busca respostas rápidas sobre MEI e crédito. Usa redes sociais e YouTube para aprender sobre gestão do negócio.",
        },
    }

# ── GERAR / CACHEAR ───────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>Resumo</div>", unsafe_allow_html=True)

if "resumo_cache" not in st.session_state:
    with st.spinner("Gerando análise..."):
        contexto = preparar_contexto(dados)
        api_key  = os.getenv("ANTHROPIC_API_KEY","")
        if api_key:
            try:
                analise = chamar_claude(contexto)
                fonte_label = "✨ Análise gerada por IA"
            except Exception as e:
                analise = analise_fallback(dados)
                fonte_label = f"⚠️ Fallback (erro na API: {e})"
        else:
            analise = analise_fallback(dados)
            fonte_label = "ℹ️ Análise automática (sem ANTHROPIC_API_KEY)"
        st.session_state["resumo_cache"] = analise
        st.session_state["resumo_fonte"] = fonte_label
else:
    analise     = st.session_state["resumo_cache"]
    fonte_label = st.session_state.get("resumo_fonte","")

st.markdown(f"<div style='font-size:11px;color:#5b8080;margin-bottom:14px'>{fonte_label}</div>", unsafe_allow_html=True)

# ── LINHA 1: O que mudou + Intenções ─────────────────────────────────────────
col_mudou, col_intencoes = st.columns([1.1, 2])

with col_mudou:
    st.markdown(f"""
    <div class="resumo-card" style="min-height:160px">
        <h4>O que mudou nesta semana?<br>
        <span style="font-weight:400;font-size:13px">(em relação à semana passada)</span></h4>
        <p>{analise.get('o_que_mudou','')}</p>
    </div>
    """, unsafe_allow_html=True)

with col_intencoes:
    st.markdown(f"""
    <div style="background:{CORES['card']};border:1.5px solid {CORES['card_border']};
                border-radius:16px;padding:18px 20px;">
        <div style="font-size:15px;font-weight:700;color:{CORES['ink']};
                    margin-bottom:14px;text-align:center">
            O que o usuário quis esta semana?
        </div>
    """, unsafe_allow_html=True)
    intencoes = analise.get("intencoes", [])
    if intencoes:
        cols_int = st.columns(len(intencoes))
        for i, intencao in enumerate(intencoes):
            with cols_int[i]:
                st.markdown(f"""
                <div class="intent-card">
                    <h5>{intencao.get('titulo','')}</h5>
                    <p>{intencao.get('descricao','')}</p>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top:18px'/>", unsafe_allow_html=True)

# ── LINHA 2: Timeline + Empreendedor ─────────────────────────────────────────
col_timeline, col_emp = st.columns([2, 1])

with col_timeline:
    timeline = analise.get("timeline", [])
    st.markdown("<div class='timeline-wrapper'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:16px;font-weight:700;color:{CORES['ink']};margin-bottom:28px'>Linha do tempo</div>", unsafe_allow_html=True)
    if timeline:
        cols_tl = st.columns(len(timeline))
        for i, evento in enumerate(timeline):
            with cols_tl[i]:
                st.markdown(f"""
                <div style="display:flex;flex-direction:column;align-items:center">
                    <div style="font-size:14px;font-weight:700;color:{CORES['ink']};margin-bottom:10px">
                        {evento.get('dia','')}
                    </div>
                    <div style="width:16px;height:16px;border-radius:50%;background:{CORES['ink']};
                                border:3px solid {CORES['bg']};margin-bottom:16px;flex-shrink:0"></div>
                    <div style="background:white;border:1px solid {CORES['card_border']};border-radius:10px;
                                padding:10px 12px;font-size:11.5px;color:#2a3f44;line-height:1.45;
                                text-align:center;max-width:180px">
                        {evento.get('evento','')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown(f"<div style='height:3px;background:{CORES['ink']};border-radius:2px;margin-top:-110px;margin-bottom:10px'></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_emp:
    emp = analise.get("empreendedor", {})
    st.markdown(f"""
    <div class="empreendedor-card">
        <div style="font-size:14px;font-weight:700;color:{CORES['ink']};margin-bottom:14px">
            Empreendedor da semana
        </div>
        <div style="width:80px;height:80px;border-radius:50%;
                    background:linear-gradient(135deg,#6bafc6,#2a6b7c);
                    display:flex;align-items:center;justify-content:center;
                    font-size:36px;margin:0 auto 14px;border:3px solid white">🧑‍💼</div>
        <h4>{emp.get('perfil','')}</h4>
        <p>"{emp.get('descricao','')}"</p>
    </div>
    """, unsafe_allow_html=True)