import os
import requests
import time

ACTOR_ID = "apify~google-search-scraper"


def coletar_apify(query: str, limite: int = 30) -> list[dict]:
    """
    Aciona o Google Search Scraper do Apify.
    Requer: APIFY_API_TOKEN
    """
    token = os.environ["APIFY_API_TOKEN"]
    base = "https://api.apify.com/v2"

    run_resp = requests.post(
        f"{base}/acts/{ACTOR_ID}/runs",
        params={"token": token},
        json={
            "queries": query,
            "maxPagesPerQuery": 1,
            "resultsPerPage": min(limite, 10),
            "languageCode": "pt",
            "countryCode": "br",
        },
        timeout=30,
    )
    
    run_resp.raise_for_status()
    run_id = run_resp.json()["data"]["id"]
    print(f"[Apify] Run iniciado: {run_id}. Aguardando conclusão...")

    for _ in range(18):
        time.sleep(10)
        status_resp = requests.get(
            f"{base}/actor-runs/{run_id}",
            params={"token": token},
            timeout=10,
        )
        status = status_resp.json()["data"]["status"]
        if status == "SUCCEEDED":
            break
        if status in ("FAILED", "ABORTED", "TIMED-OUT"):
            raise RuntimeError(f"[Apify] Run falhou com status: {status}")
    else:
        raise TimeoutError("[Apify] Run demorou mais de 3 minutos.")

    dataset_id = status_resp.json()["data"]["defaultDatasetId"]
    items_resp = requests.get(
        f"{base}/datasets/{dataset_id}/items",
        params={"token": token, "limit": limite},
        timeout=30,
    )
    items_resp.raise_for_status()
    items = items_resp.json()

    resultados = []
    for item in items:
        # cada item tem uma lista "organicResults"
        for r in item.get("organicResults", [item]):
            resultados.append({
                "fonte": "Apify",
                "alvo_coleta": query,
                "titulo_feedback": r.get("title") or "",
                "comentario_usuario": r.get("description") or r.get("snippet") or "",
                "avaliacao": f"Posição: {r.get('position') or 'N/A'}",
                "url": r.get("url") or "",
                "data": (r.get("date") or "")[:10],
            })

    print(f"[Apify] {len(resultados)} itens coletados.")
    return resultados