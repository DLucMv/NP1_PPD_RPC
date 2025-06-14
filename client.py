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
while True:
    print("\nTabuleiro:")
    for linha in proxy.obter_tabuleiro():
        print(" ".join(linha))

    vencedor = proxy.obter_vencedor()
    if vencedor:
        print("\nFim de jogo:", vencedor)
        break

    fase = proxy.obter_fase()
    vez = proxy.obter_vez()

    print(f"\nFase {fase} | Sua peça: {peca} | Vez de: {vez}")

    if vez != peca:
        input("Aguardando o outro jogador... Pressione Enter para atualizar.")
        continue

    print(
        "Opções: [1] Jogar  [2] Enviar mensagem  [3] Ver mensagens  [4] Desistir")
    op = input("Escolha: ")

    if op == "1":
        if fase == 1:
            jogada = input("Coloque sua peça (linha,coluna): ")
            lin, col = map(int, jogada.split())
            print(proxy.colocar_peca(peca, lin, col))
        elif fase == 2:
            entrada = input(
                "Digite 4 números (linha,coluna iniciais e finais): ")
            ox, oy, dx, dy = map(int, entrada.split())
            print(proxy.mover_peca(peca, ox, oy, dx, dy))
    elif op == "2":
        msg = input("Mensagem: ")
        print(proxy.enviar_mensagem(nome, msg))
    elif op == "3":
        print("Mensagens:\n", proxy.obter_mensagem(nome))
    elif op == "4":
        print(proxy.desistir(peca))
        break
