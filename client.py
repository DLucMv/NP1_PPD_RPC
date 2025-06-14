import xmlrpc.client


# Conecta ao servidor
proxy = xmlrpc.client.ServerProxy(
    "http://localhost:8000/RPC", allow_none=True)

# Entrada no jogo
nome = input("Digite seu nome: ")
peca, msg = proxy.entrar_jogo(nome)
if not peca:
    print(msg)
    exit()

print(f"Você é: {peca}")
print(msg)
