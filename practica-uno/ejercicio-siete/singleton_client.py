import requests

URL = "http://localhost:8000"

def crear_partida(elemento):
    endpoint = f"{URL}/partidas"
    data = {"elemento": elemento}
    response = requests.post(endpoint, json=data)
    return response.json()

def listar_partidas():
    endpoint = f"{URL}/partidas"
    response = requests.get(endpoint)
    return response.json()

def listar_partidas_por_resultado(resultado):
    endpoint = f"{URL}/partidas?resultado={resultado}"
    response = requests.get(endpoint)
    return response.json()

if __name__ == "__main__":
    partida_creada = crear_partida("papel")
    print("Partida creada:", partida_creada)
    todas_las_partidas = listar_partidas()
    print("Todas las partidas:", todas_las_partidas)

    partidas_ganadas = listar_partidas_por_resultado("ganó")
    print("Partidas ganadas:", partidas_ganadas)
