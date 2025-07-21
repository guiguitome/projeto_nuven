# bibliotecas
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

modelo = SentenceTransformer('all-MiniLM-L6-v2')

# carregar índice de vetores
index = faiss.read_index("index_faiss.index")
with open("nomes_chunks.txt", "r", encoding="utf-8") as f:
    nomes_chunks = [linha.strip() for linha in f]

pasta_entrada = r"C:\Users\gu1lh\Desktop\projetonuven\saida"

pergunta = input("Pergunte algo: ")
# converter pergunta em vetor
vetor_pergunta = modelo.encode([pergunta])
vetor_pergunta = np.array(vetor_pergunta).astype("float32")

# busca dos chunks
k = 5
distancias, indices = index.search(vetor_pergunta, k)
trechos_encontrados = []

for idx in indices[0]:
    nome_arquivo = nomes_chunks[idx].split("_chunk")[0]
    chunk_id = int(nomes_chunks[idx].split("_chunk")[1])
    caminho_arquivo = os.path.join(pasta_entrada, nome_arquivo)

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        texto_completo = f.read()

        # Dividir o texto novamente em chunks para pegar só o trecho desejado
        chunks = []
        inicio = 0
        tamanho = 500
        sobreposicao = 50

        while inicio < len(texto_completo):
            fim = min(inicio + tamanho, len(texto_completo))
            chunk = texto_completo[inicio:fim]
            chunks.append(chunk)
            inicio += tamanho - sobreposicao

        trecho = chunks[chunk_id] if chunk_id < len(chunks) else ""

    print(f"{nomes_chunks[idx]}")
    print(trecho[:800])
    print()

    trechos_encontrados.append(trecho)


# carregar o modelo LLM (flan-t5-small)
modelo_llm = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")

# prompt
contexto = "\n".join(trechos_encontrados)
prompt = f"Com base no seguinte conteúdo extraído de documentos:\n\n{contexto}\n\nResponda à pergunta: {pergunta}"

# gerar resposta
inputs = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)
resposta_ids = modelo_llm.generate(**inputs, max_new_tokens=150)
resposta = tokenizer.decode(resposta_ids[0], skip_special_tokens=True)
# exbir resposta
print(f"\n{resposta}")