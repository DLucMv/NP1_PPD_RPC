import xmlrpc.client
import time

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


# Aguarda outro jogador
while proxy.obter_tabuleiro() == None:
    print("Aguardando outro jogador...")
    time.sleep(1)

# Função auxiliar para exibir o tabuleiro


def mostrar_tabuleiro(tab):
    print("\n  0 1 2 3 4")
    for i, linha in enumerate(tab):
        print(i, " ".join(linha))


# Ações do jogo
acao = input("Digite 'jogar', 'mensagem' ou 'desistir': ").strip().lower()

if acao == "desistir":
    print(proxy.desistir(peca))
