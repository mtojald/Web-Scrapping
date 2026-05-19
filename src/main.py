# src/main.py
import json
import os
from bs4 import BeautifulSoup

def rodar_scraping_local():
    # define o caminho do html LOCAL, caso seja link usa url = link
    
    caminho_html = os.path.join("src", "pagina_sebrae.html")
    
    if not os.path.exists(caminho_html):
        print(f"Erro: O arquivo {caminho_html} não foi encontrado na pasta 'src'.")
        return

    print("Lendo página de feedbacks locais estruturados do SEBRAE...")
    
    # Abre e lê o conteúdo do HTML estático
    with open(caminho_html, "r", encoding="utf-8") as f:
        html_conteudo = f.read()

    # O BeautifulSoup faz o parseamento do documento local
    soup = BeautifulSoup(html_conteudo, "html.parser")
    dados_extraidos = []

    # Localiza todos os blocos de feedbacks definidos pela classe CSS
    feedbacks = soup.select(".feedback-card")

    for item in feedbacks:
        # Extrai os textos limpando os espaços extras das tags
        titulo = item.select_one(".titulo").get_text(strip=True)
        comentario = item.select_one(".comentario").get_text(strip=True)
        nota = item.select_one(".nota").get_text(strip=True)

        # Guarda os dados mapeados explicitamente para o SEBRAE
        dados_extraidos.append({
            "alvo_coleta": "SEBRAE",
            "titulo_feedback": titulo,
            "comentario_usuario": comentario,
            "avaliacao": nota
        })

    # Salva o resultado final estruturado em JSON na raiz do projeto
    with open("resultado_sebrae_local.json", "w", encoding="utf-8") as f:
        json.dump(dados_extraidos, f, indent=4, ensure_ascii=False)
        
    print(f"\nSucesso! {len(dados_extraidos)} feedbacks do SEBRAE foram extraídos via BeautifulSoup.")
    print("O arquivo 'resultado_sebrae_local.json' foi gerado com sucesso!")

if __name__ == "__main__":
    rodar_scraping_local()