import json
from google.cloud import storage
from datetime import timedelta

# Función para generar la URL firmada
def generar_url_firmada(nombre_bucket, nombre_blob):
    cliente_storage = storage.Client()
    bucket = cliente_storage.bucket(nombre_bucket)
    blob = bucket.blob(nombre_blob)
    
    url = blob.generate_signed_url(expiration=timedelta(days=365), method="GET")
    
    return url

# Función para convertir las URLs gs:// a URLs firmadas en los datos JSON
def convertir_a_urls_firmadas(ruta_archivo_json, ruta_salida_json):

    with open(ruta_archivo_json, 'r') as archivo:
        datos = json.load(archivo)

    for item in datos:
        url_gs = item["data"]["image"]
        
        if url_gs.startswith("gs://"):
            ruta = url_gs[5:]  # Eliminar 'gs://'
            nombre_bucket, nombre_blob = ruta.split("/", 1)
            
            # Generar la URL firmada
            url_firmada = generar_url_firmada(nombre_bucket, nombre_blob)
            
            # Actualizar el JSON con la URL firmada
            item["data"]["image"] = url_firmada

    # Guardar los datos actualizados en un nuevo archivo
    with open(ruta_salida_json, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

    print(f"Las URLs firmadas se han escrito en {ruta_salida_json}")

ruta_archivo_json = 'conjunto_aleatorio_3.json'  
ruta_salida_json = 'conjunto_aleatorio_3_temp.json' 
convertir_a_urls_firmadas(ruta_archivo_json, ruta_salida_json)