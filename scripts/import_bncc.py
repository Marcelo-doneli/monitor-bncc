from src.db import get_connection

def import_bncc():
    objetivos = [
        {
            "code": "EI01EO01",
            "field": "O eu, o outro e o nós",
            "age_group": "Bebês",
            "description": "Perceber que suas ações têm efeitos nas outras crianças e nos adultos."
        },
        {
            "code": "EI01CG01",
            "field": "Corpo, gestos e movimentos",
            "age_group": "Bebês",
            "description": "Movimentar as partes do corpo para exprimir corporalmente emoções, necessidades e desejos."
        },
        {
            "code": "EI01TS01",
            "field": "Traços, sons, cores e formas",
            "age_group": "Bebês",
            "description": "Explorar sons produzidos com o próprio corpo e com objetos do ambiente."
        },
        {
            "code": "EI02EO01",
            "field": "O eu, o outro e o nós",
            "age_group": "Crianças bem pequenas",
            "description": "Demonstrar atitudes de cuidado e solidariedade na interação com crianças e adultos."
        },
        {
            "code": "EI02EF01",
            "field": "Escuta, fala, pensamento e imaginação",
            "age_group": "Crianças bem pequenas",
            "description": "Dialogar com crianças e adultos, expressando seus desejos, necessidades, sentimentos e opiniões."
        },
        {
            "code": "EI02ET01",
            "field": "Espaços, tempos, quantidades, relações e transformações",
            "age_group": "Crianças bem pequenas",
            "description": "Explorar e descrever semelhanças e diferenças entre as características e propriedades dos objetos."
        },
        {
            "code": "EI03EO01",
            "field": "O eu, o outro e o nós",
            "age_group": "Crianças pequenas",
            "description": "Demonstrar empatia pelos outros, percebendo que as pessoas têm diferentes sentimentos, necessidades e maneiras de pensar e agir."
        },
        {
            "code": "EI03EF01",
            "field": "Escuta, fala, pensamento e imaginação",
            "age_group": "Crianças pequenas",
            "description": "Expressar ideias, desejos e sentimentos sobre suas vivências, por meio da linguagem oral e escrita."
        },
        {
            "code": "EI03CG01",
            "field": "Corpo, gestos e movimentos",
            "age_group": "Crianças pequenas",
            "description": "Criar com o corpo formas diversificadas de expressão de sentimentos, sensações e emoções."
        }
    ]

    conn = get_connection()
    cursor = conn.cursor()

    for objetivo in objetivos:
        cursor.execute("""
            INSERT INTO bncc_objectives (code, field, age_group, description)
            VALUES (?, ?, ?, ?)
        """, (
            objetivo["code"],
            objetivo["field"],
            objetivo["age_group"],
            objetivo["description"]
        ))

    conn.commit()
    conn.close()
    print("Objetivos da BNCC importados com sucesso.")

if __name__ == "__main__":
    import_bncc()