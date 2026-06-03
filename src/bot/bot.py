from . import coletar_reddit, coletar_noticias, coletar_youtube, coletar_apify
from .callParams import FONTES, RESULTADO_PATH, QUERY
import json
import sys

class scrapBot():
    
    def __init__(self, arguments=sys.argv):
        self.arguments=arguments    
     
    def rodar_scraping(self):
        dados = []
        
        if self.arguments[1]=="all":
            dados = self.scrappersEmSeq()
        
        for plataforma in self.arguments:
            match plataforma:
                case "reddit":
                    dados += coletar_reddit(QUERY, limite=50)
                case "news":
                    dados += coletar_noticias(QUERY, limite=50)
                case "youtube":
                    dados += coletar_youtube(QUERY, limite=30)
                case "apify":
                    pass
                    #dados += coletar_apify(QUERY, limite=30)
                case _:
                    print("\nNenhuma fonte ativa. Configure as variáveis no arquivo .env")

        with open(RESULTADO_PATH, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        print(f"\n✅ {len(dados)} itens salvos em '{RESULTADO_PATH}'")

    def scrappersEmSeq(self):
            dadosAcc = []
        
            dadosAcc += coletar_reddit(QUERY, limite=50)
            dadosAcc += coletar_noticias(QUERY, limite=50)
            dadosAcc += coletar_youtube(QUERY, limite=30)
            #dadosAcc += coletar_apify(QUERY, limite=30)
            
            return dadosAcc
        
        

