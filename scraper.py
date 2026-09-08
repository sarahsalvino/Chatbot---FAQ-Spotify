import requests
from bs4 import BeautifulSoup
import time
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

URLS = [
    #Como começar:
    "https://support.spotify.com/br-pt/article/getting-started/",
    "https://support.spotify.com/br-pt/article/what-is-spotify/",
    "https://support.spotify.com/br-pt/article/your-library/",
    "https://support.spotify.com/br-pt/article/now-playing/",
    "https://support.spotify.com/br-pt/article/supported-devices-for-spotify/",
    #Soluções de problemas:
    "https://support.spotify.com/br-pt/article/reinstall-spotify/",
    "https://support.spotify.com/br-pt/article/updating-spotify/",
    "https://support.spotify.com/br-pt/article/spotify-not-playing/",
    "https://support.spotify.com/br-pt/article/why-has-the-app-changed/",
    "https://support.spotify.com/br-pt/article/spotify-is-offline/",
    "https://support.spotify.com/br-pt/article/cant-hear-spotify/",
    "https://support.spotify.com/br-pt/article/missing-music-or-podcasts/",
    "https://support.spotify.com/br-pt/article/contact-us/",
]

#Frases/marcadores que indicam "a partir daqui não é mais conteúdo do artigo"
MARCADORES_DE_CORTE = ["Artigos relacionados"]

#Linhas soltas que não são conteúdo de verdade e devem ser removidas
LINHAS_PARA_IGNORAR = ["Você está usando uma ferramenta baseada em IA."]

#Função para raspar o conteúdo de um artigo
def scrape_article(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    main = soup.find("main")
    titulo = main.find("h1").get_text(strip=True)

    elementos = main.find_all(["h2", "h3", "p", "li"])

#Criando uma lista de linhas de texto, ignorando linhas vazias e linhas que contenham marcadores de corte ou linhas para ignorar
    linhas = []
    for el in elementos:
        texto = el.get_text(strip=True)
        if not texto:
            continue
        #Se bater num marcador de corte, para de coletar linhas
        if texto in MARCADORES_DE_CORTE:
            break
        if texto in LINHAS_PARA_IGNORAR:
            continue
        linhas.append(texto)

    conteudo = "\n".join(linhas)

    return {"url": url, "titulo": titulo, "conteudo": conteudo}

#Raspando os artigos e salvando em um arquivo JSON
resultados = []
for url in URLS:
    print(f"Raspando: {url}")
    dados = scrape_article(url)
    resultados.append(dados)
    time.sleep(1)

with open("data/faq_recursos_app.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print("Concluído!")