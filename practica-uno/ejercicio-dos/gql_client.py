import requests

url = 'http://localhost:8000/graphql'
#Creando una planta
creando_planta = """
mutation{
    crearPlanta(
        nombre: "Nuevo Nombre",
        especie: "Nueva Especie",
        edad: 10,
        altura: 50,
        frutos: true
    ) {
        planta {
            id
        }
    }
}
"""

response = requests.post(url, json={'query': creando_planta})
print(response.text)
# #Listando todas las plantas
listando_plantas = """
{
    plantas{
        id
        nombre
        especie
        edad
        altura
        frutos
    }
}
"""

response = requests.post(url, json={'query': listando_plantas})
print(response.text)
#Buscando plantas por especie
buscando_plantas = """
{
    plantaEspecie(especie:"Rosa sp."){
        id
        nombre
        especie
        edad
        altura
        frutos
    }
}
"""

response = requests.post(url, json={'query': buscando_plantas})
print(response.text)
#Buscnado plantas que tienen frutos
buscando_plantas = """
{
    plantaFrutos(frutos:"true"){
        id
        nombre
        especie
        edad
        altura
        frutos
    }
}
"""

response = requests.post(url, json={'query': buscando_plantas})
print(response.text)
#Actualizar Planta
actualizar_planta = """
mutation{
    actualizarPlanta(
        id:1,
        nombre: "Nuevo Nombre",
        especie: "Nueva Especie",
        edad: 10,
        altura: 50,
        frutos: true
    ) {
        planta {
            id
        }
    }
}
"""

response = requests.post(url, json={'query': actualizar_planta})
print(response.text)
#Eliminando una planta
eliminando_planta = """
mutation{
    deletePlanta(id:2) {
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""

response = requests.post(url, json={'query': eliminando_planta})
print(response.text)