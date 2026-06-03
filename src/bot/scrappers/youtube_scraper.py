import os
import requests


def coletar_youtube(query: str, limite: int = 30) -> list[dict]:
    """
    Busca vídeos sobre `query` no YouTube e coleta título + descrição.
    Requer: YOUTUBE_API_KEY
    """
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": min(limite, 50),
        "relevanceLanguage": "pt",
        "order": "date",
        "key": os.environ["YOUTUBE_API_KEY"],
    }

    resp = requests.get(search_url, params=params, timeout=10)
    resp.raise_for_status()
    items = resp.json().get("items", [])

    resultados = []
    for item in items:
        snippet = item.get("snippet", {})
        video_id = item.get("id", {}).get("videoId", "")
        resultados.append({
            "fonte": "YouTube",
            "alvo_coleta": query,
            "titulo_feedback": snippet.get("title", ""),
            "comentario_usuario": snippet.get("description", ""),
            "avaliacao": f"Canal: {snippet.get('channelTitle', 'N/A')}",
            "url": f"https://youtube.com/watch?v={video_id}",
            "data": (snippet.get("publishedAt") or "")[:10],
        })

    print(f"[YouTube] {len(resultados)} vídeos coletados.")
    return resultados