import streamlit as st
from src.analysis_engine import (
    get_children_with_deficiency_summary,
    get_most_critical_bncc_objectives,
    get_deficiency_by_field,
    get_deficiency_by_class
)

st.set_page_config(page_title="Resumo Pedagógico", layout="wide")

st.title("Resumo Pedagógico das Defasagens")

st.subheader("1. Crianças com maior número de defasagens")

dados_criancas = get_children_with_deficiency_summary()

if dados_criancas:
    for item in dados_criancas:
        nome = item[1]
        total_defasagens = item[2]

        st.write(f"**{nome}** — {total_defasagens} defasagem(ns)")
else:
    st.success("Nenhuma defasagem registrada até o momento.")

st.divider()

st.subheader("2. Objetivos da BNCC com maior número de defasagens")

dados_objetivos = get_most_critical_bncc_objectives()

if dados_objetivos:
    for item in dados_objetivos:
        codigo = item[0]
        campo = item[1]
        faixa = item[2]
        descricao = item[3]
        total = item[4]

        st.markdown(f"### {codigo}")
        st.write(f"**Campo de experiência:** {campo}")
        st.write(f"**Faixa etária:** {faixa}")
        st.write(f"**Descrição:** {descricao}")
        st.write(f"**Total de defasagens:** {total}")
        st.divider()
else:
    st.info("Nenhum objetivo com defasagem registrado até o momento.")
    st.divider()

st.subheader("3. Defasagens por campo de experiência")

dados_campos = get_deficiency_by_field()

if dados_campos:
    for item in dados_campos:
        campo = item[0]
        total = item[1]

        st.write(f"**{campo}** — {total} defasagem(ns)")
else:
    st.info("Nenhuma defasagem agrupada por campo de experiência.")
    st.divider()

st.subheader("4. Defasagens por turma")

dados_turmas = get_deficiency_by_class()

if dados_turmas:
    for item in dados_turmas:
        turma = item[0]
        escola = item[1]
        total = item[2]

        st.write(f"**{turma}** | Escola: {escola} — {total} defasagem(ns)")
else:
    st.info("Nenhuma defasagem agrupada por turma.")