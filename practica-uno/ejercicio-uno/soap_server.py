from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher,SOAPHandler
from typing import Union
def operaciones_aritmeticas(x,y,oper):
    if(oper == "+"):
        return x+y
    elif oper == "-":
        return x-y
    elif oper == "*" or oper == "x":
        return x*y
    else:
        return 0
def div_dos_numeros(x,y):
    return x/y

dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "operaciones_aritmeticas",
    operaciones_aritmeticas,
    returns={"operaciones_aritmeticas":int},
    args={
        "x":int,
        "y":int,
        "oper":str
    }
)
dispatcher.register_function(
    "div_dos_numeros",
    div_dos_numeros,
    returns={"div_dos_numeros":float},
    args={
        "x":int,
        "y":int,
    }
)

server = HTTPServer(("0.0.0.0",8000),SOAPHandler)
server.dispatcher = dispatcher
print("Servidor soap inciado en http//localhost:8000/")
server.serve_forever()