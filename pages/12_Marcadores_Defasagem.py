import streamlit as st
from datetime import datetime
from src.db import get_connection

st.set_page_config(page_title="Marcadores de Defasagem", layout="wide")

st.title("Marcadores Persistentes de Defasagem")

st.write("""
Esta tela mostra os marcadores de defasagem gerados automaticamente pelo sistema.
O marcador permanece ativo até que a criança apresente avanço em nova avaliação do mesmo objetivo.
""")


def formatar_data(data_texto):
    if not data_texto:
        return "---"

    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(data_texto, formato).strftime("%d/%m/%Y")
        except ValueError:
            pass

    return data_texto


conn = get_connection()
cursor = conn.cursor()

filtro_status = st.selectbox(
    "Filtrar por status",
    ["ATIVO", "ENCERRADO", "Todos"]
)

query = """
SELECT
    deficiency_markers.id,
    children.full_name,
    bncc_objectives.id,
    bncc_objectives.code,
    bncc_objectives.field,
    bncc_objectives.age_group,
    bncc_objectives.description,
    deficiency_markers.status,
    deficiency_markers.opened_date,
    deficiency_markers.closed_date
FROM deficiency_markers
INNER JOIN children ON deficiency_markers.child_id = children.id
INNER JOIN bncc_objectives ON deficiency_markers.objective_id = bncc_objectives.id
"""

params = []

if filtro_status != "Todos":
    query += " WHERE deficiency_markers.status = ?"
    params.append(filtro_status)

query += """
ORDER BY
    deficiency_markers.status,
    children.full_name,
    bncc_objectives.code
"""

cursor.execute(query, params)
marcadores = cursor.fetchall()

if marcadores:
    for m in marcadores:
        marker_id = m[0]
        nome_crianca = m[1]
        objective_id = m[2]
        codigo_objetivo = m[3]
        campo = m[4]
        faixa = m[5]
        descricao = m[6]
        status = m[7]
        data_abertura = formatar_data(m[8])
        data_encerramento = formatar_data(m[9])

        st.markdown(f"## {nome_crianca}")

        if status == "ATIVO":
            st.error("Marcador ativo de defasagem")
        else:
            st.success("Marcador encerrado")

        st.write(f"**Código do objetivo:** {codigo_objetivo}")
        st.write(f"**Campo de experiência:** {campo}")
        st.write(f"**Faixa etária:** {faixa}")
        st.write(f"**Objetivo:** {descricao}")
        st.write(f"**Data de abertura:** {data_abertura}")
        st.write(f"**Data de encerramento:** {data_encerramento}")

        if status == "ATIVO":
            cursor.execute("""
            SELECT strategy, notes
            FROM pedagogical_strategies
            WHERE objective_id = ?
            """, (objective_id,))

            estrategias = cursor.fetchall()

            if estrategias:
                st.write("**Estratégias pedagógicas sugeridas:**")
                for estrategia in estrategias:
                    texto = estrategia[0]
                    observacao = estrategia[1] if estrategia[1] else ""

                    st.write(f"- {texto}")
                    if observacao:
                        st.write(f"  Observação: {observacao}")
            else:
                st.info("Não há estratégias pedagógicas cadastradas para este objetivo.")

        st.divider()
else:
    st.info("Nenhum marcador encontrado.")

conn.close()