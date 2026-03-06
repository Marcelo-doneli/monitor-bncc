import streamlit as st
from src.db import get_connection

st.set_page_config(page_title="Objetivos BNCC", layout="wide")

st.title("Objetivos de Aprendizagem da BNCC")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT code, field, age_group, description
FROM bncc_objectives
ORDER BY age_group, field, code
""")

objetivos = cursor.fetchall()
conn.close()

if objetivos:

    idade = st.selectbox(
        "Filtrar por faixa etária",
        ["Todos", "Bebês", "Crianças bem pequenas", "Crianças pequenas"]
    )

    for obj in objetivos:

        if idade != "Todos" and obj[2] != idade:
            continue

        st.markdown(f"### {obj[0]}")
        st.write("**Campo de experiência:**", obj[1])
        st.write("**Faixa etária:**", obj[2])
        st.write(obj[3])
        st.divider()

else:
    st.info("Nenhum objetivo BNCC cadastrado.")