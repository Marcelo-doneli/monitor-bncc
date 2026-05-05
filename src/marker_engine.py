from datetime import date


def update_deficiency_marker(
    conn,
    child_id,
    objective_id,
    assessment_id,
    assessment_date,
    learning_level
):
    cursor = conn.cursor()

    # Verifica se já existe marcador ativo para essa criança e esse objetivo
    cursor.execute("""
    SELECT id
    FROM deficiency_markers
    WHERE child_id = ?
      AND objective_id = ?
      AND status = 'ATIVO'
    """, (child_id, objective_id))

    marcador_ativo = cursor.fetchone()

    # Caso 1: avaliação indica defasagem
    if learning_level == "Não desenvolvido":

        if marcador_ativo:
            marker_id = marcador_ativo[0]

            cursor.execute("""
            UPDATE deficiency_markers
            SET last_assessment_id = ?
            WHERE id = ?
            """, (assessment_id, marker_id))

        else:
            cursor.execute("""
            INSERT INTO deficiency_markers (
                child_id,
                objective_id,
                status,
                opened_date,
                closed_date,
                last_assessment_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                child_id,
                objective_id,
                "ATIVO",
                str(assessment_date),
                None,
                assessment_id
            ))

    # Caso 2: avaliação indica avanço
    else:
        if marcador_ativo:
            marker_id = marcador_ativo[0]

            cursor.execute("""
            UPDATE deficiency_markers
            SET status = 'ENCERRADO',
                closed_date = ?,
                last_assessment_id = ?
            WHERE id = ?
            """, (
                str(assessment_date),
                assessment_id,
                marker_id
            ))