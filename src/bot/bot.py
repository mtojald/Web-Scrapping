"""Orquestrador dos scrapers (OO)."""
from __future__ import annotations

import json
import sys

from .reqParams import RESULTADO_PATH, QUERY
from .models import FeedbackCollection
from .scrappers.base_scraper import BaseScraper
from .scrappers.news_scraper import NewsScraper
from .scrappers.youtube_scraper import YoutubeScraper
from .scrappers.reddit_scraper import RedditScraper
from .scrappers.apify_scraper import ApifyScraper


class ScrapBot:
    """Coordena a execução de um ou mais scrapers e consolida os resultados."""

    # Registro de plataformas disponíveis: nome usado na CLI -> classe scraper
    REGISTRO_SCRAPERS: dict[str, type[BaseScraper]] = {
        "news": NewsScraper,
        "youtube": YoutubeScraper,
        "reddit": RedditScraper,
        "apify": ApifyScraper,
    }

    def __init__(self, query: str = QUERY, arguments: list[str] | None = None):
        self.query = query
        self.arguments = arguments if arguments is not None else sys.argv
        self._scrapers: list[BaseScraper] = []

    def registrar_scraper(self, scraper: BaseScraper) -> "ScrapBot":
        """Permite adicionar scrapers customizados em tempo de execução."""
        self._scrapers.append(scraper)
        return self

    def _criar_scraper(self, nome_plataforma: str) -> BaseScraper | None:
        classe = self.REGISTRO_SCRAPERS.get(nome_plataforma)
        return classe(self.query) if classe else None

    def coletar_tudo(self) -> FeedbackCollection:
        """Executa News e YouTube em sequência (fontes que não exigem polling longo)."""
        colecao = FeedbackCollection()
        for nome in ("news", "youtube"):
            scraper = self._criar_scraper(nome)
            if scraper:
                colecao = colecao.estender(scraper.coletar())
        return colecao

    def scrappersEmSeq(self) -> list[dict]:
        """Mantido por compatibilidade: retorna lista de dicts (formato legado)."""
        return self.coletar_tudo().como_lista_dicts()

    def coletar_plataformas(self, nomes: list[str]) -> FeedbackCollection:
        colecao = FeedbackCollection()
        for nome in nomes:
            scraper = self._criar_scraper(nome)
            if scraper:
                colecao = colecao.estender(scraper.coletar())
            else:
                print(f"\nFonte '{nome}' desconhecida ou não configurada.")
        return colecao

    def rodar_scraping(self) -> None:
        """Ponto de entrada usado pelo main.py (CLI)."""
        if len(self.arguments) <= 1:
            print("\nNenhuma fonte ativa. Configure as variáveis no arquivo .env")
            return

        if self.arguments[1] == "all":
            colecao = self.coletar_tudo()
        else:
            colecao = self.coletar_plataformas(self.arguments[1:])

        with open(RESULTADO_PATH, "a", encoding="utf-8") as f:
            json.dump(colecao.como_lista_dicts(), f, indent=4, ensure_ascii=False)

        print(f"\n✅ {len(colecao)} itens salvos em '{RESULTADO_PATH}'")


# Alias para compatibilidade com código antigo que importava `scrapBot`
scrapBot = ScrapBot
