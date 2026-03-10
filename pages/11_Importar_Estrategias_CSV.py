import csv
import io
import streamlit as st
from src.db import get_connection

st.set_page_config(page_title="Importar Estratégias CSV", layout="wide")

st.title("Importar Estratégias Pedagógicas por CSV")

st.write("Envie uma planilha CSV com as colunas: codigo_objetivo, estrategia, observacoes")

arquivo = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

if arquivo is not None:
    conteudo = arquivo.read().decode("utf-8")
    leitor = csv.DictReader(io.StringIO(conteudo))

    colunas_esperadas = {"codigo_objetivo", "estrategia", "observacoes"}

    if not leitor.fieldnames:
        st.error("O arquivo está vazio ou inválido.")
        st.stop()

    colunas_arquivo = set(leitor.fieldnames)

    if not colunas_esperadas.issubset(colunas_arquivo):
        st.error("O CSV deve conter as colunas: codigo_objetivo, estrategia, observacoes")
        st.stop()

    linhas = list(leitor)

    st.subheader("Pré-visualização")
    st.write(f"Total de linhas encontradas: {len(linhas)}")
    st.dataframe(linhas, use_container_width=True)

    if st.button("Importar estratégias"):
        conn = get_connection()
        cursor = conn.cursor()

        total_importadas = 0
        total_nao_encontradas = 0

        for linha in linhas:
            codigo_objetivo = linha["codigo_objetivo"].strip()
            estrategia = linha["estrategia"].strip()
            observacoes = linha["observacoes"].strip()

            if codigo_objetivo == "" or estrategia == "":
                continue

            cursor.execute("""
            SELECT id
            FROM bncc_objectives
            WHERE code = ?
            """, (codigo_objetivo,))
            objetivo = cursor.fetchone()

            if objetivo:
                objective_id = objetivo[0]

                cursor.execute("""
                INSERT INTO pedagogical_strategies (objective_id, strategy, notes)
                VALUES (?, ?, ?)
                """, (
                    objective_id,
                    estrategia,
                    observacoes
                ))

                total_importadas += 1
            else:
                total_nao_encontradas += 1

        conn.commit()
        conn.close()

        st.success(f"Estratégias importadas com sucesso: {total_importadas}")
        if total_nao_encontradas > 0:
            st.warning(f"Objetivos não encontrados: {total_nao_encontradas}")