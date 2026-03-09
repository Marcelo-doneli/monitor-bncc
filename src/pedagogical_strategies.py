def get_strategies_by_field(field):

    estrategias = {

        "O eu, o outro e o nós": [
            "Promover rodas de conversa sobre convivência.",
            "Propor brincadeiras cooperativas.",
            "Trabalhar atividades de empatia e respeito."
        ],

        "Corpo, gestos e movimentos": [
            "Realizar circuitos motores.",
            "Promover atividades com dança e música.",
            "Estimular jogos de equilíbrio e coordenação."
        ],

        "Traços, sons, cores e formas": [
            "Explorar pintura e desenho livre.",
            "Utilizar materiais diversos para expressão artística.",
            "Realizar atividades musicais com instrumentos."
        ],

        "Escuta, fala, pensamento e imaginação": [
            "Promover contação de histórias.",
            "Estimular dramatizações.",
            "Realizar jogos de linguagem e rimas."
        ],

        "Espaços, tempos, quantidades, relações e transformações": [
            "Realizar jogos de classificação e comparação.",
            "Explorar atividades com blocos e formas.",
            "Trabalhar contagem em brincadeiras."
        ]
    }

    return estrategias.get(field, [])