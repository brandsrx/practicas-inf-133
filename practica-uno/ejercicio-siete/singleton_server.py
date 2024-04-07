import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
class JuegoPiedraPapelTijera:
    @staticmethod
    def jugar(elemento_jugador):
        elementos = ['piedra', 'papel', 'tijera']
        elemento_servidor = random.choice(elementos)
        
        if elemento_jugador == elemento_servidor:
            resultado = 'empató'
        elif (elemento_jugador == 'piedra' and elemento_servidor == 'tijera') or \
             (elemento_jugador == 'tijera' and elemento_servidor == 'papel') or \
             (elemento_jugador == 'papel' and elemento_servidor == 'piedra'):
            resultado = 'ganó'
        else:
            resultado = 'perdió'
        
        return elemento_servidor, resultado
class PartidasManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.partidas = []
            cls._instance.id_counter = 1
        return cls._instance

    def crear_partida(self, elemento_servidor, resultado):
        partida = {"id": self.id_counter, "elemento_servidor": elemento_servidor, "resultado": resultado}
        self.partidas.append(partida)
        self.id_counter += 1
        return partida

    def listar_partidas(self):
        return self.partidas

    def listar_partidas_por_resultado(self, resultado):
        return [partida for partida in self.partidas if partida["resultado"] == resultado]
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/partidas":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            elemento_jugador = json.loads(post_data.decode())["elemento"]
            elemento_servidor, resultado = JuegoPiedraPapelTijera.jugar(elemento_jugador)
            partida = PartidasManager().crear_partida(elemento_jugador, resultado)

            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(partida).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/partidas":
            partidas = PartidasManager().listar_partidas()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(partidas).encode("utf-8"))
        elif self.path.startswith("/partidas?resultado="):
            resultado = parse_qs(urlparse(self.path).query)["resultado"][0]
            partidas_por_resultado = PartidasManager().listar_partidas_por_resultado(resultado)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(partidas_por_resultado).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Iniciando servidor...')
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()