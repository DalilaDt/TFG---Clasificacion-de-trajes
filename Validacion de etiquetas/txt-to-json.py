import json

with open("conjunto_aleatorio_1.txt", "r") as archivo_txt:
    lineas = archivo_txt.read().splitlines()

datos_json = []
for ruta in lineas:
    entrada = {
        "data": {
            "image": ruta
        },
        "annotations": []
    }
    datos_json.append(entrada)

with open("conjunto_aleatorio_2.json", "w") as archivo_json:
    json.dump(datos_json, archivo_json, indent=4)


with open("conjunto_aleatorio_2.txt", "r") as archivo_txt:
    lineas = archivo_txt.read().splitlines()

datos_json = []
for ruta in lineas:
    entrada = {
        "data": {
            "image": ruta
        },
        "annotations": []
    }
    datos_json.append(entrada)

with open("conjunto_aleatorio_1.json", "w") as archivo_json:
    json.dump(datos_json, archivo_json, indent=4)


with open("conjunto_aleatorio_3.txt", "r") as archivo_txt:
    lineas = archivo_txt.read().splitlines()

datos_json = []
for ruta in lineas:
    entrada = {
        "data": {
            "image": ruta
        },
        "annotations": []
    }
    datos_json.append(entrada)

with open("conjunto_aleatorio_3.json", "w") as archivo_json:
    json.dump(datos_json, archivo_json, indent=4)
