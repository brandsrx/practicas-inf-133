import requests
import json

URL = "http://localhost:8000/animales"

def crear_animal(nombre, especie, tipo,genero, edad, peso):
    data = {
        "nombre": nombre,
        "especie": especie,
        "tipo":tipo,
        "genero": genero,
        "edad": edad,
        "peso": peso
    }
    response = requests.post(URL, json=data)
    return response.json()

def listar_animales():
    response = requests.get(URL)
    return response.json()

def buscar_animales_por_especie(especie):
    params = {"especie": especie}
    response = requests.get(URL, params=params)
    return response.json()

def buscar_animales_por_genero(genero):
    params = {"genero": genero}
    response = requests.get(URL, params=params)
    return response.json()

def actualizar_animal(id, nombre, especie,tipo, genero, edad, peso):
    url = f"{URL}/{id}"
    data = {
        "nombre": nombre,
        "especie": especie,
        "tipo":tipo,
        "genero": genero,
        "edad": edad,
        "peso": peso
    }
    response = requests.put(url, json=data)
    return response.json()

def eliminar_animal(id):
    url = f"{URL}/{id}"
    response = requests.delete(url)
    return response.json()

if __name__ == "__main__":
    nuevo_animal = crear_animal("León","tiburonzin", "Pez", "Masculino", 5, 150)
    print(nuevo_animal)
    animales = listar_animales()
    print(animales)

    felinos = buscar_animales_por_especie("Pez")
    print(felinos)
    genero = buscar_animales_por_genero("hembra")
    print(genero)

    animal_actualizado = actualizar_animal(1, "Rana","rana", "Reptil", "Hembra", 6, 160)
    print( animal_actualizado)
    resultado = eliminar_animal(2)
    print( resultado)
