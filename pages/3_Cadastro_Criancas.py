import streamlit as st
from src.db import get_connection

st.set_page_config(page_title="Cadastro de Crianças", layout="wide")

st.title("Cadastro de Crianças")

st.write("Cadastro das crianças da Educação Infantil.")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT id, name FROM schools ORDER BY name")
escolas = cursor.fetchall()

if not escolas:
    st.warning("Cadastre uma escola antes de cadastrar crianças.")
    conn.close()
    st.stop()

escolas_dict = {escola[1]: escola[0] for escola in escolas}

with st.form("form_crianca"):

    nome_crianca = st.text_input("Nome da criança")
    data_nascimento = st.date_input("Data de nascimento", format="DD/MM/YYYY")
    escola = st.selectbox("Escola", list(escolas_dict.keys()))

    salvar = st.form_submit_button("Salvar")

    if salvar:

        if nome_crianca.strip() == "":
            st.warning("Informe o nome da criança.")
        else:

            cursor.execute(
                "INSERT INTO children (full_name, birth_date) VALUES (?, ?)",
                (nome_crianca.strip(), str(data_nascimento))
            )

            conn.commit()

            st.success("Criança cadastrada com sucesso.")

st.subheader("Crianças cadastradas")

cursor.execute("""
SELECT children.id, children.full_name, children.birth_date
FROM children
ORDER BY children.full_name
""")

criancas = cursor.fetchall()

conn.close()

if criancas:
    from datetime import datetime

for c in criancas:
    data_formatada = datetime.strptime(c[2], "%Y-%m-%d").strftime("%d/%m/%Y")
    st.write(f"{c[0]} - {c[1]} | Nascimento: {data_formatada}")
else:
    st.info("Nenhuma criança cadastrada ainda.")