# Desafio Técnico - Laboratório Nuven (Desenvolvedor IA)

Este projeto implementa um pipeline completo para processamento de documentos (PDFs e imagens), realizando extração de texto via OCR (quando necessário), chunking, vetorização semântica, recuperação de informações baseada em similaridade vetorial e geração de respostas com uma LLM, com base nos documentos indexados.

## Estrutura de diretórios

```
projetonuven/
├── entrada/ # PDFs e imagens originais
├── saida/ # Textos extraídos (.txt)
├── index_faiss.index # Índice vetorial salvo
├── nomes_chunks.txt # Mapeamento nome do chunk
├── preprocess.py
├── indexacao.py
├── consulta.py
└── README.md
```

## Tecnologias utilizadas

- **Tesseract OCR** – para extração de texto de imagens/PDFs escaneados
- **pdf2image / PyMuPDF (fitz)** – para lidar com PDFs nativos e convertê-los em imagens
- **img2table** – extração estruturada de tabelas a partir de imagens
- **FAISS** – indexação e busca vetorial eficiente
- **Sentence Transformers (all-MiniLM-L6-v2)** – para geração de embeddings semânticos
- **Transformers (HuggingFace)** – para resposta automática via LLM, usando o modelo "flan-t5-small" por leve e rápido

## Arquitetura do pipeline
o projeto foi dividido nas seguintes etapas:

1. **Pré-processamento (`preprocess.py`)**
   - Detecta se o arquivo é um PDF nativo, PDF escaneado ou imagem.
   - Aplica OCR (PDF escaneado, imagem) ou extração direta com `fitz` (PDF nativo).
   - Realiza ajustes de contraste e filtro de ruído em imagens.
   - Salva os textos processados em `.txt`.

2. **Indexação (`indexacao.py`)**
   - Divide o conteúdo em chunks com sobreposição, para não ter perda de contexto.
   - Gera embeddings semânticos usando `SentenceTransformer`.
   - Indexa vetores com FAISS para recuperação eficiente.
   - Salva os nomes dos chunks e o índice vetorial.
                
3. **Consulta (`consulta.py`)**
   - Recebe uma pergunta do usuário.
   - Converte a pergunta em embedding e busca os chunks mais semelhantes (recupera 5 para melhor contextualização).
   - Usa uma LLM (Flan-T5-Small) para gerar a resposta com base nos trechos encontrados.
