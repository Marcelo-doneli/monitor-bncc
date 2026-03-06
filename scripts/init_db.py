from src.db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (school_id) REFERENCES schools (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS children (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        birth_date TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bncc_objectives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        field TEXT NOT NULL,
        age_group TEXT NOT NULL,
        description TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    objective_id INTEGER NOT NULL,
    assessment_date TEXT NOT NULL,
    learning_level TEXT NOT NULL,
    notes TEXT,
    deficiency TEXT,
    FOREIGN KEY (child_id) REFERENCES children (id),
    FOREIGN KEY (objective_id) REFERENCES bncc_objectives (id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS child_class (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER NOT NULL,
        class_id INTEGER NOT NULL,
        FOREIGN KEY (child_id) REFERENCES children (id),
        FOREIGN KEY (class_id) REFERENCES classes (id)
    )
    """)
    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso.")

if __name__ == "__main__":
    create_tables()