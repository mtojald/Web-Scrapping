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

---

## Exemplos de respostas (JSON)

### YouTube (exemplo de item `items[]` retornado pela API)
```json
{
  "kind": "youtube#searchResult",
  "etag": "CuSOmcZf6tR72MRNUvvdxkXSlfs",
  "id": { "kind": "youtube#video", "videoId": "zOCVf45fAPU" },
  "snippet": {
    "publishedAt": "2026-06-02T14:24:58Z",
    "channelId": "UCzTRZtuTwFkWI_bnpltZjgA",
    "title": "O Conecta MEI é um programa que conecta MEIs à prestação de serviços nas agências da CAIXA",
    "description": "MEI, sua próxima oportunidade de trabalho começa agora! O Conecta MEI é um programa que conecta microempreendedores ...",
    "thumbnails": {
      "default": { "url": "https://i.ytimg.com/vi/zOCVf45fAPU/default.jpg", "width": 120, "height": 90 },
      "medium": { "url": "https://i.ytimg.com/vi/zOCVf45fAPU/mqdefault.jpg", "width": 320, "height": 180 },
      "high": { "url": "https://i.ytimg.com/vi/zOCVf45fAPU/hqdefault.jpg", "width": 480, "height": 360 }
    },
    "channelTitle": "Sebrae Amazonas",
    "liveBroadcastContent": "none",
    "publishTime": "2026-06-02T14:24:58Z"
  }
}
```

### NewsAPI (exemplo retirado de `src/JSON/reqPlataformas.json`)
```json
{
  "fonte": "NewsAPI",
  "alvo_coleta": "SEBRAE",
  "titulo_feedback": "O mercado que não sabe\ncontar seu consumidor",
  "comentario_usuario": "Por que o Brasil, o 4º maior mercado de beleza do mundo, ainda não mede quem realmente o sustenta",
  "avaliacao": "Fonte: Ig.com.br",
  "url": "https://gente.ig.com.br/colunas/luiz-cantu/2026-06-01/o-mercado-que-nao-sabe-contar-seu-consumidor.html",
  "data": "2026-06-01"
}
```

### Apify (exemplo de item de dataset / `organicResults[]` usado no scraper)
```json
{
  "source": "Apify",
  "organicResults": [
    {
      "position": 1,
      "title": "SEBRAE: como melhorar atendimento ao microempreendedor",
      "description": "Artigo com opinião sobre atendimentos e vagas de capacitação",
      "snippet": "Resumo do conteúdo encontrado na página",
      "url": "https://exemplo.com/sebrae-artigo",
      "date": "2026-06-01"
    }
  ]
}
```

### Reddit (exemplo de estrutura de post quando implementar)
```json
{
  "data": {
    "children": [
      {
        "kind": "t3",
        "data": {
          "id": "abcd12",
          "title": "Experiência com SEBRAE: curso grátis ajudou no faturamento",
          "selftext": "Depoimento do usuário sobre o curso",
          "subreddit": "brasil",
          "created_utc": 1717000000,
          "url": "https://reddit.com/r/brasil/comments/abcd12/experiencia_sebrae/"
        }
      }
    ]
  }
}
```
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

---

## Exemplos de respostas (JSON)

### YouTube (exemplo de item `items[]` retornado pela API)
```json
{
  "kind": "youtube#searchResult",
  "etag": "CuSOmcZf6tR72MRNUvvdxkXSlfs",
  "id": { "kind": "youtube#video", "videoId": "zOCVf45fAPU" },
  "snippet": {
    "publishedAt": "2026-06-02T14:24:58Z",
    "channelId": "UCzTRZtuTwFkWI_bnpltZjgA",
    "title": "O Conecta MEI é um programa que conecta MEIs à prestação de serviços nas agências da CAIXA",
    "description": "MEI, sua próxima oportunidade de trabalho começa agora! O Conecta MEI é um programa que conecta microempreendedores ...",
    "thumbnails": {
      "default": { "url": "https://i.ytimg.com/vi/zOCVf45fAPU/default.jpg", "width": 120, "height": 90 },
      "medium": { "url": "https://i.ytimg.com/vi/zOCVf45fAPU/mqdefault.jpg", "width": 320, "height": 180 },
      "high": { "url": "https://i.ytimg.com/vi/zOCVf45fAPU/hqdefault.jpg", "width": 480, "height": 360 }
    },
    "channelTitle": "Sebrae Amazonas",
    "liveBroadcastContent": "none",
    "publishTime": "2026-06-02T14:24:58Z"
  }
}
```

