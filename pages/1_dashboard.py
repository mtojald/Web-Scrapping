"""Página Dashboard do Atlas Insights."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import streamlit as st

from src.ui.page import AtlasPage
from src.ui.components import (
    MetricCard, GaugeBar, SentimentDonut, FeaturedPostCard, SourceBarChart, AtlasCard,
)


class DashboardPage(AtlasPage):
    NOME_PAGINA = "Dashboard"

    def renderizar_conteudo(self) -> None:
        colecao = self.colecao_filtrada
        rotulo_plataformas = (
            "todas as plataformas"
            if len(self.plataformas_ativas) == len(self.colecao.fontes_presentes())
            else ", ".join(sorted(self.plataformas_ativas))
        )
        self.cabecalho(
            "Dashboard",
            f"Análise de feedbacks e sentimentos · {colecao.total} registros · {rotulo_plataformas}",
        )

        # ── Linha de métricas ──────────────────────────────
        cols = st.columns(4)
        for col, metric in zip(cols, MetricCard.linha_padrao(colecao)):
            with col:
                metric.render()

        st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)

        # ── Linha de gráficos (cada card = UMA chamada a st.markdown) ──
        col_gauges, col_destaque, col_fontes = st.columns([1, 1.35, 1.25])

        with col_gauges:
            corpo = GaugeBar.html_de_colecao(colecao)
            AtlasCard("Índices", "NPS e CSAT", corpo).render()

        with col_destaque:
            destaque = colecao.ordenar_por_data().primeiro()
            corpo = FeaturedPostCard(destaque).to_html() + SentimentDonut(colecao).to_html()
            AtlasCard("Destaque do período", "Publicação mais recente", corpo).render()

        with col_fontes:
            corpo = SourceBarChart(colecao).to_html()
            AtlasCard("Sentimentos por fonte", "Canal de atendimento", corpo).render()

        # ── Tabela ──────────────────────────────────────────
        st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)
        AtlasCard("Feedbacks", "Registros coletados", "").render()
        registros = colecao.como_lista_dicts()
        if registros:
            df = pd.DataFrame(registros)
            colunas = ["fonte", "titulo_feedback", "comentario_usuario", "sentimento", "data"]
            colunas_ok = [c for c in colunas if c in df.columns]
            st.dataframe(df[colunas_ok].reset_index(drop=True), use_container_width=True, height=280)
        else:
            st.info("Nenhum registro para os filtros aplicados.")


DashboardPage().executar()
