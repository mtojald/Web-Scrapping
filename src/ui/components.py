"""Componentes visuais reutilizaveis do Atlas Insights (OO).

Cada componente expoe `to_html()`, que retorna a string HTML pronta,
e `render()`, um atalho que injeta esse HTML via `st.markdown`.
Paginas que precisam combinar varios componentes dentro do mesmo
card (mesma <div>) devem usar `to_html()` e concatenar em UMA unica
chamada a `st.markdown` -- abrir/fechar uma div em chamadas separadas
nao e seguro no Streamlit.
"""
from __future__ import annotations

import streamlit as st

from ..bot.models import Feedback, FeedbackCollection, SOURCE_META


class MetricCard:
    """Um cartao de metrica do topo do Dashboard."""

    def __init__(self, label: str, value: str, delta: str = "", delta_color: str = "#4a6b70"):
        self.label = label
        self.value = value
        self.delta = delta
        self.delta_color = delta_color

    def to_html(self) -> str:
        return (
            '<div class="metric-card">'
            f'<div class="metric-label">{self.label}</div>'
            f'<div class="metric-value">{self.value}</div>'
            f'<div class="metric-delta" style="color:{self.delta_color}">{self.delta}</div>'
            '</div>'
        )

    def render(self) -> None:
        st.markdown(self.to_html(), unsafe_allow_html=True)

    @classmethod
    def linha_padrao(cls, colecao: FeedbackCollection) -> list["MetricCard"]:
        """Constroi a linha de 4 metricas a partir de uma FeedbackCollection."""
        total = colecao.total
        pos, neg = colecao.positivos, colecao.criticos
        pct_pos, pct_neg = colecao.percentual_positivo, colecao.percentual_critico
        media = colecao.media_estrelas if total else None
        return [
            cls("Total de feedbacks", f"{total}", "registros coletados", "#4a6b70"),
            cls("Positivos", f"{pos}", f"\u25b2 {pct_pos}%", "#1c7f54"),
            cls("Negativos", f"{neg}", f"\u25bc {pct_neg}%", "#b8362b"),
            cls("Media geral", f"{media:.1f} \u2605" if media else "-", "", "#4a6b70"),
        ]


class GaugeBar:
    """Indicador horizontal estilo barra (NPS/CSAT), como no design Atlas."""

    def __init__(self, label: str, valor: int):
        self.label = label
        self.valor = max(0, min(100, valor))

    @property
    def cor(self) -> str:
        if self.valor >= 60:
            return "#1c7f54"
        if self.valor >= 40:
            return "#c28a00"
        return "#b8362b"

    def to_html(self) -> str:
        return (
            '<div class="gauge-row">'
            f'<div class="gauge-label">{self.label}</div>'
            '<div style="display:flex;align-items:center;gap:10px">'
            f'<div class="gauge-track"><div class="gauge-fill" style="width:{self.valor}%;background:{self.cor}"></div></div>'
            f'<div style="font-size:18px;font-weight:700;color:#0f2027;min-width:40px;text-align:right">{self.valor}%</div>'
            '</div>'
            '</div>'
        )

    def render(self) -> None:
        st.markdown(self.to_html(), unsafe_allow_html=True)

    @classmethod
    def de_colecao(cls, colecao: FeedbackCollection) -> list["GaugeBar"]:
        return [cls("Indice NPS", colecao.nps), cls("Indice CSAT", colecao.csat)]

    @classmethod
    def html_de_colecao(cls, colecao: FeedbackCollection) -> str:
        return "".join(g.to_html() for g in cls.de_colecao(colecao))


