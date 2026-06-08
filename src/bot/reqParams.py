from dotenv import load_dotenv
from pathlib import Path
import os

# Carrega variáveis do .env (se existir)
load_dotenv()

# Palavra-chave central de busca
QUERY = os.getenv("SEARCH_QUERY", "SEBRAE")
DIR_RAIZ=  Path.cwd()
RESULTADO_PATH = DIR_RAIZ / "src/JSON/reqPlataformas.json"

# Controle de quais fontes ativar (False = pula se a key não estiver configurada)
FONTES = {
    "reddit":  all(os.getenv(k) for k in ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"]),
    "news":    bool(os.getenv("NEWS_API_KEY")),
    "youtube": bool(os.getenv("YOUTUBE_API_KEY")),
    "apify":   bool(os.getenv("APIFY_API_TOKEN")),
}