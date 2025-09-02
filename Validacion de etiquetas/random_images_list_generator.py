import random
from google.cloud import storage

# Inicializar el cliente de GCS
cliente = storage.Client()
nombre_bucket = "trajes-danza-paraguaya"
bucket = cliente.get_bucket(nombre_bucket)
categorias = ["POP", "TRA", "INF", "FAN"]
imagenes_por_categoria = 25
cantidad_de_conjuntos = 3

# Función para filtrar imágenes por categoría
def filtrar_imagenes_por_categoria(rutas, categoria):
    return [ruta for ruta in rutas if categoria in ruta]

# Obtener todas las rutas de imágenes
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

# Guardar los conjuntos en archivos
for i, conjunto in enumerate(conjuntos, 1):
    nombre_archivo = f"conjunto_aleatorio_{i}.txt"
    with open(nombre_archivo, "w") as archivo:
        for ruta in conjunto:
            archivo.write(f"gs://{nombre_bucket}/{ruta}\n")
    print(f"Conjunto {i} guardado en {nombre_archivo}")