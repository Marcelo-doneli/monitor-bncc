import streamlit as st
from src.db import get_connection

st.set_page_config(page_title="Cadastro Objetivos BNCC", layout="wide")

st.title("Cadastro de Objetivos de Aprendizagem da BNCC")

campos_experiencia = [
    "O eu, o outro e o nós",
    "Corpo, gestos e movimentos",
    "Traços, sons, cores e formas",
    "Escuta, fala, pensamento e imaginação",
    "Espaços, tempos, quantidades, relações e transformações"
]

faixas_etarias = [
    "Bebês",
    "Crianças bem pequenas",
    "Crianças pequenas"
]

conn = get_connection()
cursor = conn.cursor()

st.subheader("Cadastrar novo objetivo")

with st.form("form_bncc"):
    codigo = st.text_input("Código do objetivo (ex: EI02EO01)")
    campo = st.selectbox("Campo de experiência", campos_experiencia)
    faixa = st.selectbox("Faixa etária", faixas_etarias)
    descricao = st.text_area("Descrição do objetivo")

    salvar = st.form_submit_button("Salvar objetivo")

    if salvar:
        if codigo.strip() == "" or descricao.strip() == "":
            st.warning("Preencha todos os campos.")
        else:
            cursor.execute("""
                INSERT INTO bncc_objectives (code, field, age_group, description)
                VALUES (?, ?, ?, ?)
            """, (codigo.strip(), campo, faixa, descricao.strip()))
            conn.commit()
            st.success("Objetivo cadastrado com sucesso.")
            st.rerun()

st.divider()
st.subheader("Objetivos cadastrados")

cursor.execute("""
    SELECT id, code, field, age_group, description
    FROM bncc_objectives
    ORDER BY age_group, field, code
""")
objetivos = cursor.fetchall()

if objetivos:
    for obj in objetivos:
        obj_id, code, field, age_group, description = obj

        with st.expander(f"{code} - {description[:80]}"):
            st.write(f"**Código:** {code}")
            st.write(f"**Campo:** {field}")
            st.write(f"**Faixa etária:** {age_group}")
            st.write(f"**Descrição:** {description}")

            col1, col2 = st.columns(2)

            with col1:
                with st.form(f"editar_{obj_id}"):
                    novo_codigo = st.text_input("Código", value=code, key=f"codigo_{obj_id}")
                    novo_campo = st.selectbox(
                        "Campo de experiência",
                        campos_experiencia,
                        index=campos_experiencia.index(field),
                        key=f"campo_{obj_id}"
                    )
                    nova_faixa = st.selectbox(
                        "Faixa etária",
                        faixas_etarias,
                        index=faixas_etarias.index(age_group),
                        key=f"faixa_{obj_id}"
                    )
                    nova_descricao = st.text_area(
                        "Descrição",
                        value=description,
                        key=f"descricao_{obj_id}"
                    )

                    salvar_edicao = st.form_submit_button("Salvar alterações")

                    if salvar_edicao:
                        if novo_codigo.strip() == "" or nova_descricao.strip() == "":
                            st.warning("Preencha todos os campos da edição.")
                        else:
                            cursor.execute("""
                                UPDATE bncc_objectives
                                SET code = ?, field = ?, age_group = ?, description = ?
                                WHERE id = ?
                            """, (
                                novo_codigo.strip(),
                                novo_campo,
                                nova_faixa,
                                nova_descricao.strip(),
                                obj_id
                            ))
                            conn.commit()
                            st.success("Objetivo atualizado com sucesso.")
                            st.rerun()

            with col2:
                st.write("")
                st.write("")
                excluir = st.button("Excluir objetivo", key=f"excluir_{obj_id}")

                if excluir:
                    cursor.execute("DELETE FROM bncc_objectives WHERE id = ?", (obj_id,))
                    conn.commit()
                    st.success("Objetivo excluído com sucesso.")
                    st.rerun()
else:
    st.info("Nenhum objetivo cadastrado.")

conn.close()