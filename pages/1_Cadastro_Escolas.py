import streamlit as st
from src.db import get_connection

st.set_page_config(page_title="Cadastro de Escolas", layout="wide")

st.title("Cadastro de Escolas")

st.write("Nesta tela será possível cadastrar as unidades escolares da rede.")

with st.form("form_escola"):
    nome_escola = st.text_input("Nome da escola")
    salvar = st.form_submit_button("Salvar")

    if salvar:
        if nome_escola.strip() == "":
            st.warning("Informe o nome da escola.")
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO schools (name) VALUES (?)",
                (nome_escola.strip(),)
            )
            conn.commit()
            conn.close()
            st.success("Escola cadastrada com sucesso.")

st.subheader("Escolas cadastradas")

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, name FROM schools ORDER BY name")
escolas = cursor.fetchall()
conn.close()

if escolas:
    for escola in escolas:
        st.write(f"{escola[0]} - {escola[1]}")
else:
    st.info("Nenhuma escola cadastrada ainda.")