from xmlrpc.server import SimpleXMLRPCServer

# Função que o servidor irá oferecer


def soma(a, b):
    return a + b


# Criação do servidor
server = SimpleXMLRPCServer(("localhost", 8000))
print("Servidor RPC escutando na porta 8000...")

# Registro da função
server.register_function(soma, "soma")

# Loop do servidor
server.serve_forever()
