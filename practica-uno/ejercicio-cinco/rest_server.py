from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Animal:
    def __init__(self, id, nombre, especie, genero, edad, peso):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

class ZooAPI:
    def __init__(self):
        self.animales = []
        self.id_counter = 1
        self.crear_animal("Leonardo", "León", "Macho", 5, 150)
        self.crear_animal("Luna", "Tigre", "Hembra", 3, 120)
        
    def crear_animal(self, nombre, especie, genero, edad, peso):
        animal = Animal(self.id_counter, nombre, especie, genero, edad, peso)
        self.animales.append(animal)
        self.id_counter += 1
        return animal

    def listar_animales(self):
        return self.animales

    def buscar_animales_por_especie(self, especie):
        return [animal for animal in self.animales if animal.especie.lower() == especie.lower()]

    def buscar_animales_por_genero(self, genero):
        return [animal for animal in self.animales if animal.genero.lower() == genero.lower()]

    def actualizar_animal(self, id, nombre, especie, genero, edad, peso):
        for animal in self.animales:
            if animal.id == id:
                animal.nombre = nombre
                animal.especie = especie
                animal.genero = genero
                animal.edad = edad
                animal.peso = peso
                return animal
        return None

    def eliminar_animal(self, id):
        self.animales = [animal for animal in self.animales if animal.id != id]

class ZooRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            animal = api.crear_animal(data.get("nombre"), data.get("especie"), data.get("genero"), data.get("edad"), data.get("peso"))
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(animal.__dict__).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/animales":
            animales = api.listar_animales()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps([animal.__dict__ for animal in animales]).encode("utf-8"))
        elif self.path.startswith("/animales?especie="):
            especie = parse_qs(urlparse(self.path).query)["especie"][0]
            animales = api.buscar_animales_por_especie(especie)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps([animal.__dict__ for animal in animales]).encode("utf-8"))
        elif self.path.startswith("/animales?genero="):
            genero = parse_qs(urlparse(self.path).query)["genero"][0]
            animales = api.buscar_animales_por_genero(genero)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps([animal.__dict__ for animal in animales]).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[2])
            data = self.read_data()
            animal = api.actualizar_animal(animal_id, data.get("nombre"), data.get("especie"), data.get("genero"), data.get("edad"), data.get("peso"))
            if animal:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(animal.__dict__).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[2])
            api.eliminar_animal(animal_id)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Animal eliminado correctamente"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

if __name__ == "__main__":
    api = ZooAPI()
    port = ("", 8000)
    httpd = HTTPServer(port, ZooRequestHandler)
    print(f"Iniciando servidor web en http://localhost:{port}/")
    httpd.serve_forever()
