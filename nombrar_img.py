import os

def renombrar_imagenes(carpeta, inicio, sigue, index=1):
    # Obtener una lista de archivos en la carpeta
    archivos = os.listdir(carpeta)
    
    # Filtrar solo los archivos que son imágenes (puedes ajustar las extensiones según tus necesidades)
    extensiones_imagen = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    imagenes = [archivo for archivo in archivos if archivo.lower().endswith(extensiones_imagen)]
    
    # Calcular cuántos ceros a la izquierda (padding) se necesita según el número total de imágenes
    padding = len(str(index + len(imagenes) - 1))
    
    # Renombrar cada imagen
    for i, imagen in enumerate(imagenes):
        # Obtener la extensión del archivo original
        extension = os.path.splitext(imagen)[1]
        
        # Crear el nuevo nombre con padding
        nuevo_nombre = f"IMG{str(index + i).zfill(4)}_{inicio}_{sigue}{extension}"
        
        # Obtener las rutas completas (anterior y nueva)
        ruta_anterior = os.path.join(carpeta, imagen)
        ruta_nueva = os.path.join(carpeta, nuevo_nombre)
        
        # Renombrar el archivo
        os.rename(ruta_anterior, ruta_nueva)
        print(f"Renombrado: {imagen} -> {nuevo_nombre}")

# Ejemplo de uso:
renombrar_imagenes("F:\\Kygua-20241011T001126Z-001", "TRA", "FE", 4426)
