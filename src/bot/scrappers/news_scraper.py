import os
import requests


def coletar_noticias(query: str, limite: int = 50) -> list[dict]:
    """
    Busca artigos de notícias sobre `query` via NewsAPI.
    Requer: NEWS_API_KEY
    Plano grátis: 100 req/dia, apenas últimos 30 dias.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": min(limite, 100),
        "apiKey": os.environ["NEWS_API_TOKEN"],
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    artigos = resp.json().get("articles", [])

    resultados = []
    for a in artigos:
        resultados.append({
            "fonte": "NewsAPI",
            "alvo_coleta": query,
            "titulo_feedback": a.get("title", ""),
            "comentario_usuario": a.get("description") or a.get("content") or "",
            "avaliacao": f"Fonte: {a.get('source', {}).get('name', 'N/A')}",
            "url": a.get("url", ""),
            "data": (a.get("publishedAt") or "")[:10],
        })

    print(f"[NewsAPI] {len(resultados)} artigos coletados.")
    return resultados