class SentimentDonut:
    """Donut de sentimentos (CSS puro, sem dependencia de libs de grafico)."""

    def __init__(self, colecao: FeedbackCollection):
        self.colecao = colecao

    def to_html(self) -> str:
        c = self.colecao
        pos, neu, crit = c.percentual_positivo, c.percentual_neutro, c.percentual_critico
        fim_pos = pos
        fim_neu = pos + neu
        gradiente = (
            f"conic-gradient(#1c7f54 0% {fim_pos}%, #c28a00 {fim_pos}% {fim_neu}%, "
            f"#b8362b {fim_neu}% 100%)"
        )
        legenda = [
            ("Positivo", "#1c7f54", pos),
            ("Neutro",   "#c28a00", neu),
            ("Critico",  "#b8362b", crit),
        ]
        itens_legenda = "".join(
            '<div style="display:flex;align-items:center;gap:6px">'
            f'<div style="width:10px;height:10px;border-radius:50%;background:{cor};flex-shrink:0"></div>'
            f'<span style="color:#4a6b70">{rotulo}</span>'
            f'<b style="color:#0f2027;margin-left:auto">{pct}%</b>'
            '</div>'
            for rotulo, cor, pct in legenda
        )

        return (
            '<div style="margin-top:14px;display:flex;align-items:center;gap:16px">'
            f'<div style="width:90px;height:90px;border-radius:50%;flex-shrink:0;background:{gradiente};'
            'display:flex;align-items:center;justify-content:center">'
            '<div style="width:56px;height:56px;border-radius:50%;background:#fff"></div>'
            '</div>'
            f'<div style="display:flex;flex-direction:column;gap:5px;font-size:12px">{itens_legenda}</div>'
            '</div>'
        )

    def render(self) -> None:
        st.markdown(self.to_html(), unsafe_allow_html=True)


class FeaturedPostCard:
    """Card de destaque com a publicacao mais recente."""

    def __init__(self, feedback: Feedback | None):
        self.feedback = feedback

    def to_html(self) -> str:
        if self.feedback is None:
            return "<div class='post-card'>Nenhuma publicacao disponivel.</div>"
        f = self.feedback
        return (
            '<div class="post-card">'
            '<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px">'
            f'<div class="post-avatar">{f.icone_fonte}</div>'
            f'<div><div class="post-title">{f.titulo[:70] or "Sem titulo"}</div>'
            f'<div class="post-meta">{f.fonte} &middot; {f.data or "-"}</div></div>'
            '</div>'
            f'<div class="post-body">{f.corpo_resumido(180)}</div>'
            '<div class="post-stats">'
            f'<span>{f.avaliacao or "-"}</span>'
            f'<span>Sentimento: <b>{f.sentimento}</b></span>'
            '</div>'
            '</div>'
        )

    def render(self) -> None:
        st.markdown(self.to_html(), unsafe_allow_html=True)


class SourceBarChart:
    """Barras horizontais de contagem por fonte (CSS puro)."""

    def __init__(self, colecao: FeedbackCollection):
        self.colecao = colecao

    def to_html(self) -> str:
        contagem = self.colecao.contagem_por_fonte()
        if not contagem:
            return "<div style='font-size:12px;color:#4a6b70'>Sem dados.</div>"
        maximo = max(contagem.values()) or 1
        linhas = []
        for fonte, total in sorted(contagem.items(), key=lambda kv: -kv[1]):
            cor = SOURCE_META.get(fonte, {}).get("color", "#1a5060")
            largura = round(total / maximo * 95)
            linhas.append(
                '<div class="bar-row">'
                '<div style="display:flex;justify-content:space-between;margin-bottom:3px">'
                f'<span style="font-size:11px;color:#4a6b70;font-family:\'JetBrains Mono\',monospace">{fonte}</span>'
                f'<span style="font-size:11px;color:#0f2027;font-weight:600">{total}</span>'
                '</div>'
                f'<div class="bar-track"><div class="bar-fill" style="width:{largura}%;background:{cor}"></div></div>'
                '</div>'
            )
        return "".join(linhas)

    def render(self) -> None:
        st.markdown(self.to_html(), unsafe_allow_html=True)


