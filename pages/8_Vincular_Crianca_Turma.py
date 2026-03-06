import streamlit as st
from src.db import get_connection

st.set_page_config(page_title="Vincular Criança à Turma", layout="wide")

st.title("Vincular Criança à Turma")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT id, full_name FROM children ORDER BY full_name")
criancas = cursor.fetchall()

cursor.execute("""
SELECT classes.id, classes.name, schools.name
FROM classes
INNER JOIN schools ON classes.school_id = schools.id
ORDER BY schools.name, classes.name
""")
turmas = cursor.fetchall()

if not criancas:
    st.warning("Cadastre crianças antes de fazer vínculos.")
    conn.close()
    st.stop()

if not turmas:
    st.warning("Cadastre turmas antes de fazer vínculos.")
    conn.close()
    st.stop()

criancas_dict = {c[1]: c[0] for c in criancas}
turmas_dict = {f"{t[1]} - {t[2]}": t[0] for t in turmas}

with st.form("form_vinculo"):
    crianca_selecionada = st.selectbox("Criança", list(criancas_dict.keys()))
    turma_selecionada = st.selectbox("Turma", list(turmas_dict.keys()))
    salvar = st.form_submit_button("Vincular")

    if salvar:
        child_id = criancas_dict[crianca_selecionada]
        class_id = turmas_dict[turma_selecionada]

        cursor.execute("""
        INSERT INTO child_class (child_id, class_id)
        VALUES (?, ?)
        """, (child_id, class_id))

        conn.commit()
        st.success("Criança vinculada à turma com sucesso.")

st.divider()
st.subheader("Vínculos cadastrados")

cursor.execute("""
SELECT
    children.full_name,
    classes.name,
    schools.name
FROM child_class
INNER JOIN children ON child_class.child_id = children.id
INNER JOIN classes ON child_class.class_id = classes.id
INNER JOIN schools ON classes.school_id = schools.id
ORDER BY children.full_name
""")

vinculos = cursor.fetchall()
conn.close()

if vinculos:
    for v in vinculos:
        st.write(f"Criança: {v[0]} | Turma: {v[1]} | Escola: {v[2]}")
else:
    st.info("Nenhum vínculo cadastrado ainda.")