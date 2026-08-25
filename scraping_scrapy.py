import json
import sys

import scrapy
from scrapy.crawler import CrawlerProcess


RESULTADOS = []


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"

    custom_settings = {
        "LOG_ENABLED": False,
        "USER_AGENT": "UFRN-WebScraping-Atividade-Academica/1.0",
        "DOWNLOAD_TIMEOUT": 20,
    }

    def __init__(self, urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls or []

    def parse(self, response):
        partes = response.css("div.mw-parser-output p ::text").getall()

        if not partes:
            partes = response.css("p ::text").getall()

        texto = " ".join(
            parte.strip()
            for parte in partes
            if parte.strip()
        )

        RESULTADOS.append({
            "url": response.url,
            "texto": texto
        })


if __name__ == "__main__":
    # Windows usa cp1252 por padrao, que nao representa todo texto da Wikipedia.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    urls = sys.argv[1:]

    processo = CrawlerProcess()
    processo.crawl(WikipediaSpider, urls=urls)
    processo.start()

    print(json.dumps(RESULTADOS, ensure_ascii=False))
