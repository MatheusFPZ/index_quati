from datasets import load_dataset
import json

# Carregar dataset
quati_1M_passages = load_dataset("unicamp-dl/quati", "quati_1M_passages", trust_remote_code=True)
dataset = quati_1M_passages["quati_1M_passages"]

# Converter para lista de dicionários corretamente
lista_de_documentos = [dict(doc) for doc in dataset]

# Salvar como lista JSON
with open("quati_1M_passages.json", "w", encoding="utf-8") as f:
    json.dump(lista_de_documentos, f, ensure_ascii=False)
