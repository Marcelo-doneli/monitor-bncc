from src.db import get_connection


def get_children_with_deficiency_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        children.id,
        children.full_name,
        COUNT(assessments.id) as total_defasagens
    FROM assessments
    INNER JOIN children ON assessments.child_id = children.id
    WHERE assessments.deficiency = 'Sim'
    GROUP BY children.id, children.full_name
    ORDER BY total_defasagens DESC, children.full_name
    """)
    resultados = cursor.fetchall()
    conn.close()

    return resultados
def get_most_critical_bncc_objectives():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        bncc_objectives.code,
        bncc_objectives.field,
        bncc_objectives.age_group,
        bncc_objectives.description,
        COUNT(assessments.id) as total_defasagens
    FROM assessments
    INNER JOIN bncc_objectives ON assessments.objective_id = bncc_objectives.id
    WHERE assessments.deficiency = 'Sim'
    GROUP BY
        bncc_objectives.code,
        bncc_objectives.field,
        bncc_objectives.age_group,
        bncc_objectives.description
    ORDER BY total_defasagens DESC, bncc_objectives.code
    """)

    resultados = cursor.fetchall()
    conn.close()

    return resultados
def get_deficiency_by_field():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        bncc_objectives.field,
        COUNT(assessments.id) as total_defasagens
    FROM assessments
    INNER JOIN bncc_objectives ON assessments.objective_id = bncc_objectives.id
    WHERE assessments.deficiency = 'Sim'
    GROUP BY bncc_objectives.field
    ORDER BY total_defasagens DESC, bncc_objectives.field
    """)

    resultados = cursor.fetchall()
    conn.close()

    return resultados
def get_deficiency_by_class():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        classes.name,
        schools.name,
        COUNT(assessments.id) as total_defasagens
    FROM assessments
    INNER JOIN children ON assessments.child_id = children.id
    INNER JOIN child_class ON children.id = child_class.child_id
    INNER JOIN classes ON child_class.class_id = classes.id
    INNER JOIN schools ON classes.school_id = schools.id
    WHERE assessments.deficiency = 'Sim'
    GROUP BY classes.name, schools.name
    ORDER BY total_defasagens DESC, schools.name, classes.name
    """)

    resultados = cursor.fetchall()
    conn.close()

    return resultados