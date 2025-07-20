#bibliotecas
import os
import fitz
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# ****FUNÇÕES****

# extrair texto de pdf nativo
def extrair_texto_pdf_nativo(caminho_pdf):
    texto = ""
    
    with fitz.open(caminho_pdf) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    
    return texto.strip()

# extrair texto de pdf escaneado 
def extrair_texto_pdf_imagem(caminho_pdf):
    imagens = convert_from_path(caminho_pdf)
    texto = ""

    for imagem in imagens:
        # preprocessamento
        imagem = imagem.convert("L")
        imagem = imagem.point(lambda x: 0 if x < 150 else 255)

        texto += pytesseract.image_to_string(imagem, lang='por')

    return texto.strip()

# extrair texto de imagens
def extrair_texto_imagem(caminho_imagem):
    #preprocessamento
    imagem = Image.open(caminho_imagem).convert("L")
    imagem = imagem.point(lambda x: 0 if x < 150 else 255)

    texto = pytesseract.image_to_string(imagem, lang='por')
    
    return texto.strip()

# salvar o texto extraido em .txt
def salvar_texto(texto, caminho_saida):
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(texto)

# detectar se um PDF tem texto nativo ou precisa de OCR
def detectar_tipo_pdf(caminho_pdf):
    with fitz.open(caminho_pdf) as doc:
        for pagina in doc:
            if pagina.get_text().strip():
                return "pdf_nativo"
            
    return "pdf_imagem"

# processar PDF ou imagem
def processar_arquivo(caminho_arquivo, pasta_saida):
    nome_base = os.path.splitext(os.path.basename(caminho_arquivo))[0]
    caminho_saida = os.path.join(pasta_saida, f'{nome_base}.txt')

    if caminho_arquivo.endswith(".pdf"):
        tipo = detectar_tipo_pdf(caminho_arquivo)
        if tipo == "pdf_nativo":
            texto = extrair_texto_pdf_nativo(caminho_arquivo)
        else:
            texto = extrair_texto_pdf_imagem(caminho_arquivo)
    
    elif caminho_arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
        texto = extrair_texto_imagem(caminho_arquivo)
    
    else:
        print(f"Tipo de arquivo não suportado: {caminho_arquivo}")
        return
    
    salvar_texto(texto, caminho_saida)
    print(f"Processamento concluído! Texto salvo em: {caminho_saida}" )


# caminhos de entrada e saida
pasta_entrada = r"C:\Users\gu1lh\Desktop\projetonuven\entrada"
pasta_saida = r"C:\Users\gu1lh\Desktop\projetonuven\saida"
    
# rodar em todos os arquivos da entrada
if __name__ == "__main__":
    arquivos = os.listdir(pasta_entrada)

    for arquivo in arquivos:
        caminho = os.path.join(pasta_entrada, arquivo)
        processar_arquivo(caminho, pasta_saida)

