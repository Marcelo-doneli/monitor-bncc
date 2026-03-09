import streamlit as st
from src.db import get_connection

st.set_page_config(page_title="Cadastro de Estratégias Pedagógicas", layout="wide")

st.title("Cadastro de Estratégias Pedagógicas")

st.write("Cadastre estratégias pedagógicas vinculadas a objetivos específicos da BNCC.")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT id, code, field, age_group, description
FROM bncc_objectives
ORDER BY age_group, field, code
""")
objetivos = cursor.fetchall()

if not objetivos:
    st.warning("Cadastre objetivos da BNCC antes de cadastrar estratégias pedagógicas.")
    conn.close()
    st.stop()

objetivos_labels = [
    f"{obj[1]} | {obj[2]} | {obj[3]} | {obj[4][:60]}"
    for obj in objetivos
]
objetivos_dict = {
    f"{obj[1]} | {obj[2]} | {obj[3]} | {obj[4][:60]}": obj[0]
    for obj in objetivos
}

st.subheader("Cadastrar nova estratégia")

with st.form("form_estrategia"):
    objetivo_selecionado = st.selectbox("Objetivo da BNCC", objetivos_labels)
    estrategia = st.text_area("Estratégia pedagógica")
    observacoes = st.text_area("Observações (opcional)")
    salvar = st.form_submit_button("Salvar estratégia")

    if salvar:
        if estrategia.strip() == "":
            st.warning("Informe a estratégia pedagógica.")
        else:
            objective_id = objetivos_dict[objetivo_selecionado]

            cursor.execute("""
            INSERT INTO pedagogical_strategies (objective_id, strategy, notes)
            VALUES (?, ?, ?)
            """, (
                objective_id,
                estrategia.strip(),
                observacoes.strip()
            ))

            conn.commit()
            st.success("Estratégia pedagógica cadastrada com sucesso.")
            st.rerun()

st.divider()
st.subheader("Estratégias cadastradas")

cursor.execute("""
SELECT
    pedagogical_strategies.id,
    pedagogical_strategies.objective_id,
    bncc_objectives.code,
    bncc_objectives.field,
    bncc_objectives.age_group,
    bncc_objectives.description,
    pedagogical_strategies.strategy,
    pedagogical_strategies.notes
FROM pedagogical_strategies
INNER JOIN bncc_objectives ON pedagogical_strategies.objective_id = bncc_objectives.id
ORDER BY bncc_objectives.age_group, bncc_objectives.field, bncc_objectives.code
""")

estrategias = cursor.fetchall()

if estrategias:
    for e in estrategias:
        estrategia_id = e[0]
        objective_id_atual = e[1]
        codigo = e[2]
        campo = e[3]
        faixa = e[4]
        descricao = e[5]
        estrategia_texto = e[6]
        observacoes_texto = e[7] if e[7] else ""

        with st.expander(f"{codigo} - {estrategia_texto[:80]}"):
            st.write(f"**Campo de experiência:** {campo}")
            st.write(f"**Faixa etária:** {faixa}")
            st.write(f"**Objetivo:** {descricao}")

            col1, col2 = st.columns(2)

            with col1:
                with st.form(f"editar_estrategia_{estrategia_id}"):
                    # descobrir qual índice do objetivo atual
                    label_atual = None
                    for obj in objetivos:
                        if obj[0] == objective_id_atual:
                            label_atual = f"{obj[1]} | {obj[2]} | {obj[3]} | {obj[4][:60]}"
                            break

                    novo_objetivo = st.selectbox(
                        "Objetivo da BNCC",
                        objetivos_labels,
                        index=objetivos_labels.index(label_atual) if label_atual in objetivos_labels else 0,
                        key=f"obj_{estrategia_id}"
                    )

                    nova_estrategia = st.text_area(
                        "Estratégia pedagógica",
                        value=estrategia_texto,
                        key=f"estrategia_{estrategia_id}"
                    )

                    novas_observacoes = st.text_area(
                        "Observações",
                        value=observacoes_texto,
                        key=f"obs_{estrategia_id}"
                    )

                    salvar_edicao = st.form_submit_button("Salvar alterações")

                    if salvar_edicao:
                        if nova_estrategia.strip() == "":
                            st.warning("Informe a estratégia pedagógica.")
                        else:
                            novo_objective_id = objetivos_dict[novo_objetivo]

                            cursor.execute("""
                            UPDATE pedagogical_strategies
                            SET objective_id = ?, strategy = ?, notes = ?
                            WHERE id = ?
                            """, (
                                novo_objective_id,
                                nova_estrategia.strip(),
                                novas_observacoes.strip(),
                                estrategia_id
                            ))

                            conn.commit()
                            st.success("Estratégia atualizada com sucesso.")
                            st.rerun()

            with col2:
                st.write("")
                st.write("")
                excluir = st.button("Excluir estratégia", key=f"excluir_estrategia_{estrategia_id}")

                if excluir:
                    cursor.execute(
                        "DELETE FROM pedagogical_strategies WHERE id = ?",
                        (estrategia_id,)
                    )
                    conn.commit()
                    st.success("Estratégia excluída com sucesso.")
                    st.rerun()
else:
    st.info("Nenhuma estratégia pedagógica cadastrada ainda.")

conn.close()