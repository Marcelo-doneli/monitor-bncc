import os
import streamlit as st

st.set_page_config(
    page_title="Sistema de Monitoramento da Aprendizagem",
    layout="wide"
)

st.title("Sistema de Monitoramento da Aprendizagem - Educação Infantil")

st.write("""
Este sistema tem como objetivo acompanhar as aprendizagens das crianças
da Educação Infantil com base nos objetivos da BNCC.
""")

st.subheader("Status do sistema")

if os.path.exists("database.db"):
    st.success("Banco de dados encontrado com sucesso.")
else:
    st.error("Banco de dados não encontrado.")

st.write("Próximas etapas do sistema:")
st.write("- Cadastro de escolas")
st.write("- Cadastro de turmas")
st.write("- Cadastro de crianças")
st.write("- Avaliações diagnósticas")
st.write("- Relatórios pedagógicos")