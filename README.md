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
   git clone https://github.com/mtojald/Web-Scrapping/
   cd seu-repositorio
