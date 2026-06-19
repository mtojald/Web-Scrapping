"""Scraper de notícias via NewsAPI (OO)."""
from __future__ import annotations

import os

import requests

from ..models import Feedback
from .base_scraper import BaseScraper


class NewsScraper(BaseScraper):
    """Busca artigos de notícias sobre `query` via NewsAPI.

    Requer: NEWS_API_TOKEN (ou NEWS_API_KEY).
    Plano grátis: 100 req/dia, apenas últimos 30 dias.
    """

    nome_fonte = "NewsAPI"
    limite_padrao = 50
    ENDPOINT = "https://newsapi.org/v2/everything"

    def __init__(self, query: str, limite: int | None = None, api_key: str | None = None):
        super().__init__(query, limite)
        self.api_key = api_key or os.getenv("NEWS_API_TOKEN") or os.environ.get("NEWS_API_KEY", "")

    def _buscar_itens_brutos(self) -> list:
        params = {
            "q": self.query,
            "language": "pt",
            "sortBy": "publishedAt",
            "pageSize": min(self.limite, 100),
            "apiKey": self.api_key,
        }
        resp = requests.get(self.ENDPOINT, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json().get("articles", [])

    def _converter_item(self, item) -> Feedback | None:
        fonte_nome = item.get("source", {}).get("name", "N/A")
        return Feedback(
            fonte=self.nome_fonte,
            alvo_coleta=self.query,
            titulo=item.get("title", "") or "",
            comentario=item.get("description") or item.get("content") or "",
            avaliacao=f"Fonte: {fonte_nome}",
            url=item.get("url", "") or "",
            data=(item.get("publishedAt") or "")[:10],
        )


def coletar_noticias(query: str, limite: int = 50) -> list[dict]:
    """Função de compatibilidade: mantém a assinatura usada por código legado."""
    feedbacks = NewsScraper(query, limite).coletar()
    return [f.como_dict() for f in feedbacks]
