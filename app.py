import streamlit as st
import matplotlib.pyplot as plt

from scraping_requests import extrair_com_requests
from scraping_scrapy_runner import extrair_com_scrapy
from processamento import limpar_texto, gerar_nuvem, contar_palavra


st.set_page_config(page_title="Web Scraping - Wikipedia", layout="centered")

st.title("Web Scraping - Wikipedia")
st.write("Atividade de Fundamentos e Técnicas em Ciência de Dados - UFRN")

st.markdown("### 1. Escolha o método")
metodo = st.radio(
    "Método de coleta:",
    ["Requests + BeautifulSoup", "Scrapy"]
)

st.markdown("### 2. Digite 5 termos")
termos_texto = st.text_area(
    "Separe os termos por vírgula:",
    value=(
        "Universidade Federal do Rio Grande do Norte, "
        "Ciência de Dados, "
        "Aprendizado de Máquina, "
        "Engenharia de Software, "
        "Armazém de Dados"
    ),
    height=100
)

if st.button("Processar páginas"):
    termos = [termo.strip() for termo in termos_texto.split(",") if termo.strip()]

    if len(termos) != 5:
        st.error("Digite exatamente 5 termos separados por vírgula.")
    else:
        try:
            if metodo == "Requests + BeautifulSoup":
                texto, tempo, urls = extrair_com_requests(termos)
            else:
                texto, tempo, urls = extrair_com_scrapy(termos)

            texto_limpo = limpar_texto(texto)

            st.session_state["texto_limpo"] = texto_limpo
            st.session_state["tempo"] = tempo
            st.session_state["urls"] = urls
            st.session_state["metodo"] = metodo

            st.success("Coleta finalizada.")
        except Exception as erro:
            st.error(f"Erro durante a coleta: {erro}")

if "texto_limpo" in st.session_state:
    st.markdown("### Resultado")
    st.write(f"**Método:** {st.session_state['metodo']}")
    st.write(f"**Tempo de execução:** {st.session_state['tempo']:.2f} segundos")

    with st.expander("Páginas acessadas"):
        for url in st.session_state["urls"]:
            st.write(url)

    if st.session_state["texto_limpo"]:
        st.markdown("### 3. Nuvem de palavras")
        nuvem = gerar_nuvem(st.session_state["texto_limpo"])

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(nuvem, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

        st.markdown("### 4. Contar uma palavra")
        palavra = st.text_input("Digite uma palavra:")

        if st.button("Contar palavra"):
            if palavra.strip():
                quantidade = contar_palavra(
                    st.session_state["texto_limpo"],
                    palavra
                )
                st.write(
                    f'A palavra **"{palavra}"** aparece '
                    f"**{quantidade} vez(es)** no texto limpo das 5 páginas."
                )
            else:
                st.warning("Digite uma palavra.")
    else:
        st.warning("Nenhum texto foi encontrado nas páginas.")
