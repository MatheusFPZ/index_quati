import pysolr
import json
import time

# Configurações
SOLR_URL = 'http://localhost:8983/solr/quati_core2'  # Ajuste o nome do core, se necessário
JSON_FILE = 'quati_1M_passages.json'  # Arquivo JSON com documentos
BATCH_SIZE = 1000  # Tamanho do lote

# Conectar ao Solr
solr = pysolr.Solr(SOLR_URL, timeout=60)

def carregar_json_em_lotes(caminho_arquivo, batch_size):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        documentos = json.load(f)
        for i in range(0, len(documentos), batch_size):
            yield documentos[i:i + batch_size]

def indexar_documentos():
    total = 0
    start_time = time.time()  # ⏱️ Início da contagem
    for lote in carregar_json_em_lotes(JSON_FILE, BATCH_SIZE):
        # Ajuste os campos para garantir que passage_id e passage estão corretos
        for doc in lote:
            # Verifique se os campos são atribuídos corretamente
            doc['passage_id'] = doc.get('passage_id', '')  # Garantir que passage_id esteja no documento
            doc['passage'] = doc.get('passage', '')        # Garantir que passage esteja no documento
        
        try:
            solr.add(lote, commit=False)
            total += len(lote)
            print(f"{total} documentos indexados...")
        except Exception as e:
            print(f"Erro ao indexar lote: {e}")

    # Commit final
    try:
        solr.commit()
        print("✅ Commit final realizado.")
    except Exception as e:
        print(f"Erro no commit final: {e}")

    end_time = time.time()  # ⏱️ Fim da contagem
    tempo_total = end_time - start_time
    print(f"\n⏱️ Tempo total de indexação: {tempo_total:.2f} segundos")

# Executar
print("🔄 Iniciando indexação...")
indexar_documentos()
