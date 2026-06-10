# 🕸️ Scrapper

Este é um projeto de Web Scraping desenvolvido em Python utilizando a biblioteca **BeautifulSoup (bs4)**. O objetivo principal é extrair dados do SEBRAE para monitorar pontos de melhorias baseado nas avaliações públicas dos consumidores.

## 🚀 Funcionalidades

- Conexão e requisição HTTP ao site alvo utilizando a biblioteca `requests`.
- Parseamento (análise) de HTML robusto com `BeautifulSoup`.
- Extração automática de:
  - Avaliações
  - Comentários
  - Serviço
- Exportação dos dados extraídos para um arquivo `[ex: dados.csv / dados.json]`.

## 🛠️ Tecnologias Utilizadas

- **Python** 
- **BeautifulSoup4 (bs4)** - Para extração e navegação no HTML.
- **Requests** - Para enviar as requisições HTTP.
- **Pandas** (Opcional) - Para manipulação de dados e exportação para CSV.

## 📋 Pré-requisitos

Antes de começar, você vai precisar ter o **Python** instalado em sua máquina.

Também é altamente recomendável utilizar um ambiente virtual (como `venv`).

## 🔧 Instalação e Execução

Siga os passos abaixo para rodar o projeto localmente:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/mtojald/Web-Scrapping.git
   cd seu-repositorio
   ```
2. **Instale dependências:**
   ```bash
   python -m pip install -r requirements.txt
   ```
3. **Configure variáveis de ambiente:**
   Crie um arquivo `.env` com as chaves necessárias, por exemplo:
   ```ini
   NEWS_API_KEY=seu_news_api_key
   YOUTUBE_API_KEY=seu_youtube_api_key
   APIFY_API_TOKEN=seu_apify_api_token
   REDDIT_CLIENT_ID=seu_reddit_client_id
   REDDIT_CLIENT_SECRET=seu_reddit_client_secret
   ```

## ▶️ Como rodar o scraper (`main.py`)

O arquivo `main.py` inicia a classe `scrapBot` em `src/bot/bot.py`.

- `python main.py all`
  - executa a sequência de scrapers `reddit`, `news` e `youtube`.
- `python main.py plataforma1 plataforma2 (Ex: python main.py news youtube)`
  - executa apenas os scrapers passados


### Como `sys.argv` é usado

A classe `scrapBot` recebe `sys.argv` no construtor e verifica cada argumento passado na linha de comando:

Os resultados são gravados em `src/JSON/reqPlataformas.json`.

## ▶️ Como rodar a interface Streamlit

Para abrir o dashboard, execute o comando abaixo a partir da raiz do projeto:

```bash
streamlit run app.py
```

Isso carrega a aplicação com as páginas:
- `pages/1_dashboard.py`
- `pages/2_publicacoes.py`
- `pages/3_resumo.py`

## 🧩 Parâmetros de requisição por scraper

### Apify

- Endpoint principal:
  - `POST https://api.apify.com/v2/acts/apify~google-search-scraper/runs`
- Parâmetros enviados no corpo JSON (mais importantes e editáveis):
  - `queries`: string de busca (`padrão: SEBRAE`)
  - `maxPagesPerQuery`: número de páginas por consulta (fixo em `1`)
  - `resultsPerPage`: número de resultados por página (`min(limite, 10)`)
- Parâmetros enviados na querystring:
  - `token`: valor de `APIFY_API_TOKEN`
- Uso adicional (opcional):
  - Consulta do status do run em `GET https://api.apify.com/v2/actor-runs/{run_id}`
  - Leitura de dados em `GET https://api.apify.com/v2/datasets/{dataset_id}/items` com `token` e `limit`

### NewsAPI 

- Endpoint:
  - `GET https://newsapi.org/v2/everything`
- Parâmetros querystring:
  - `q`: string de busca (`query`)
  - `sortBy`: `publishedAt`
  - `pageSize`: número de artigos retornados (`min(limite, 100)`)
  - `apiKey`: valor de `NEWS_API_KEY`

### YouTube

- Endpoint:
  - `GET https://www.googleapis.com/youtube/v3/search`
- Parâmetros querystring:
  - `part`: `snippet`
  - `q`: string de busca (`query`)
  - `type`: `video`
  - `maxResults`: número de vídeos retornados (`min(limite, 50)`)
  - `relevanceLanguage`: `pt`
  - `order`: `date`
  - `key`: valor de `YOUTUBE_API_KEY`

### Reddit (`src/scrapers/reddit_scraper.py`)

- Atualmente a função `coletar_reddit(query, limite)` retorna uma lista vazia e não possui requisição implementada.

## 🌐 Variáveis de ambiente necessárias

- `APIFY_API_TOKEN` — token do Apify para executar o actor e buscar resultados.
- `NEWS_API_KEY` — chave da NewsAPI para buscar artigos.
- `YOUTUBE_API_KEY` — chave da API do YouTube para busca de vídeos.
- `REDDIT_CLIENT_ID` e `REDDIT_CLIENT_SECRET` — necessários quando o scraper de Reddit estiver implementado.
