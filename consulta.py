import requests
import csv

# Consultas a serem executadas
consultas = [
    "Qual a maior característica da fauna brasileira?",
    "quais países europeus seguem o regime monarquista?",
    "quais os critérios de definição dos monumentos intitulados maravilhas do mundo moderno?",
    "Como o Brasil reagiu a epidemia de AIDS no fim do século XX?",
    "Qual a maior torcida de futebol do Brasil?"
]

# URL base do Solr
solr_url = "http://localhost:8983/solr/quati_core/select"

# Função para executar consulta no Solr e retornar os resultados
def executar_consulta(query, num_resultados=100):
    params = {
        'q': query,
        'rows': num_resultados,
        'fl': 'passage_id,score',  # Apenas id e score
        'wt': 'json',
        'df': 'passage',  # Campo padrão para busca
        'indent': 'true'
    }
    response = requests.get(solr_url, params=params)
    response.raise_for_status()  # Garante que a requisição foi bem-sucedida
    return response.json()

# Lista para armazenar os resultados
resultados = []
consultas_id = [1,9,11,13,15]

# Executar as consultas e coletar resultados
for consulta_id, consulta in zip(consultas_id, consultas):
    dados = executar_consulta(consulta)
    print(f"Consulta {consulta_id}: {consulta}")
    print(f"Resultados encontrados: {dados['response']['numFound']}")
    
    for rank, doc in enumerate(dados['response']['docs'], start=1):
        resultado = {
            'número_da_consulta': consulta_id,
            'número_do_documento': doc['passage_id'],
            'ordem_no_ranking': rank,
            'score': doc['score'],
        }
        resultados.append(resultado)

# Salvar os resultados no CSV
with open('resultados_consultas.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['número_da_consulta', 'número_do_documento', 'ordem_no_ranking', 'score'])
    writer.writeheader()
    writer.writerows(resultados)

print("Resultados salvos em 'resultados_consultas.csv'")
