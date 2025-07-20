#bibliotecas
import os

# caminho da pasta com os .txt gerados
pasta_txt = r"C:\Users\gu1lh\Desktop\projetonuven\saida"

# lista para guardar os coteúdos
textos = []

# pecorre todos os arquivos da pasta
for nome_arquivo in os.listdir(pasta_txt):
    if nome_arquivo.endswith(".txt"):
        caminho = os.path.join(pasta_txt, nome_arquivo)
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            textos.append(conteudo)
        
        print(f"Carregado: {nome_arquivo}")