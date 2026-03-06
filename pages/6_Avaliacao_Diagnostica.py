import streamlit as st
from src.db import get_connection
from datetime import datetime

st.set_page_config(page_title="Avaliação Diagnóstica", layout="wide")

st.title("Avaliação Diagnóstica")

conn = get_connection()
cursor = conn.cursor()

# Buscar turmas com escola
cursor.execute("""
SELECT classes.id, classes.name, schools.name
FROM classes
INNER JOIN schools ON classes.school_id = schools.id
ORDER BY schools.name, classes.name
""")
turmas = cursor.fetchall()

if not turmas:
    st.warning("Cadastre pelo menos uma turma antes de lançar avaliações.")
    conn.close()
    st.stop()

turmas_dict = {f"{t[1]} - {t[2]}": t[0] for t in turmas}

# Buscar objetivos BNCC
cursor.execute("""
SELECT id, code, description
FROM bncc_objectives
ORDER BY code
""")
objetivos = cursor.fetchall()

if not objetivos:
    st.warning("Cadastre pelo menos um objetivo da BNCC antes de lançar avaliações.")
    conn.close()
    st.stop()

objetivos_dict = {
    f"{objetivo[1]} - {objetivo[2]}": objetivo[0]
    for objetivo in objetivos
}

turma_selecionada = st.selectbox("Turma", list(turmas_dict.keys()))
class_id = turmas_dict[turma_selecionada]

# Buscar apenas crianças da turma selecionada
cursor.execute("""
SELECT children.id, children.full_name
FROM child_class
INNER JOIN children ON child_class.child_id = children.id
WHERE child_class.class_id = ?
ORDER BY children.full_name
""", (class_id,))
criancas = cursor.fetchall()

if not criancas:
    st.warning("Não há crianças vinculadas a esta turma.")
    conn.close()
    st.stop()

criancas_dict = {crianca[1]: crianca[0] for crianca in criancas}

with st.form("form_avaliacao"):

    crianca_selecionada = st.selectbox("Criança", list(criancas_dict.keys()))
    objetivo_selecionado = st.selectbox("Objetivo da BNCC", list(objetivos_dict.keys()))
    data_avaliacao = st.date_input("Data da avaliação", format="DD/MM/YYYY")

    nivel_aprendizagem = st.selectbox(
        "Nível de aprendizagem",
        [
            "Não desenvolvido",
            "Em desenvolvimento",
            "Desenvolvido"
        ]
    )

    observacoes = st.text_area("Observações")

    salvar = st.form_submit_button("Salvar avaliação")

    if salvar:
        child_id = criancas_dict[crianca_selecionada]
        objective_id = objetivos_dict[objetivo_selecionado]

        if nivel_aprendizagem == "Não desenvolvido":
            defasagem = "Sim"
        else:
            defasagem = "Não"

        cursor.execute("""
        INSERT INTO assessments (
            child_id,
            objective_id,
            assessment_date,
            learning_level,
            notes,
            deficiency
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            child_id,
            objective_id,
            str(data_avaliacao),
            nivel_aprendizagem,
            observacoes.strip(),
            defasagem
        ))

        conn.commit()
        st.success("Avaliação registrada com sucesso.")

st.divider()
st.subheader("Avaliações registradas")

cursor.execute("""
SELECT
    assessments.id,
    children.full_name,
    bncc_objectives.code,
    bncc_objectives.description,
    assessments.assessment_date,
    assessments.learning_level,
    assessments.notes,
    assessments.deficiency
FROM assessments
INNER JOIN children ON assessments.child_id = children.id
INNER JOIN bncc_objectives ON assessments.objective_id = bncc_objectives.id
ORDER BY assessments.assessment_date DESC, children.full_name
""")

avaliacoes = cursor.fetchall()
conn.close()

if avaliacoes:
    for av in avaliacoes:
        data_formatada = datetime.strptime(av[4], "%Y-%m-%d").strftime("%d/%m/%Y")

        st.markdown(f"**{av[1]}**")
        st.write(f"Objetivo: {av[2]} - {av[3]}")
        st.write(f"Data: {data_formatada}")
        st.write(f"Nível: {av[5]}")
        st.write(f"Defasagem identificada: {av[7] if av[7] else 'Não'}")
        st.write(f"Observações: {av[6] if av[6] else '---'}")
        st.divider()
else:
    st.info("Nenhuma avaliação registrada ainda.")