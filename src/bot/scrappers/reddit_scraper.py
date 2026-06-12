import os
import requests
import time

ACTOR_ID = "aaSw38cTypQmjF6Au"
APIFY_QUERY = "SEBRAE"

def coletar_reddit(query: str, limite: int = 50) -> list[dict]:
    """
    Aciona o Reclame Aqui Scraper - Consumer Complaints BR do Apify.
    Requer: APIFY_API_TOKEN
    """
    
    token = os.environ["APIFY_API_TOKEN"]
    base = "https://api.apify.com/v2"

    run_resp = requests.post(
        f"{base}/acts/{ACTOR_ID}/runs",
        params={"token": token},
        json={
            {
                "companies": [
                    "sebrae"
                ],
                "includeCompanyStats":True,
                "maxComplaints": 20,
                "proxyConfiguration": {
                    "useApifyProxy": True,
                    "apifyProxyGroups": []
                },
                "statusFilter": "all"
            }
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
    items = dict(items_resp.json())
    
    return items