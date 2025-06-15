import tkinter as tk
from tkinter import messagebox, simpledialog
import xmlrpc.client


class SeegaGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Seega - Cliente")
        self.proxy = xmlrpc.client.ServerProxy(
            "http://localhost:8000/RPC", allow_none=True)

        self.nome = simpledialog.askstring("Nome", "Digite seu nome:")
        self.peca, msg = self.proxy.entrar_jogo(self.nome)
        if not self.peca:
            messagebox.showerror("Erro", msg)
            master.destroy()
            return

        messagebox.showinfo("Conectado", msg)

        self.origem = None  # Coordenadas (linha, coluna)
        self.btn_origem = None  # Botão clicado

        self.criar_widgets()
        self.atualizar_tabuleiro()
        self.atualizar_mensagens()

    def criar_widgets(self):
        self.frame_tabuleiro = tk.Frame(self.master)
        self.frame_tabuleiro.pack()

        self.botoes = [[None for _ in range(5)] for _ in range(5)]
        for i in range(5):
            for j in range(5):
                btn = tk.Button(self.frame_tabuleiro, text="", width=4, height=2,
                                command=lambda x=i, y=j: self.acao_jogada(x, y))
                btn.grid(row=i, column=j)
                self.botoes[i][j] = btn

        self.lbl_info = tk.Label(self.master, text="")
        self.lbl_info.pack()

        self.chat_entry = tk.Entry(self.master)
        self.chat_entry.pack()

        self.btn_enviar = tk.Button(
            self.master, text="Enviar Mensagem", command=self.enviar_mensagem)
        self.btn_enviar.pack()

        self.btn_atualizar = tk.Button(
            self.master, text="Atualizar Estado", command=self.atualizar_estado
        )
        self.btn_atualizar.pack()

        self.texto_mensagens = tk.Text(
            self.master, height=6, state=tk.DISABLED)
        self.texto_mensagens.pack()

        self.btn_desistir = tk.Button(
            self.master, text="Desistir", command=self.desistir)
        self.btn_desistir.pack()

    def atualizar_tabuleiro(self):
        tabuleiro = self.proxy.obter_tabuleiro()
        if not tabuleiro:
            return
        for i in range(5):
            for j in range(5):
                self.botoes[i][j].config(text=tabuleiro[i][j])
        vez = self.proxy.obter_vez()
        self.lbl_info.config(text=f"Sua peça: {self.peca} | Vez de: {vez}")

        vencedor = self.proxy.obter_vencedor()
        if vencedor:
            messagebox.showinfo("Fim de jogo", f"Vencedor: {vencedor}")
            self.master.destroy()

    def acao_jogada(self, linha, coluna):
        fase = self.proxy.obter_fase()

        vez = self.proxy.obter_vez()
        if vez != self.peca:
            messagebox.showinfo("Aguarde", "Ainda não é sua vez!")
            return

        # Fase 1: colocação simples
        if fase == 1:
            msg = self.proxy.colocar_peca(self.peca, linha, coluna)
            messagebox.showinfo("Jogada", msg)
            self.atualizar_tabuleiro()
            return

        # Fase 2: movimentação com clique duplo
        if not self.origem:
            # Verifica se a peça clicada é do próprio jogador
            tabuleiro = self.proxy.obter_tabuleiro()
            valor = tabuleiro[linha][coluna].strip()
            if valor != self.peca:
                messagebox.showinfo("Inválido", "Selecione uma de suas peças.")
                return

            # Selecionar origem
            self.origem = (linha, coluna)
            self.btn_origem = self.botoes[linha][coluna]
            self.btn_origem.config(
                bg="yellow", relief=tk.SOLID, bd=3  # Borda mais espessa e cor chamativa
            )
        else:
            ox, oy = self.origem
            dx, dy = linha, coluna
            msg = self.proxy.mover_peca(self.peca, ox, oy, dx, dy)
            messagebox.showinfo("Jogada", msg)
            self.atualizar_tabuleiro()

            # Reset visual e estado
            if self.btn_origem:
                self.btn_origem.config(
                    bg="SystemButtonFace", relief=tk.RAISED, bd=1
                )
            self.origem = None
            self.btn_origem = None

    def enviar_mensagem(self):
        texto = self.chat_entry.get()
        if texto:
            self.proxy.enviar_mensagem(self.nome, texto)
            self.chat_entry.delete(0, tk.END)

    def atualizar_mensagens(self):
        mensagens = self.proxy.obter_mensagem(self.nome)
        if mensagens and mensagens != "Nenhuma nova mensagem.":
            self.texto_mensagens.config(state=tk.NORMAL)
            self.texto_mensagens.insert(tk.END, mensagens + "\n")
            self.texto_mensagens.config(state=tk.DISABLED)
            self.texto_mensagens.see(tk.END)  # Scroll automático

    def atualizar_estado(self):
        self.atualizar_tabuleiro()
        self.atualizar_mensagens()

    def desistir(self):
        msg = self.proxy.desistir(self.peca)
        messagebox.showinfo("Desistência", msg)
        self.master.destroy()


# Início da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = SeegaGUI(root)
    root.mainloop()
