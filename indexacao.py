#bibliotecas
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# caminho da pasta com os .txt gerados
pasta_txt = r"C:\Users\gu1lh\Desktop\projetonuven\saida"
# pasta onde será salvo os chunks
pasta_chunks = r"C:\Users\gu1lh\Desktop\projetonuven\chunks"

# para o embeddings:
modelo = SentenceTransformer('all-MiniLM-L6-v2')

# função das chunks
def dividir_em_chunks(texto, tamanho=500, sobreposicao=50):
    chunks = []
    inicio = 0

    while inicio < len(texto):
        fim = min(inicio + tamanho, len(texto))
        chunk = texto[inicio:fim]
        chunks.append(chunk)
        inicio += tamanho - sobreposicao
    
    return chunks

todos_chunks = []
nomes_chunks = []

# pecorre todos os arquivos da pasta
for nome_arquivo in os.listdir(pasta_txt):
    if nome_arquivo.endswith(".txt"):
        caminho = os.path.join(pasta_txt, nome_arquivo)
        with open(caminho, "r", encoding="utf-8") as arquivo:
            texto = arquivo.read()
        
        chunks = dividir_em_chunks(texto)
        
        for i, chunk in enumerate(chunks):
            todos_chunks.append(chunk)
            nomes_chunks.append(f"{nome_arquivo}_chunk{i}")

# gerar embeddings
vetores = modelo.encode(todos_chunks)

# converter vetores para formato FAISS
vetores_np = np.array(vetores).astype("float32")

# criar e preencher o índice vetorial FAISS
d = vetores_np.shape[1]
index = faiss.IndexFlatL2(d)
index.add(vetores_np)

# salva o indice e os nomes dos chunks
faiss.write_index(index, "index_faiss.index")

with open("nomes_chunks.txt", "w", encoding="utf-8") as f:
    for nome in nomes_chunks:
        f.write(nome + "\n")

print(f"Indexação concluída com {len(vetores_np)} chunks.")