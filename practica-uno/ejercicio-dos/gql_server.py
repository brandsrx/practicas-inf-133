from http.server import HTTPServer,BaseHTTPRequestHandler
import json
from graphene import ObjectType,Field,Mutation,String,Int,Boolean,List,Schema

class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura = Int()
    frutos = Boolean()
plantas = [
    Planta(
        id=1,
        nombre="Rosa",
        especie="Rosa sp.",
        edad=12,
        altura=30,
        frutos=False
    ),
    Planta(
        id=2,
        nombre="Manzano",
        especie="Malus domestica",
        edad=24,
        altura=150,
        frutos=True
    ),
    Planta(
        id=3,
        nombre="Tomate",
        especie="Solanum lycopersicum",
        edad=8,
        altura=60,
        frutos=True
    ),
]
class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()
    planta = Field(Planta)
    def mutate(root,info,nombre,especie,edad,altura,frutos):
        nueva_planta = Planta(
            id=len(plantas)+1,
            nombre=nombre,
            especie=especie,
            edad=edad,
            altura=altura,
            frutos=frutos
        )
        plantas.append(nueva_planta)
        return CrearPlanta(planta=nueva_planta)
class ActualizarPlanta(Mutation):
    class Arguments:
        id = Int()
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, id, nombre, especie, edad, altura, frutos):
        for planta in plantas:
            if planta.id == id:
                planta.nombre = nombre
                planta.especie = especie
                planta.edad = edad
                planta.altura = altura
                planta.frutos = frutos
                return ActualizarPlanta(planta=planta)
        return None
        
class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None
class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta().Field()
    actualizar_planta = ActualizarPlanta().Field()
    
class Query(ObjectType):
    plantas = List(Planta)
    planta_especie = Field(List(Planta),especie=String())
    planta_frutos = Field(List(Planta),frutos=String())

    def resolve_plantas(self, info):
        return plantas
    def resolve_planta_especie(self,info,especie):
        return [planta for planta in plantas if planta.especie == especie]
    def resolve_planta_frutos(self,info,frutos):
        return [planta for planta in plantas if planta.frutos == True]

schema = Schema(query=Query,mutation=Mutations)

class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()