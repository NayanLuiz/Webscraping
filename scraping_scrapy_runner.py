import json
import subprocess
import sys
import time
from pathlib import Path

from scraping_requests import resolver_url


def extrair_com_scrapy(termos):
    inicio = time.perf_counter()

    urls = [resolver_url(termo) for termo in termos]

    arquivo_scrapy = Path(__file__).with_name("scraping_scrapy.py")

    comando = [
        sys.executable,
        str(arquivo_scrapy),
        *urls
    ]

    resultado = subprocess.run(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120
    )

    if resultado.returncode != 0:
        detalhe = (resultado.stderr or "").strip()
        raise RuntimeError(detalhe or "O processo Scrapy terminou com erro.")

    linhas = [
        linha.strip()
        for linha in (resultado.stdout or "").splitlines()
        if linha.strip()
    ]

    if not linhas:
        raise RuntimeError("O Scrapy não retornou conteúdo.")

    dados = json.loads(linhas[-1])

    texto_completo = " ".join(
        item.get("texto", "")
        for item in dados
    )

    fim = time.perf_counter()
    tempo = fim - inicio

    return texto_completo, tempo, urls
