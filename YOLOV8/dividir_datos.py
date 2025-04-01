import os
import glob
import shutil
import random

def dividir_datos(origen, destino, proporciones):
    categorias = ["tradicional", "popular", "inspiracion", "fantasia"]
    
    for categoria in categorias:
        ruta_origen = os.path.join(origen, categoria)
        imagenes = []
        patrones = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "*.tiff"]
        
        for patron in patrones:
            imagenes.extend(glob.glob(os.path.join(ruta_origen, patron)))
        
        random.shuffle(imagenes)
        
        num_train = int(len(imagenes) * proporciones["train"])
        num_val = int(len(imagenes) * proporciones["val"])
        
        conjuntos = {
            "train": imagenes[:num_train],
            "val": imagenes[num_train:num_train + num_val],
            "test": imagenes[num_train + num_val:]
        }
        
        for conjunto, archivos in conjuntos.items():
            ruta_destino = os.path.join(destino, conjunto, categoria)
            os.makedirs(ruta_destino, exist_ok=True)
            
            for archivo in archivos:
                shutil.move(archivo, os.path.join(ruta_destino, os.path.basename(archivo)))
                print(f"Movido {archivo} a {ruta_destino}")

# Definir rutas
carpeta_origen = r"C:\\Users\\dalil\\OneDrive\\Escritorio\\Tesis 2025\\images\\fuente-externa"
carpeta_destino = r"C:\\Users\\dalil\\OneDrive\\Escritorio\\Tesis 2025\\Tutorial yolo\\dataset"
proporciones = {"train": 0.7, "val": 0.2, "test": 0.1}

dividir_datos(carpeta_origen, carpeta_destino, proporciones)
