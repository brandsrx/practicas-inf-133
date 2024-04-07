import requests
url = "http://localhost:8000/"

# crear paciente
ruta = url + "pacientes"
new_paciente = {
    "ci": 654321,
    "nombre": "Ana",
    "apellido": "González",
    "edad": "28",
    "genero": "Femenino",
    "diagnostico": "alergia",
    "doctor": "Pedro Ramirez",
}
post_response = requests.request(method="POST", url=ruta, json=new_paciente)
print(post_response.text)

# Listar pacientes 
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get) 
print(get_response.text)
#buscar pacientes ci
ci = 9971522
ruta_get_ci = url + f"pacientes/{ci}"
response = requests.request(method="GET", url=ruta_get_ci)
print(response.text)

#listar pacientes por diagnostico
diagnostico = "Diabetes" 
ruta = url + f"pacientes?diagnostico={diagnostico}"
response = requests.request(method="GET", url=ruta)
print(response.text)
# listar pacientes por doctor
doctor = "Pedro Pérez"  
ruta = url + f"pacientes?doctor={doctor}"
response = requests.request(method="GET", url=ruta)
print(response.text)
# actualizar paciente 
ci = 9876543
ruta = url + f"pacientes/{ci}"
update_date = {
    "nombre": "Gael",
    "apellido": "Garcia",
    "edad": "25",
    "genero": "Masculino",
    "diagnostico": "asma",
    "doctor": "Marcos Borras"
}
response = requests.request(method="PUT", url=ruta, json=update_date)
print(response.text)
#eliminar paciente
ci = 9971522
ruta = url + f"pacientes/{ci}"
response = requests.request(method="DELETE", url=ruta)
print(response.text)
