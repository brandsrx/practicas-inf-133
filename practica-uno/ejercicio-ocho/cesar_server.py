import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class Message:
    def __init__(self, id, contenido):
        self.id = id
        self.contenido = contenido
        self.contenido_encriptado = self.encriptar_contenido(contenido)

    def encriptar_contenido(self, contenido):
        contenido_encriptado = ''
        for char in contenido:
            if char.isalpha():
                ascii_code = ord(char)
                shifted_ascii_code = ascii_code + 3
                if char.islower():
                    if shifted_ascii_code > ord('z'):
                        shifted_ascii_code -= 26
                elif char.isupper():
                    if shifted_ascii_code > ord('Z'):
                        shifted_ascii_code -= 26
                contenido_encriptado += chr(shifted_ascii_code)
            else:
                contenido_encriptado += char
        return contenido_encriptado

class MessageAPI:
    def __init__(self):
        self.messages = []
        self.id_counter = 1

    def create_message(self, contenido):
        message = Message(self.id_counter, contenido)
        self.messages.append(message)
        self.id_counter += 1
        return message

    def list_messages(self):
        return self.messages

    def get_message_by_id(self, id):
        for message in self.messages:
            if message.id == id:
                return message
        return None

    def update_message(self, id, contenido):
        message = self.get_message_by_id(id)
        if message:
            message.contenido = contenido
            message.contenido_encriptado = message.encriptar_contenido(contenido)

    def delete_message(self, id):
        self.messages = [message for message in self.messages if message.id != id]

class MessageRequestHandler(BaseHTTPRequestHandler):
    api = MessageAPI()

    def do_POST(self):
        if self.path == "/mensajes":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            contenido = data.get('contenido')
            message = self.api.create_message(contenido)
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(message.__dict__).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/mensajes":
            messages = self.api.list_messages()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps([message.__dict__ for message in messages]).encode('utf-8'))
        elif self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[2])
            message = self.api.get_message_by_id(id)
            if message:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(message.__dict__).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[2])
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data.decode('utf-8'))
            contenido = data.get('contenido')
            self.api.update_message(id, contenido)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Mensaje actualizado correctamente"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[2])
            self.api.delete_message(id)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Mensaje eliminado correctamente"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, MessageRequestHandler)
    print(f'Servidor iniciado en el puerto {port}...')
    httpd.serve_forever()