### NewsAPI (exemplo retirado de `src/JSON/reqPlataformas.json`)
```json

    "status": "ok",
    "totalResults": 65,
    "articles": [
        {
            "source": {
                "id": null,
                "name": "Ig.com.br"
            },
            "author": "Luiz Cantú, Luiz Cantú",
            "title": "O mercado que não sabe\ncontar seu consumidor",
            "description": "Por que o Brasil, o 4º maior mercado de beleza do mundo, ainda não mede quem realmente o sustenta",
            "url": "https://gente.ig.com.br/colunas/luiz-cantu/2026-06-01/o-mercado-que-nao-sabe-contar-seu-consumidor.html",
            "urlToImage": "https://i0.statig.com.br/bancodeimagens/9t/l8/ek/9tl8ek3auueqiqt7xapb0q0nr.jpg",
            "publishedAt": "2026-06-01T16:15:01Z",
            "content": "Existe uma pergunta que o mercado de beleza brasileiro ainda não aprendeu a fazer. Não é sobre tendência, não é sobre ingrediente ativo e não é sobre qual tom de batom vai viralizar na próxima estaçã… [+10321 chars]"
        },
        {
            "source": {
                "id": "globo",
                "name": "Globo"
            },
            "author": null,
            "title": "Franchising dobra economia e atrai novos investidores",
            "description": "Setor faturou R$ 273 bilhões em 2024, cresceu 13,5% — quase quatro vezes acima do PIB — e abre espaço para modelos enxutos como o das lavanderias express",
            "url": "https://valor.globo.com/patrocinado/dino/noticia/2026/06/01/franchising-dobra-economia-e-atrai-novos-investidores-1.ghtml",
            "urlToImage": "https://s3.glbimg.com/v1/AUTH_63b422c2caee4269b8b34177e8876b93/public/fb_marca.png",
            "publishedAt": "2026-06-01T13:29:20Z",
            "content": "O franchising brasileiro cresceu quase quatro vezes mais que o Produto Interno Bruto (PIB) nos últimos dois anos. Em 2024, dados da Associação Brasileira de Franchising (ABF) mostram que o setor fatu… [+3529 chars]"
        },
```

### Apify (exemplo de item de dataset / `organicResults[]` usado no scraper)
```json
{
  "source": "Apify",
  "organicResults": [
    {
      "position": 1,
      "title": "SEBRAE: como melhorar atendimento ao microempreendedor",
      "description": "Artigo com opinião sobre atendimentos e vagas de capacitação",
      "snippet": "Resumo do conteúdo encontrado na página",
      "url": "https://exemplo.com/sebrae-artigo",
      "date": "2026-06-01"
    }
  ]
}
```

### Reddit (exemplo de estrutura de post quando implementar)
```json
{
  "data": {
    "children": [
      {
        "kind": "t3",
        "data": {
          "id": "abcd12",
          "title": "Experiência com SEBRAE: curso grátis ajudou no faturamento",
          "selftext": "Depoimento do usuário sobre o curso",
          "subreddit": "brasil",
          "created_utc": 1717000000,
          "url": "https://reddit.com/r/brasil/comments/abcd12/experiencia_sebrae/"
        }
      }
    ]
  }
}
```
