"""Scraper genérico via Apify (Google Search Scraper) (OO)."""
from __future__ import annotations

import os
import time

import requests

from ..models import Feedback
from .base_scraper import BaseScraper


class ApifyScraper(BaseScraper):
    """Aciona o Google Search Scraper do Apify para buscar `query`.

    Requer: APIFY_API_TOKEN.
    """

    nome_fonte = "Apify"
    limite_padrao = 30
    ACTOR_ID = "apify~google-search-scraper"
    BASE_URL = "https://api.apify.com/v2"
    POLL_INTERVALO_S = 10
    POLL_TENTATIVAS = 18

    def __init__(self, query: str, limite: int | None = None, token: str | None = None):
        super().__init__(query, limite)
        self.token = token or os.environ.get("APIFY_API_TOKEN", "")

    def _iniciar_run(self) -> str:
        resp = requests.post(
            f"{self.BASE_URL}/acts/{self.ACTOR_ID}/runs",
            params={"token": self.token},
            json={
                "queries": self.query,
                "maxPagesPerQuery": 1,
                "resultsPerPage": min(self.limite, 10),
                "languageCode": "pt-BR",
                "countryCode": "br",
            },
            timeout=30,
        )
        resp.raise_for_status()
        run_id = resp.json()["data"]["id"]
        print(f"[{self.nome_fonte}] Run iniciado: {run_id}. Aguardando conclusão...")
        return run_id

    def _esperar_conclusao(self, run_id: str) -> str:
        for _ in range(self.POLL_TENTATIVAS):
            time.sleep(self.POLL_INTERVALO_S)
            status_resp = requests.get(
                f"{self.BASE_URL}/actor-runs/{run_id}",
                params={"token": self.token},
                timeout=10,
            )
            status_resp.raise_for_status()
            dados = status_resp.json()["data"]
            if dados["status"] == "SUCCEEDED":
                return dados["defaultDatasetId"]
            if dados["status"] in ("FAILED", "ABORTED", "TIMED-OUT"):
                raise RuntimeError(f"[{self.nome_fonte}] Run falhou com status: {dados['status']}")
        raise TimeoutError(f"[{self.nome_fonte}] Run demorou mais que o esperado.")

    def _buscar_itens_brutos(self) -> list:
        if not self.token:
            return []
        run_id = self._iniciar_run()
        dataset_id = self._esperar_conclusao(run_id)
        items_resp = requests.get(
            f"{self.BASE_URL}/datasets/{dataset_id}/items",
            params={"token": self.token, "limit": self.limite},
            timeout=30,
        )
        items_resp.raise_for_status()
        itens = items_resp.json()
        # cada item pode conter uma lista "organicResults"
        brutos = []
        for item in itens:
            brutos.extend(item.get("organicResults", [item]))
        return brutos

    def _converter_item(self, item) -> Feedback | None:
        return Feedback(
            fonte=self.nome_fonte,
            alvo_coleta=self.query,
            titulo=item.get("title") or "",
            comentario=item.get("description") or item.get("snippet") or "",
            avaliacao=f"Posição: {item.get('position') or 'N/A'}",
            url=item.get("url") or "",
            data=(item.get("date") or "")[:10],
        )


class ReclameAquiScraper(ApifyScraper):
    """Variante do ApifyScraper apontada para o ator de Reclame Aqui."""

    nome_fonte = "ReclameAqui"
    ACTOR_ID = "NBbFLTa9dAVtyOdt5"

    def _iniciar_run(self) -> str:
        resp = requests.post(
            f"{self.BASE_URL}/acts/{self.ACTOR_ID}/runs",
            params={"token": self.token},
            json={
                "companies": [self.query.lower()],
                "includeCompanyStats": True,
                "maxComplaints": self.limite,
                "proxyConfiguration": {"useApifyProxy": True, "apifyProxyGroups": []},
                "statusFilter": "all",
            },
            timeout=30,
        )
        resp.raise_for_status()
        run_id = resp.json()["data"]["id"]
        print(f"[{self.nome_fonte}] Run iniciado: {run_id}. Aguardando conclusão...")
        return run_id

    def _buscar_itens_brutos(self) -> list:
        if not self.token:
            return []
        run_id = self._iniciar_run()
        dataset_id = self._esperar_conclusao(run_id)
        items_resp = requests.get(
            f"{self.BASE_URL}/datasets/{dataset_id}/items",
            params={"token": self.token, "limit": self.limite},
            timeout=30,
        )
        items_resp.raise_for_status()
        return items_resp.json()

    def _converter_item(self, item) -> Feedback | None:
        if not isinstance(item, dict):
            return None
        return Feedback(
            fonte=self.nome_fonte,
            alvo_coleta=self.query,
            titulo=item.get("title", "") or "",
            comentario=item.get("description") or item.get("complaint", "") or "",
            avaliacao=item.get("rating", "") or "",
            url=item.get("url", "") or "",
            data=(item.get("date") or "")[:10],
        )


def coletar_apify(query: str, limite: int = 30) -> list[dict]:
    """Função de compatibilidade: mantém a assinatura usada por código legado."""
    feedbacks = ApifyScraper(query, limite).coletar()
    return [f.como_dict() for f in feedbacks]
