from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Classe com todos o métodos fornecidos pelo servidor


class SeegaServer:
    def __init__(self):
        self.tabuleiro = [["⬜" for _ in range(5)] for _ in range(5)]
        self.jogadores = []  # Lista de tuplas: (nome, peça)
        self.vez = None
        self.finalizado = False
        self.vencedor = None
        self.chat = []
        self.mensagens = {}

        # Colocação inicial (cada jogador terá 12 peças)
        self.pecas_restantes = {"🔴": 12, "🔵": 12}

    def entrar_jogo(self, nome):
        if len(self.jogadores) >= 2:
            return None, "O jogo já está cheio."

        peca = "🔴" if not self.jogadores else "🔵"
        self.jogadores.append((nome, peca))

        if len(self.jogadores) == 2:
            self.vez = "🔴"

        return peca, "Aguardando o outro jogador..." if len(self.jogadores) < 2 else "O jogo começou!"


# Configuração RPC
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC",)


servidor = SeegaServer()

with SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler, allow_none=True) as server:
    server.register_instance(servidor)
    print("Servidor Seega escutando na porta 8000...✅")
    server.serve_forever()
