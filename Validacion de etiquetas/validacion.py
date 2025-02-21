import json
import glob
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse, unquote
import csv

def cargar_json(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def extraer_etiquetas(datos_json):
    etiquetas = {}
    for elemento in datos_json:
        id_imagen = elemento['data']['image']
        if id_imagen.startswith("https:"):
            id_imagen = id_imagen.split("?")[0]
            id_imagen = id_imagen.replace("https://storage.googleapis.com", "gs:/")
        etiqueta = elemento['annotations'][0]['result'][0]['value']['choices'][0]
        etiquetas[id_imagen] = etiqueta
    ## print("Ejemplo de etiquetas extraídas:", list(etiquetas.items())[:5])
    return etiquetas

def generar_informe(grupo, referencia, etiquetas_expertos, nombres_expertos):
    nombre_archivo = f"informe_validacion_grupo_{grupo}.csv"
    with open(nombre_archivo, mode='w', encoding='utf-8', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["ID Imagen", "Etiqueta Original"] + nombres_expertos)

        for id_imagen, etiqueta_real in referencia.items():
            etiquetas_validadas = [etiquetas.get(id_imagen, "No etiquetado") for etiquetas in etiquetas_expertos]
            escritor.writerow([id_imagen, etiqueta_real] + etiquetas_validadas)

    print(f"Informe generado: {nombre_archivo}")

def calcular_concordancia(referencia, etiquetas_expertos):
    total_imagenes = len(referencia)
    if total_imagenes == 0:
        return 0.0, {"correcto": 0, "incorrecto": 0}
    
    conteo_correctos = Counter()
    
    for id_imagen, etiqueta_real in referencia.items():
        votos_expertos = [etiquetas.get(id_imagen) for etiquetas in etiquetas_expertos if id_imagen in etiquetas]
        if votos_expertos.count(etiqueta_real) >= 2:
            conteo_correctos["correcto"] += 1
        else:
            conteo_correctos["incorrecto"] += 1

    porcentaje_correcto = (conteo_correctos["correcto"] / total_imagenes) * 100
    return porcentaje_correcto, conteo_correctos

def calcular_concordancia_individual(referencia, etiquetas_expertos):
    total_imagenes = len(referencia)
    if total_imagenes == 0:
        return {}, {}
    
    porcentajes = {}
    detalles_expertos = {}
    for i, etiquetas in enumerate(etiquetas_expertos):
        correctos = sum(1 for id_img, etiqueta_real in referencia.items() if etiquetas.get(id_img) == etiqueta_real)
        porcentajes[f"Experto_{i+1}"] = (correctos / total_imagenes) * 100
        detalles_expertos[f"Experto_{i+1}"] = {
            "correctos": correctos,
            "incorrectos": total_imagenes - correctos
        }
    return porcentajes, detalles_expertos

def main():
    archivo_referencia = 'original.json'
    etiquetas_original = extraer_etiquetas(cargar_json(archivo_referencia)).items()
    archivos_expertos = sorted(glob.glob('validacion_grupo*_*.json'))
    
    grupos = {}
    nombres_expertos = []
    index_experto = 0
    for archivo in archivos_expertos:
        id_grupo = archivo.split('_')[1]
        id_experto = archivo.split('_')[2].split('.')[0]
        if id_grupo not in grupos:
            grupos[id_grupo] = []
        grupos[id_grupo].append(archivo)
        if id_experto not in nombres_expertos:
            nombres_expertos.append(id_experto)
    
    porcentajes = 0
    for grupo, archivos in grupos.items():
        etiquetas_expertos = [extraer_etiquetas(cargar_json(archivo)) for archivo in archivos]
        imagenes_muestra = set(etiquetas_expertos[0].keys()) if etiquetas_expertos else set()
        referencia = {k: v for k, v in etiquetas_original if k in imagenes_muestra}
        
        if not referencia:
            print(f"Grupo {grupo} - No hay imágenes en la muestra, no se puede calcular la concordancia.")
            print("-" * 40)
            continue
        generar_informe(grupo, referencia, etiquetas_expertos, nombres_expertos)
        
        porcentaje_correcto, conteo_correctos = calcular_concordancia(referencia, etiquetas_expertos)
        concordancia_individual, detalles_expertos = calcular_concordancia_individual(referencia, etiquetas_expertos)
        porcentajes += porcentaje_correcto

        print(f"Grupo {grupo} - Porcentaje Correcto: {porcentaje_correcto:.2f}%")
        print(f"Imágenes Correctas: {conteo_correctos['correcto']}, Imágenes Incorrectas: {conteo_correctos['incorrecto']}")
        print("Concordancia Individual de Expertos:")
        for experto, porcentaje in concordancia_individual.items():
            print(f"  {nombres_expertos[index_experto]}: {porcentaje:.2f}% (Correctos: {detalles_expertos[experto]['correctos']}, Incorrectos: {detalles_expertos[experto]['incorrectos']})")
            index_experto += 1
        print("-" * 40)
    
    porcentajes = porcentajes / 3
    print (f"Porcentaje de etiquetas correctas: {porcentajes:.2f}%")

if __name__ == "__main__":
    main()
