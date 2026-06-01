import json
import os
import sys
from dotenv import load_dotenv

# Carrega variáveis do .env (se existir)
load_dotenv()

# Adiciona src ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from scrapers import coletar_reddit, coletar_noticias, coletar_youtube, coletar_apify

# Palavra-chave central de busca
QUERY = os.getenv("SEARCH_QUERY", "SEBRAE")
RESULTADO_PATH = "resultado_sebrae_local.json"

# Controle de quais fontes ativar (False = pula se a key não estiver configurada)
FONTES = {
    "reddit":  all(os.getenv(k) for k in ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"]),
    "news":    bool(os.getenv("NEWS_API_KEY")),
    "youtube": bool(os.getenv("YOUTUBE_API_KEY")),
    "apify":   bool(os.getenv("APIFY_API_TOKEN")),
}


def rodar_scraping():
    dados = []

    if FONTES["reddit"]:
        dados += coletar_reddit(QUERY, limite=50)
    else:
        print("[Reddit] Pulado — REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET não configurados.")

    if FONTES["news"]:
        dados += coletar_noticias(QUERY, limite=50)
    else:
        print("[NewsAPI] Pulado — NEWS_API_KEY não configurada.")

    if FONTES["youtube"]:
        dados += coletar_youtube(QUERY, limite=30)
    else:
        print("[YouTube] Pulado — YOUTUBE_API_KEY não configurada.")

    if FONTES["apify"]:
        dados += coletar_apify(QUERY, limite=30)
    else:
        print("[Apify] Pulado — APIFY_API_TOKEN não configurado.")

    if not dados:
        print("\nNenhuma fonte ativa. Configure as variáveis no arquivo .env")
        return

    with open(RESULTADO_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f"\n✅ {len(dados)} itens salvos em '{RESULTADO_PATH}'")


if __name__ == "__main__":
    rodar_scraping()