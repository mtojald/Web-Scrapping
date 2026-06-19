"""Classe base para todos os scrapers do projeto (Orientação a Objetos)."""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Feedback


class BaseScraper(ABC):
    """Define o contrato comum a todo scraper de plataforma.

    Subclasses devem implementar `_buscar_itens_brutos` (chamada de API) e
    `_converter_item` (mapeamento do item bruto para um `Feedback`).
    """

    nome_fonte: str = "Desconhecida"
    limite_padrao: int = 30

    def __init__(self, query: str, limite: int | None = None):
        self.query = query
        self.limite = limite or self.limite_padrao
        self._itens_brutos: list = []

    def coletar(self) -> list[Feedback]:
        """Template method: orquestra busca, conversão e log de resultado."""
        self._itens_brutos = self._buscar_itens_brutos()
        feedbacks = [self._converter_item(item) for item in self._itens_brutos]
        feedbacks = [f for f in feedbacks if f is not None]
        self._logar_resultado(len(feedbacks))
        return feedbacks

    @abstractmethod
    def _buscar_itens_brutos(self) -> list:
        """Executa a requisição à API/fonte e retorna itens crus."""
        raise NotImplementedError

    @abstractmethod
    def _converter_item(self, item) -> Feedback | None:
        """Converte um item bruto da fonte em um `Feedback`."""
        raise NotImplementedError

    def _logar_resultado(self, quantidade: int) -> None:
        print(f"[{self.nome_fonte}] {quantidade} itens coletados.")

    def __repr__(self) -> str:
        return f"<{type(self).__name__} query={self.query!r} limite={self.limite}>"
