import streamlit as st
from src.db import get_connection
from datetime import datetime

st.set_page_config(page_title="Crianças com Defasagem", layout="wide")

st.title("Crianças com Defasagem de Aprendizagem")

st.write("Lista das avaliações em que foi identificada defasagem de aprendizagem.")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT
    children.full_name,
    children.birth_date,
    bncc_objectives.code,
    bncc_objectives.field,
    bncc_objectives.age_group,
    bncc_objectives.description,
    assessments.assessment_date,
    assessments.learning_level,
    assessments.notes
FROM assessments
INNER JOIN children ON assessments.child_id = children.id
INNER JOIN bncc_objectives ON assessments.objective_id = bncc_objectives.id
WHERE assessments.deficiency = 'Sim'
ORDER BY children.full_name, assessments.assessment_date DESC
""")

registros = cursor.fetchall()
conn.close()

if registros:
    nomes_criancas = sorted(list(set(r[0] for r in registros)))
    faixas_etarias = sorted(list(set(r[4] for r in registros)))
    campos_experiencia = sorted(list(set(r[3] for r in registros)))

    col1, col2, col3 = st.columns(3)

    with col1:
        filtro_crianca = st.selectbox(
            "Filtrar por criança",
            ["Todas"] + nomes_criancas
        )

    with col2:
        filtro_faixa = st.selectbox(
            "Filtrar por faixa etária",
            ["Todas"] + faixas_etarias
        )

    with col3:
        filtro_campo = st.selectbox(
            "Filtrar por campo de experiência",
            ["Todos"] + campos_experiencia
        )

    registros_filtrados = []

    for r in registros:
        if filtro_crianca != "Todas" and r[0] != filtro_crianca:
            continue
        if filtro_faixa != "Todas" and r[4] != filtro_faixa:
            continue
        if filtro_campo != "Todos" and r[3] != filtro_campo:
            continue
        registros_filtrados.append(r)

    if registros_filtrados:
        for r in registros_filtrados:
            nome_crianca = r[0]
            data_nascimento = datetime.strptime(r[1], "%Y-%m-%d").strftime("%d/%m/%Y")
            codigo_objetivo = r[2]
            campo_experiencia = r[3]
            faixa_etaria = r[4]
            descricao_objetivo = r[5]
            data_avaliacao = datetime.strptime(r[6], "%Y-%m-%d").strftime("%d/%m/%Y")
            nivel = r[7]
            observacoes = r[8] if r[8] else "---"

            st.markdown(f"## {nome_crianca}")
            st.write(f"**Data de nascimento:** {data_nascimento}")
            st.write(f"**Código do objetivo:** {codigo_objetivo}")
            st.write(f"**Campo de experiência:** {campo_experiencia}")
            st.write(f"**Faixa etária:** {faixa_etaria}")
            st.write(f"**Objetivo:** {descricao_objetivo}")
            st.write(f"**Data da avaliação:** {data_avaliacao}")
            st.write(f"**Nível de aprendizagem:** {nivel}")
            st.write(f"**Observações:** {observacoes}")
            st.error("Defasagem identificada")
            st.divider()
    else:
        st.info("Nenhum registro encontrado com os filtros selecionados.")
else:
    st.success("Nenhuma criança com defasagem registrada até o momento.")