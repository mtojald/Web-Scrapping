"""Classe base de página (Template Method) para as páginas Streamlit."""
from __future__ import annotations

import json
from abc import ABC, abstractmethod

import streamlit as st

from .sidebar import AtlasSidebar
from ..bot.models import FeedbackCollection
from ..bot.reqParams import RESULTADO_PATH


class AtlasPage(ABC):
    """Esqueleto comum a todas as páginas: carregar dados, sidebar, filtrar, render."""

    NOME_PAGINA: str = "Página"
    CAMINHO_DADOS = RESULTADO_PATH

    def __init__(self):
        self.colecao: FeedbackCollection = self._carregar_dados()
        self.plataformas_ativas: set[str] = set()
        self.colecao_filtrada: FeedbackCollection = self.colecao

    def _carregar_dados(self) -> FeedbackCollection:
        if "dados_scraping" in st.session_state:
            lista = st.session_state["dados_scraping"]
            return FeedbackCollection.de_lista_dicts(lista)
        try:
            with open(self.CAMINHO_DADOS, "r", encoding="utf-8") as f:
                lista = json.load(f)
            return FeedbackCollection.de_lista_dicts(lista)
        except FileNotFoundError:
            st.error("Arquivo de dados não encontrado. Execute main.py primeiro.")
            st.stop()
            return FeedbackCollection()

    def _renderizar_sidebar(self) -> None:
        sidebar = AtlasSidebar(self.NOME_PAGINA, self.colecao)
        self.plataformas_ativas = sidebar.renderizar(extra_content=self.conteudo_extra_sidebar)
        self.colecao_filtrada = self.colecao.filtrar_por_fonte(self.plataformas_ativas)

    def conteudo_extra_sidebar(self) -> None:
        """Hook opcional: subclasses podem sobrescrever para adicionar controles próprios."""
        return None

    def cabecalho(self, titulo: str, subtitulo: str) -> None:
        st.markdown(f"""
        <div class="eyebrow">Atlas Insights · SEBRAE</div>
        <div class="page-title">{titulo}</div>
        <div class="page-subtitle">{subtitulo}</div>
        """, unsafe_allow_html=True)

    @abstractmethod
    def renderizar_conteudo(self) -> None:
        """Implementado por cada página concreta."""
        raise NotImplementedError

    def executar(self) -> None:
        """Template method: ordem fixa de execução da página."""
        self._renderizar_sidebar()
        self.renderizar_conteudo()
