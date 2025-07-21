# Desafio técnico Laboratório Nuven - Desenvolvedor IA
Este projeto implementa um pipeline de processamento de documentos (PDFs e imagens), extração de texto com OCR, vetorização semântica, indexação com FAISS e resposta automática a perguntas usando uma LLM (Flan-T5-small). O objetivo é permitir a consulta inteligente de conteúdos extraídos do Código de Obras de Eusébio, por meio de perguntas em linguagem natural.

🧱 Estrutura do Projeto
bash
Copiar
Editar
projetonuven/
├── entrada/            # Arquivos originais (.pdf, .jpg, .webp, etc)
├── saida/              # Textos extraídos (formato .txt)
├── chunks/             # (opcional) Pasta onde seriam salvos os pedaços de texto
├── preprocess.py       # Etapa 1: Extração de texto (OCR + leitura de PDF)
├── indexacao.py        # Etapa 2: Embeddings + indexação FAISS
├── consulta.py         # Etapa 3: Consulta + geração de resposta via LLM
├── index_faiss.index   # Arquivo gerado com índice vetorial FAISS
└── nomes_chunks.txt    # Lista com os nomes e ordem dos chunks
🚀 Execução
1. Pré-requisitos
Python 3.8+

Tesseract OCR instalado (link)

Instalar as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
2. Etapas
▶️ Etapa 1 - Extração de texto:
bash
Copiar
Editar
python preprocess.py
Entrada: arquivos em entrada/

Saída: textos .txt em saida/

PDFs são classificados automaticamente como nativos ou imagem

Imagens usam OCR com pré-processamento

Tabelas são extraídas com img2table

▶️ Etapa 2 - Indexação:
bash
Copiar
Editar
python indexacao.py
Divide os textos em chunks de 500 caracteres com sobreposição

Gera vetores semânticos com o modelo all-MiniLM-L6-v2

Indexa os vetores com FAISS

Salva index_faiss.index e nomes_chunks.txt

▶️ Etapa 3 - Consulta com LLM:
bash
Copiar
Editar
python consulta.py
O usuário faz uma pergunta (em português)

O sistema busca os top 5 chunks mais relevantes

Uma LLM (Flan-T5-small) gera uma resposta com base nesses trechos

🤖 Decisões Técnicas
OCR + pré-processamento: melhora acurácia do pytesseract, convertendo para tons de cinza, aumentando contraste e eliminando ruído.

img2table: usado como tentativa de extrair tabelas de imagens.

SentenceTransformer: usado para embeddings semânticos compactos e eficientes.

FAISS: biblioteca de busca vetorial de alta performance.

LLM (Flan-T5-small): gera respostas coesas a partir do conteúdo indexado, com ótimo custo-benefício para o desafio.

Chunking com sobreposição: evita perda de contexto entre divisões de texto.

📌 Observações
O foco foi construir um pipeline técnico funcional e claro, como sugerido no desafio.

As funções foram organizadas para facilitar o reuso, modificação e depuração.

O código pode ser facilmente adaptado para outros contextos de documentos ou modelos LLM maiores (como flan-t5-base ou mistral).

✅ Exemplo de uso
bash
Copiar
Editar
Pergunte algo: O que é necessário para obter o "Habite-se" segundo o Código de Obras de Eusébio?

Resposta:
Para obter o "Habite-se", a obra deve estar concluída, o proprietário deve solicitá-lo junto ao município e ela passará por vistoria. Também é necessário que atenda aos regulamentos e às exigências de segurança contra incêndio estabelecidas pelo Corpo de Bombeiros.
Se quiser, posso gerar também um requirements.txt com as dependências detectadas a partir dos imports. Deseja isso?
