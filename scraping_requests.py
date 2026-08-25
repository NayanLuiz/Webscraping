import time
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


WIKIPEDIA_BASE_URL = "https://pt.wikipedia.org"
WIKIPEDIA_API_URL = f"{WIKIPEDIA_BASE_URL}/w/api.php"
CABECALHO = {
    "User-Agent": "UFRN-WebScraping-Atividade-Academica/1.0"
}


def montar_url(termo):
    termo = termo.strip().replace(" ", "_")
    termo = quote(termo, safe="_()-")
    return f"{WIKIPEDIA_BASE_URL}/wiki/{termo}"


def resolver_url(termo):
    """Retorna URL existente, corrigindo capitalizacao/titulo via busca."""
    url_direta = montar_url(termo)
    resposta = requests.get(
        url_direta,
        headers=CABECALHO,
        timeout=20,
        allow_redirects=True,
    )

    if resposta.ok:
        return resposta.url

    if resposta.status_code != 404:
        resposta.raise_for_status()

    busca = requests.get(
        WIKIPEDIA_API_URL,
        headers=CABECALHO,
        params={
            "action": "query",
            "list": "search",
            "srsearch": termo.strip(),
            "srlimit": 1,
            "format": "json",
            "utf8": 1,
        },
        timeout=20,
    )
    busca.raise_for_status()
    resultados = busca.json().get("query", {}).get("search", [])

    if not resultados:
        raise ValueError(f'Nenhuma pagina encontrada para "{termo}".')

    return montar_url(resultados[0]["title"])


def extrair_texto_pagina(url):
    resposta = requests.get(url, headers=CABECALHO, timeout=20)
    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")

    paragrafos = soup.select("div.mw-parser-output p")

    if not paragrafos:
        paragrafos = soup.find_all("p")

    return " ".join(
        paragrafo.get_text(" ", strip=True)
        for paragrafo in paragrafos
    )


def extrair_com_requests(termos):
    inicio = time.perf_counter()

    urls = [resolver_url(termo) for termo in termos]
    textos = []

    for url in urls:
        textos.append(extrair_texto_pagina(url))

    texto_completo = " ".join(textos)

    fim = time.perf_counter()
    tempo = fim - inicio

    return texto_completo, tempo, urls
