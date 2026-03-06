import streamlit as st
from src.db import get_connection

st.set_page_config(page_title="Cadastro de Turmas", layout="wide")

st.title("Cadastro de Turmas")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT id, name FROM schools ORDER BY name")
escolas = cursor.fetchall()

if not escolas:
    st.warning("Cadastre pelo menos uma escola antes de cadastrar turmas.")
    conn.close()
    st.stop()

escolas_dict = {escola[1]: escola[0] for escola in escolas}

with st.form("form_turma"):
    escola_selecionada = st.selectbox("Escola", list(escolas_dict.keys()))
    nome_turma = st.text_input("Nome da turma")
    salvar = st.form_submit_button("Salvar")

    if salvar:
        if nome_turma.strip() == "":
            st.warning("Informe o nome da turma.")
        else:
            school_id = escolas_dict[escola_selecionada]
            cursor.execute(
                "INSERT INTO classes (school_id, name) VALUES (?, ?)",
                (school_id, nome_turma.strip())
            )
            conn.commit()
            st.success("Turma cadastrada com sucesso.")

st.subheader("Turmas cadastradas")

cursor.execute("""
    SELECT classes.id, classes.name, schools.name
    FROM classes
    INNER JOIN schools ON classes.school_id = schools.id
    ORDER BY schools.name, classes.name
""")
turmas = cursor.fetchall()

conn.close()

if turmas:
    for turma in turmas:
        st.write(f"{turma[0]} - {turma[1]} | Escola: {turma[2]}")
else:
    st.info("Nenhuma turma cadastrada ainda.")