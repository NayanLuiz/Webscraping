# Web Scraping na Wikipedia

Projeto simples para a disciplina **Fundamentos e Técnicas em Ciência de Dados - UFRN**.

## Objetivo

Comparar duas formas de fazer Web Scraping em páginas da Wikipedia:

1. Requests + BeautifulSoup
2. Scrapy

O usuário informa 5 termos separados por vírgula. O programa:

- acessa as 5 páginas da Wikipedia;
- extrai os textos dos parágrafos;
- junta todo o conteúdo em uma única string;
- remove stopwords;
- gera uma nuvem de palavras;
- mede o tempo da coleta;
- permite pesquisar quantas vezes uma palavra aparece no texto limpo.

## Estrutura

- `app.py`: aplicação Streamlit.
- `scraping_requests.py`: coleta usando Requests + BeautifulSoup.
- `scraping_scrapy.py`: Spider simples do Scrapy.
- `scraping_scrapy_runner.py`: executa o Scrapy a partir do Streamlit.
- `processamento.py`: limpeza, stopwords, nuvem de palavras e contagem.
- `notebook_colab.ipynb`: versão simples para Google Colab.
- `requirements.txt`: bibliotecas utilizadas.

## Como executar

### 1. Instale as bibliotecas

```bash
pip install -r requirements.txt
```

### 2. Inicie a aplicação

```bash
streamlit run app.py
```

O navegador abrirá a aplicação.

## Exemplo de termos

Digite:

```text
Universidade Federal do Rio Grande do Norte, Ciência de Dados, Aprendizado de Máquina, Engenharia de Software, Armazém de Dados
```

## Observação sobre Scrapy

Na aplicação Streamlit, o Scrapy é executado em um processo separado. Isso deixa o código simples e evita problemas do reactor do Twisted quando o Streamlit recarrega a página.

No Google Colab foi incluído um exemplo usando `crochet`, conforme a observação da atividade.
# Webscraping
