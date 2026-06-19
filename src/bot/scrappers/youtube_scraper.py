"""Scraper de vídeos via YouTube Data API (OO)."""
from __future__ import annotations

import os

import requests

from ..models import Feedback
from .base_scraper import BaseScraper


class YoutubeScraper(BaseScraper):
    """Busca vídeos sobre `query` no YouTube e coleta título + descrição.

    Requer: YOUTUBE_API_KEY.
    """

    nome_fonte = "YouTube"
    limite_padrao = 30
    ENDPOINT = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self, query: str, limite: int | None = None, api_key: str | None = None):
        super().__init__(query, limite)
        self.api_key = api_key or os.environ.get("YOUTUBE_API_KEY", "")

    def _buscar_itens_brutos(self) -> list:
        params = {
            "part": "snippet",
            "q": self.query,
            "type": "video",
            "maxResults": min(self.limite, 50),
            "relevanceLanguage": "pt",
            "order": "date",
            "key": self.api_key,
        }
        resp = requests.get(self.ENDPOINT, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json().get("items", [])

    def _converter_item(self, item) -> Feedback | None:
        snippet = item.get("snippet", {})
        video_id = item.get("id", {}).get("videoId", "")
        return Feedback(
            fonte=self.nome_fonte,
            alvo_coleta=self.query,
            titulo=snippet.get("title", "") or "",
            comentario=snippet.get("description", "") or "",
            avaliacao=f"Canal: {snippet.get('channelTitle', 'N/A')}",
            url=f"https://youtube.com/watch?v={video_id}" if video_id else "",
            data=(snippet.get("publishedAt") or "")[:10],
        )


def coletar_youtube(query: str, limite: int = 30) -> list[dict]:
    """Função de compatibilidade: mantém a assinatura usada por código legado."""
    feedbacks = YoutubeScraper(query, limite).coletar()
    return [f.como_dict() for f in feedbacks]
