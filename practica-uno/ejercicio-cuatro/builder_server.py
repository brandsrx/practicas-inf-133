from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

class PacienteBuilder:
    def __init__(self):
        self.ci = None
        self.nombre = None
        self.apellido= None
        self.edad = None
        self.genero= None
        self.diagnostico = None
        self.doctor= None

    def with_ci(self, ci):
        self.ci = ci
        return self

    def with_nombre(self, nombre):
        self.nombre = nombre
        return self

    def with_apellido(self, apellido):
        self.apellido = apellido
        return self

    def with_edad(self, edad):
        self.edad = edad
        return self

    def with_genero(self, genero):
        self.genero = genero
        return self

    def with_diagnostico(self, diagnostico):
        self.diagnostico = diagnostico
        return self

    def with_doctor(self, doctor):
        self.doctor = doctor
        return self

    def build(self):
        return {
            "ci": self.ci,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "edad": self.edad,
            "genero": self.genero,
            "diagnostico": self.diagnostico,
            "doctor": self.doctor
        }
builder = PacienteBuilder()
paciente1 = builder.with_ci(9971522).with_nombre("Ramiro").with_apellido("Mamani").with_edad("19").with_genero("Masculino").with_diagnostico("Diabetes").with_doctor("Pato Juan").build()
paciente2 = builder.with_ci(1234567).with_nombre("Maria").with_apellido("Lopez").with_edad("30").with_genero("Femenino").with_diagnostico("dolor de cabeza").with_doctor("Ana Martinez").build()
paciente3 = builder.with_ci(9876543).with_nombre("Juan").with_apellido("Perez").with_edad("45").with_genero("Masculino").with_diagnostico("presión arterial alta").with_doctor("Pedro Pérez").build()
pacientes = [paciente1, paciente2, paciente3]
print(pacientes)
class PacientesService:
    @staticmethod
    def add_paciente(data):
            ci = data.get("ci") 
            paciente_existente = PacientesService.ecntr_paciente(ci)
            if paciente_existente:
                return {"error": "Ya existe un paciente con el mismo ci"}
            else:
                builder = PacienteBuilder().with_ci(data.get("ci")) \
                                            .with_nombre(data.get("nombre")) \
                                            .with_apellido(data.get("apellido")) \
                                            .with_edad(data.get("edad")) \
                                            .with_genero(data.get("genero")) \
                                            .with_diagnostico(data.get("diagnostico")) \
                                            .with_doctor(data.get("doctor"))
                paciente = builder.build()
                pacientes.append(paciente)
                return pacientes 
    @staticmethod
    def ecntr_paciente(ci):
        return next(
            (paciente for paciente in pacientes if paciente["ci"] == ci),
            None,
        )
    @staticmethod
    def filtrar_paciente_nombre(nombre):
        return [
            paciente for paciente in pacientes if paciente["nombre"] == nombre
        ]
    @staticmethod
    def filtro_pacientes_diagnostico(diagnostico):
        return [
            paciente for paciente in pacientes if paciente["diagnostico"].lower() == diagnostico.lower()
        ]
    @staticmethod
    def filter_pacientes_by_doctor(doctor):
        return [
            paciente for paciente in pacientes if paciente["doctor"].lower() == doctor.lower()
                ]
    @staticmethod
    def update_paciente(ci, data):
        paciente = PacientesService.ecntr_paciente(ci)
        if paciente:
            paciente.update(data)
            return paciente
        else:
            return None
    @staticmethod
    def delete_paciente():
        pacientes.clear()
        return pacientes


class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))


class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes = PacientesService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path == "/pacientes":
            if "nombre" in query_params:
                nombre = query_params["nombre"][0]
                pacientes_filtrados = PacientesService.filtrar_paciente_nombre(nombre)
                if pacientes_filtrados:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacientesService.filtro_pacientes_diagnostico(diagnostico)
                if pacientes_filtrados:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_doctor(doctor)
                if pacientes_filtrados:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
        elif parsed_path.path.startswith("/pacientes/"):
            ci = int(parsed_path.path.split("/")[-1])
            paciente = PacientesService.ecntr_paciente(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
        
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            pacientes = PacientesService.update_paciente(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "No se encontro al paciente"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/pacientes/"):
            ci = int(parsed_path.path.split("/")[-1])
            paciente = PacientesService.ecntr_paciente(ci)
            if paciente:
                pacientes.remove(paciente)
                HTTPResponseHandler.handle_response(self, 200, {"message": "Paciente eliminado correctamente"})
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()