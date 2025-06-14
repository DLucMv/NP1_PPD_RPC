import xmlrpc.client

# Conexão com o servidor
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

# Chamada remota da função soma
resultado = proxy.soma(5, 7)
print("Resultado da soma: ", resultado)