class AtlasCard:
    """Wrapper generico de card (titulo + mono-subtitulo + corpo HTML ja pronto)."""

    def __init__(self, titulo: str, subtitulo: str, corpo_html: str, extra_style: str = ""):
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.corpo_html = corpo_html
        self.extra_style = extra_style

    def to_html(self) -> str:
        return (
            f'<div class="atlas-card" style="{self.extra_style}">'
            f'<h4>{self.titulo}</h4>'
            f'<div class="mono">{self.subtitulo}</div>'
            f'{self.corpo_html}'
            '</div>'
        )

    def render(self) -> None:
        st.markdown(self.to_html(), unsafe_allow_html=True)


class PublicationCard:
    """Card de publicacao usado na pagina de Publicacoes."""

    def __init__(self, feedback: Feedback):
        self.feedback = feedback

    def to_html(self) -> str:
        f = self.feedback
        estilo = f.estilo_sentimento
        return f"""
        <div class="pub-card">
            <div class="pub-card-header">
                <div class="pub-source-icon" style="background:{f.cor_fonte}">{f.icone_fonte}</div>
                <div class="pub-title">{(f.titulo or "Sem titulo")[:80]}</div>
            </div>
            <div class="pub-body">"{f.corpo_resumido(220)}"</div>
            <div class="badge-row">
                <span style="background:{estilo['bg']};color:{estilo['fg']};border:1.5px solid {estilo['border']};
                            border-radius:50px;padding:7px 18px;font-size:13px;font-weight:700;
                            display:inline-flex;align-items:center;gap:6px">{f.sentimento}</span>
                <span class="pub-time">{f.tempo_relativo}</span>
            </div>
        </div>
        """

    def to_html_com_link(self) -> str:
        html = self.to_html()
        f = self.feedback
        if f.url:
            html += (
                f"<div style='margin-top:-10px;margin-bottom:8px;text-align:right'>"
                f"<a href='{f.url}' target='_blank' style='font-size:11px;color:#1a5060;"
                f"text-decoration:none'>Ver original</a></div>"
            )
        return html

    def render(self) -> None:
        st.markdown(self.to_html_com_link(), unsafe_allow_html=True)


class IntentCard:
    """Card de 'intencao do usuario' usado na pagina de Resumo."""

    def __init__(self, numero: str, titulo: str, descricao: str):
        self.numero = numero
        self.titulo = titulo
        self.descricao = descricao

    def to_html(self) -> str:
        return f"""
        <div class="intent-card">
            <div class="intent-num">{self.numero}</div>
            <div class="intent-title">{self.titulo}</div>
            <div class="intent-desc">{self.descricao}</div>
        </div>
        """

    def render(self) -> None:
        st.markdown(self.to_html(), unsafe_allow_html=True)


class TimelineEvent:
    """Um ponto na linha do tempo do Resumo semanal."""

    def __init__(self, dia: str, evento: str):
        self.dia = dia
        self.evento = evento

    def to_html(self) -> str:
        return f"""
        <div style="display:flex;flex-direction:column;align-items:center;padding:0 8px">
            <div class="timeline-chip">{self.dia}</div>
            <div class="timeline-dot"></div>
            <div class="timeline-event">{self.evento}</div>
        </div>
        """

    def render(self) -> None:
        st.markdown(self.to_html(), unsafe_allow_html=True)


class EntrepreneurOfWeekCard:
    """Card do 'Empreendedor da semana' no Resumo."""

    def __init__(self, perfil: str, descricao: str):
        self.perfil = perfil
        self.descricao = descricao

    def to_html(self) -> str:
        return f"""
        <div class="atlas-card" style="text-align:center">
            <div class="mono" style="margin-bottom:16px">Empreendedor da semana</div>
            <div class="empreendedor-avatar">&#129489;&#8205;&#128188;</div>
            <div style="font-size:14px;font-weight:700;color:#0f2027;margin-bottom:4px">{self.perfil}</div>
            <div class="mono" style="margin-bottom:16px">Perfil identificado</div>
            <p style="font-size:12.5px;color:#2a3f44;line-height:1.6;text-align:left;font-style:italic">
                "{self.descricao}"
            </p>
        </div>
        """

    def render(self) -> None:
        st.markdown(self.to_html(), unsafe_allow_html=True)