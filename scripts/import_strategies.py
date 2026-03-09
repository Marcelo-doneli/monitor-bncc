import csv
from src.db import get_connection


def import_strategies():
    conn = get_connection()
    cursor = conn.cursor()

    arquivo = "data/estrategias.csv"

    with open(arquivo, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)

        total_importadas = 0
        total_nao_encontradas = 0

        for linha in leitor:
            codigo_objetivo = linha["codigo_objetivo"].strip()
            estrategia = linha["estrategia"].strip()
            observacoes = linha["observacoes"].strip()

            cursor.execute("""
            SELECT id
            FROM bncc_objectives
            WHERE code = ?
            """, (codigo_objetivo,))
            objetivo = cursor.fetchone()

            if objetivo:
                objective_id = objetivo[0]

                cursor.execute("""
                INSERT INTO pedagogical_strategies (objective_id, strategy, notes)
                VALUES (?, ?, ?)
                """, (
                    objective_id,
                    estrategia,
                    observacoes
                ))

                total_importadas += 1
            else:
                total_nao_encontradas += 1
                print(f"Objetivo não encontrado: {codigo_objetivo}")

    conn.commit()
    conn.close()

    print(f"Estratégias importadas com sucesso: {total_importadas}")
    print(f"Objetivos não encontrados: {total_nao_encontradas}")


if __name__ == "__main__":
    import_strategies()