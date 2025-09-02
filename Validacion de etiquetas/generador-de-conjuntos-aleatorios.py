import random
import json
from google.cloud import storage
from datetime import timedelta

# Configuración inicial
nombre_bucket = "trajes-danza-paraguaya"
categorias = ["POP", "TRA", "INF", "FAN"]
imagenes_por_categoria = 25
cantidad_de_conjuntos = 3

# Función para generar una URL firmada
def generar_url_firmada(cliente_storage, nombre_bucket, nombre_blob):
    bucket = cliente_storage.bucket(nombre_bucket)
    blob = bucket.blob(nombre_blob)
    url = blob.generate_signed_url(expiration=timedelta(days=365), method="GET")
    return url

# Función para filtrar imágenes por categoría
def filtrar_imagenes_por_categoria(rutas, categoria):
    return [ruta for ruta in rutas if categoria in ruta]

# Inicializar cliente de GCS
cliente_storage = storage.Client()
bucket = cliente_storage.bucket(nombre_bucket)
todos_los_archivos = list(bucket.list_blobs())
todas_las_rutas = [blob.name for blob in todos_los_archivos if blob.name.endswith(('.jpg', '.png'))]

# Generar conjuntos
conjuntos = []
imagenes_usadas = set()

for numero_conjunto in range(cantidad_de_conjuntos):
    conjunto_actual = []
    for categoria in categorias:
        imagenes_categoria = [ruta for ruta in filtrar_imagenes_por_categoria(todas_las_rutas, categoria) if ruta not in imagenes_usadas]
        if len(imagenes_categoria) < imagenes_por_categoria:
            raise ValueError(f"No hay suficientes imágenes en la categoría {categoria} para generar el conjunto {numero_conjunto + 1}.")
        imagenes_seleccionadas = random.sample(imagenes_categoria, imagenes_por_categoria)
        conjunto_actual.extend(imagenes_seleccionadas)
        imagenes_usadas.update(imagenes_seleccionadas)
    conjuntos.append(conjunto_actual)

# Generar y guardar los archivos JSON formateados para Label Studio
for i, conjunto in enumerate(conjuntos, 1):
    datos_json = []
    for ruta in conjunto:
        url_firmada = generar_url_firmada(cliente_storage, nombre_bucket, ruta)
        entrada = {
            "data": {
                "image": url_firmada
            },
            "annotations": []
        }
        datos_json.append(entrada)

    nombre_archivo_json = f"conjunto_aleatorio_{i}.json"
    with open(nombre_archivo_json, "w") as archivo_json:
        json.dump(datos_json, archivo_json, indent=4)
    print(f"Conjunto {i} guardado en {nombre_archivo_json}")
