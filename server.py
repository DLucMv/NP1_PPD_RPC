from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Classe com todos o métodos fornecidos pelo servidor


class SeegaServer:
    def __init__(self):
        self.tabuleiro = [["❌" for _ in range(5)] for _ in range(5)]
        self.tabuleiro[2][2] = "⬜"  # Centro vazio
        self.jogadores = []
        self.vez = None
        self.fase = 1
        self.pecas_colocadas = {"⚫": 0, "⚪": 0}
        self.max_pecas = 12
        self.finalizado = False
        self.vencedor = None
        self.chat = []
        self.mensagens = {}

    def entrar_jogo(self, nome):
        if len(self.jogadores) >= 2:
            return None, "Jogo cheio."
        peca = "⚫" if not self.jogadores else "⚪"
        self.jogadores.append((nome, peca))
        if len(self.jogadores) == 2:
            self.vez = "⚫"
        return peca, "Aguardando oponente." if len(self.jogadores) < 2 else "Jogo iniciado."

    def obter_tabuleiro(self):
        return self.tabuleiro

    def obter_vez(self):
        return self.vez

    def obter_fase(self):
        return self.fase

    def colocar_peca(self, peca, linha, coluna):
        if self.fase != 1:
            return "Não é fase de colocação."
        if not (0 <= linha < 5 and 0 <= coluna < 5):
            return "Posição inválida."
        if self.tabuleiro[linha][coluna] != "❌":
            return "Já ocupada."
        if (linha, coluna) == (2, 2):
            return "Centro deve ficar vazio."

        self.tabuleiro[linha][coluna] = peca
        self.pecas_colocadas[peca] += 1

        if self.pecas_colocadas["⚫"] == self.max_pecas and self.pecas_colocadas["⚪"] == self.max_pecas:
            self.fase = 2

        self.vez = "⚪" if peca == "⚫" else "⚫"
        return "Peça colocada."

    def mover_peca(self, peca, ox, oy, dx, dy):
        if self.fase != 2:
            return "Ainda estamos na fase de colocação."
        if self.vez != peca:
            return f"Não é sua vez."
        if self.tabuleiro[ox][oy] != peca or self.tabuleiro[dx][dy] not in ("❌", "⬜"):
            return "Movimento inválido."
        if abs(dx - ox) + abs(dy - oy) != 1:
            return "Movimento deve ser ortogonal de uma casa."

        self.tabuleiro[ox][oy] = "❌"
        self.tabuleiro[dx][dy] = peca
        self.verificar_captura(peca, dx, dy)

        self.vez = "⚪" if peca == "⚫" else "⚫"
        return "Movimento realizado."

    def verificar_captura(self, peca, x, y):
        oponente = "⚫" if peca == "⚪" else "⚪"
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adjx, adjy = x + dx, y + dy
            capx, capy = x + 2 * dx, y + 2 * dy
            if 0 <= adjx < 5 and 0 <= adjy < 5 and self.tabuleiro[adjx][adjy] == oponente:
                if 0 <= capx < 5 and 0 <= capy < 5 and self.tabuleiro[capx][capy] == peca:
                    self.tabuleiro[adjx][adjy] = "❌"

    # To-do métodos relativos as mensagens

    def desistir(self, peca):
        self.finalizado = True
        self.vencedor = "⚪" if peca == "⚫" else "⚫"
        return f"O jogador {peca} desistiu. {self.vencedor} venceu! 🏆"

    def verificar_finalizacao(self):
        return self.finalizado

    def obter_vencedor(self):
        return self.vencedor

# Configuração RPC


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC",)


servidor = SeegaServer()

with SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler, allow_none=True) as server:
    server.register_instance(servidor)
    print("Servidor Seega escutando na porta 8000...✅")
    server.serve_forever()
