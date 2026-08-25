import re

from wordcloud import WordCloud


STOPWORDS_PT = {
    "a", "ao", "aos", "aquela", "aquelas", "aquele", "aqueles",
    "as", "até", "com", "como", "da", "das", "de", "dela", "delas",
    "dele", "deles", "depois", "do", "dos", "e", "ela", "elas",
    "ele", "eles", "em", "entre", "era", "eram", "essa", "essas",
    "esse", "esses", "esta", "estas", "este", "estes", "eu", "foi",
    "foram", "há", "isso", "isto", "já", "mais", "mas", "me", "mesmo",
    "na", "nas", "não", "nem", "no", "nos", "nós", "o", "os", "ou",
    "para", "pela", "pelas", "pelo", "pelos", "por", "porque", "qual",
    "quando", "que", "quem", "se", "sem", "ser", "seu", "seus", "sua",
    "suas", "também", "tem", "tendo", "ter", "um", "uma", "umas", "uns",
    "vai", "vão", "você", "vocês"
}


def limpar_texto(texto):
    palavras = re.findall(
        r"[a-záàâãéêíóôõúüç]+",
        texto.lower()
    )

    palavras_limpas = [
        palavra
        for palavra in palavras
        if palavra not in STOPWORDS_PT and len(palavra) > 2
    ]

    return " ".join(palavras_limpas)


def gerar_nuvem(texto_limpo):
    return WordCloud(
        width=1000,
        height=500,
        background_color="white",
        collocations=False
    ).generate(texto_limpo)


def contar_palavra(texto_limpo, palavra):
    palavra = palavra.lower().strip()
    palavra = re.sub(r"[^a-záàâãéêíóôõúüç]", "", palavra)

    if not palavra:
        return 0

    palavras = texto_limpo.split()
    return palavras.count(palavra)
