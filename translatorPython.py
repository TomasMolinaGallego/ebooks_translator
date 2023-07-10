from googletrans import Translator
from bs4 import BeautifulSoup
import tempfile
import os
import shutil
from os.path import isfile, join
import patoolib
import shutil
from tkinter.filedialog import askopenfilename
from multiprocessing import Pool
import random

from time import sleep
from tqdm import tqdm
 

#Variables
tags_a_traducir=['p','h1', 'h2','li']
out_path= tempfile.gettempdir() + "\\" + str(random.randrange(100000, 999999))
translator = Translator()

def funcion_principal(file_name):
    with open(out_path+"\\OEBPS\\Text\\"+file_name, encoding='utf-8', mode="r+") as file:
        data=file.read()
        print("Traduciendo el fichero "+ file_name)
        content_traducido = parsear_y_traducir(data)
        file.truncate(0)
        file.write(content_traducido)
        print("Fichero traducido")

def parsear_y_traducir(data):
    #Obtiene la sopa del xhtml actual
    soup = BeautifulSoup(data, 'html.parser')
    #Y tambien una instancia en string
    content_capitulo = str(soup)
    #Por cada tag que se tenga que traducir hará una iteración
    for tag in tags_a_traducir:
        #Encontrará en la sopa todas las coincidencias que haya en xhtml para tratarlas individualmente
        all_coincidencias_tag = soup.find_all(tag)
        for coincidencia_tag in all_coincidencias_tag:
            try:
                #Por cada coincidencia de la tag, la traducirá y sustituirá el texto antiguo por el traducido
                parrafo_con_traducir=translator.translate(coincidencia_tag, dest="es").text
                content_capitulo = content_capitulo.replace(str(coincidencia_tag), parrafo_con_traducir)
            except Exception as e: 
                print(e)
                print(coincidencia_tag)
    return content_capitulo

filename_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
filename = (filename_path.rsplit("/", 1)) #Divide para coger la raíz de la ruta y el nombre del fichero
#Extrae el fichero epub de la ruta indicada y lo deja en el out_path 
print("Traduciendo el ebook: " + filename[1])
os.mkdir(out_path)
patoolib.extract_archive(filename_path, outdir=out_path, verbosity=-1)
#Saca todos los ficheros del directorio donde se han extraido las cosas

onlyfiles = [f for f in os.listdir(out_path+"\\OEBPS\\Text\\") if isfile(join(out_path+"\\OEBPS\\Text\\", f))]
list_files=os.listdir(path=out_path+"\\OEBPS\\Text\\")

for file_name in tqdm(list_files, desc="Translating..."):
    with open(out_path+"\\OEBPS\\Text\\"+file_name, encoding='utf-8', mode="r+") as file:
        data=file.read()
        #print("Traduciendo el fichero "+ file_name)
        content_traducido = parsear_y_traducir(data)
        file.truncate(0)
        file.write(content_traducido)
        #print("Fichero traducido")

zip_file = shutil.make_archive(filename[0]+"\\traduccion\\"+filename[1], 'zip', out_path)
pre, ext = os.path.splitext(zip_file)
os.rename(zip_file, pre+".epub")
shutil.rmtree(out_path)
print("Ebook terminado de traducir")
