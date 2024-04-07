from zeep import Client
client = Client("http://localhost:8000")

res = client.service.operaciones_aritmeticas(x=8,y=5,oper="+")
print(res)
res = client.service.div_dos_numeros(x=7,y=5)
print(res)