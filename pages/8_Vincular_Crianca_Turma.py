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
        SELECT id
        FROM child_class
        WHERE child_id = ? AND class_id = ?
        """, (child_id, class_id))

        vinculo_existente = cursor.fetchone()

        if vinculo_existente:
            st.warning("Esta criança já está vinculada a essa turma.")
        else:
            cursor.execute("""
            INSERT INTO child_class (child_id, class_id)
            VALUES (?, ?)
            """, (child_id, class_id))

            conn.commit()
            st.success("Criança vinculada à turma com sucesso.")
            st.rerun()

st.divider()
st.subheader("Vínculos cadastrados")

cursor.execute("""
SELECT
    child_class.id,
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

if vinculos:
    for v in vinculos:
        vinculo_id = v[0]
        nome_crianca = v[1]
        nome_turma = v[2]
        nome_escola = v[3]

        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(f"Criança: {nome_crianca} | Turma: {nome_turma} | Escola: {nome_escola}")

        with col2:
            if st.button("Excluir", key=f"excluir_{vinculo_id}"):
                cursor.execute("DELETE FROM child_class WHERE id = ?", (vinculo_id,))
                conn.commit()
                st.success("Vínculo excluído com sucesso.")
                st.rerun()
else:
    st.info("Nenhum vínculo cadastrado ainda.")

conn.close()