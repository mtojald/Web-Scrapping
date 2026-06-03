# EXEMPLOS_REQ

## Apify

### Requisição completa de criação de run
```bash
curl -X POST "https://api.apify.com/v2/acts/apify~google-search-scraper/runs?token=<APIFY_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": "SEBRAE",
    "maxPagesPerQuery": 1,
    "resultsPerPage": 10,
    "languageCode": "pt",
    "countryCode": "br"
  }'
```

Principais parâmetros:
- `token`: `<APIFY_API_TOKEN>` (query string)
- `queries`: termo de busca
- `maxPagesPerQuery`: número de páginas por consulta
- `resultsPerPage`: máximo de resultados retornados por página


## NewsAPI

### Requisição completa de busca de notícias
```bash
curl "https://newsapi.org/v2/everything?q=SEBRAE&language=pt&sortBy=publishedAt&pageSize=10&apiKey=<NEWS_API_KEY>"
```

Principais parâmetros:
- `q`: termo de busca
- `language`: `pt`
- `sortBy`: `publishedAt`
- `pageSize`: número de artigos retornados
- `apiKey`: `<NEWS_API_KEY>`

## YouTube

### Requisição completa de busca de vídeos
```bash
curl "https://www.googleapis.com/youtube/v3/search?part=snippet&q=SEBRAE&type=video&maxResults=10&relevanceLanguage=pt&order=date&key=<YOUTUBE_API_KEY>"
```

Principais parâmetros:
- `part`: `snippet`
- `q`: termo de busca
- `type`: `video`
- `maxResults`: número de vídeos retornados
- `relevanceLanguage`: `pt`
- `order`: `date`
- `key`: `<YOUTUBE_API_KEY>`

## Reddit

A função `src/scrapers/reddit_scraper.py` ainda não está implementada no projeto. Não há requisição `curl` completa usada atualmente pelo scraper.
