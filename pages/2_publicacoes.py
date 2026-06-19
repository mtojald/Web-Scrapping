"""Página Publicações do Atlas Insights."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

from src.ui.page import AtlasPage
from src.ui.components import PublicationCard


class PublicacoesPage(AtlasPage):
    NOME_PAGINA = "Publicações"

    def conteudo_extra_sidebar(self) -> None:
        self.busca = st.text_input("🔍 Buscar texto", placeholder="Palavra-chave...", key="busca_pub")
        sentimentos = self.colecao.sentimentos_presentes()
        self.sentimentos_selecionados = st.multiselect(
            "Sentimento", options=sentimentos, default=sentimentos, key="sent_pub",
        )

    def renderizar_conteudo(self) -> None:
        colecao = self.colecao_filtrada
        sentimentos = set(getattr(self, "sentimentos_selecionados", colecao.sentimentos_presentes()))
        colecao = colecao.filtrar_por_sentimento(sentimentos)
        busca = getattr(self, "busca", "")
        colecao = colecao.filtrar_por_busca(busca)

        st.markdown("<div class='pub-section-header'>Publicações</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:12px;color:#4a6b70;margin-bottom:18px'>"
            f"{colecao.total} publicações encontradas</div>",
            unsafe_allow_html=True,
        )

        if colecao.total == 0:
            st.info("Nenhuma publicação encontrada com os filtros aplicados.")
            return

        col_esq, col_dir = st.columns(2)
        for i, feedback in enumerate(colecao):
            destino = col_esq if i % 2 == 0 else col_dir
            with destino:
                PublicationCard(feedback).render()


PublicacoesPage().executar()
