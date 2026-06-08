from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

QUERY = os.getenv("SEARCH_QUERY", "SEBRAE")
DIR_RAIZ = Path.cwd()

# Garante que o diretório existe
(DIR_RAIZ / "src/JSON").mkdir(parents=True, exist_ok=True)

RESULTADO_PATH = DIR_RAIZ / "src/JSON/resultado_sebrae_local.json"

FONTES = {
    "reddit":  all(os.getenv(k) for k in ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"]),
    "news":    bool(os.getenv("NEWS_API_KEY")),
    "youtube": bool(os.getenv("YOUTUBE_API_KEY")),
    "apify":   bool(os.getenv("APIFY_API_TOKEN")),
}