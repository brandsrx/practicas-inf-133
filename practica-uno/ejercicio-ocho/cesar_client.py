import requests
import json

class MessageClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_message(self, contenido):
        url = f"{self.base_url}/mensajes"
        data = {"contenido": contenido}
        response = requests.post(url, json=data)
        return response.json()

    def list_messages(self):
        url = f"{self.base_url}/mensajes"
        response = requests.get(url)
        return response.json()

    def get_message_by_id(self, message_id):
        url = f"{self.base_url}/mensajes/{message_id}"
        response = requests.get(url)
        return response.json()

    def update_message(self, message_id, contenido):
        url = f"{self.base_url}/mensajes/{message_id}"
        data = {"contenido": contenido}
        response = requests.put(url, json=data)
        return response.json()

    def delete_message(self, message_id):
        url = f"{self.base_url}/mensajes/{message_id}"
        response = requests.delete(url)
        return response.json()

if __name__ == "__main__":
    client = MessageClient("http://localhost:8000")
    
    nuevo_mensaje = client.create_message("Hola, mundo!")
    print("Mensaje creado:", nuevo_mensaje)

    mensajes = client.list_messages()
    print("Lista de mensajes:", mensajes)

    mensaje_id = nuevo_mensaje["id"]
    mensaje = client.get_message_by_id(mensaje_id)
    print("Mensaje por ID:", mensaje)

    mensaje_actualizado = client.update_message(mensaje_id, "Hola ")
    print("Mensaje actualizado:", mensaje_actualizado)

    resultado_eliminacion = client.delete_message(mensaje_id)
    print("Mensaje eliminado:", resultado_eliminacion)
