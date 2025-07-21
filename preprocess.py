# bibliotecas
import os
import fitz
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from img2table.document import Image as Img2TableImage
from img2table.ocr import TesseractOCR
import pandas as pd
import cv2

# configuração do tesseract 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ****FUNÇÕES****

# preprocessar a imagem
def preprocess_imagem(image):
    img = image.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    width, height = img.size
    img = img.resize((width*2, height*2), Image.LANCZOS)
    img = img.point(lambda x: 0 if x < 140 else 255)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    return img

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
        imagem = preprocess_imagem(imagem)
        texto += pytesseract.image_to_string(imagem, lang='por', config='--oem 3 --psm 6 -c preserve_interword_spaces=1')
    return texto.strip()

# extrair texto de imagens
def extrair_texto_imagem(caminho_imagem):
    try:
        ocr_engine = TesseractOCR(lang="por")
        img_doc = Img2TableImage(src=caminho_imagem)
        extracted_tables = img_doc.extract_tables(ocr=ocr_engine)
        
        if extracted_tables:
            df = extracted_tables[0].df
            df.replace('', pd.NA, inplace=True)
            df.dropna(how='all', inplace=True)
            df.dropna(axis=1, how='all', inplace=True)
            texto = df.to_markdown(index=False, tablefmt="grid")
        else:
            imagem = Image.open(caminho_imagem)
            imagem = preprocess_imagem(imagem)
            texto = pytesseract.image_to_string(imagem, lang='por', config='--oem 3 --psm 6')
    except Exception as e:
        imagem = Image.open(caminho_imagem)
        texto = pytesseract.image_to_string(imagem, lang='por')
        texto = f"AVISO: Erro no processamento ({str(e)}). OCR básico:\n\n{texto}"
    return texto.strip()

# salvar o texto extraido em .txt
def salvar_texto(texto, caminho_saida):
    texto = texto.replace(',,', ',').replace(' .', '.').replace(' ,', ',')
    texto = '\n'.join([linha.strip() for linha in texto.split('\n') if linha.strip()])
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
        texto = extrair_texto_pdf_nativo(caminho_arquivo) if tipo == "pdf_nativo" else extrair_texto_pdf_imagem(caminho_arquivo)
    elif caminho_arquivo.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        texto = extrair_texto_imagem(caminho_arquivo)
    else:
        print(f"Tipo de arquivo não suportado: {caminho_arquivo}")
        return

    salvar_texto(texto, caminho_saida)
    print(f"Processamento concluído! Texto salvo em: {caminho_saida}")

# caminhos de entrada e saida
pasta_entrada = r"C:\Users\gu1lh\Desktop\projetonuven\entrada"
pasta_saida = r"C:\Users\gu1lh\Desktop\projetonuven\saida"

# rodar em todos os arquivos da entrada
if __name__ == "__main__":
    for arquivo in os.listdir(pasta_entrada):
        processar_arquivo(os.path.join(pasta_entrada, arquivo), pasta_saida)