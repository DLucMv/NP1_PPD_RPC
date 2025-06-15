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
        self.criar_widgets()
        self.atualizar_tabuleiro()

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

    def acao_jogada(self, linha, coluna):
        fase = self.proxy.obter_fase()
        if fase == 1:
            msg = self.proxy.colocar_peca(self.peca, linha, coluna)
        else:
            # Em fase 2, você pode pedir via diálogo as coordenadas de origem
            origem = simpledialog.askstring(
                "Movimento", "De onde? (linha,coluna)")
            ox, oy = map(int, origem.split(","))
            msg = self.proxy.mover_peca(self.peca, ox, oy, linha, coluna)
        messagebox.showinfo("Jogada", msg)
        self.atualizar_tabuleiro()

    def enviar_mensagem(self):
        texto = self.chat_entry.get()
        if texto:
            self.proxy.enviar_mensagem(self.nome, texto)
            self.chat_entry.delete(0, tk.END)

    def desistir(self):
        msg = self.proxy.desistir(self.peca)
        messagebox.showinfo("Desistência", msg)
        self.master.destroy()


# Início da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = SeegaGUI(root)
    root.mainloop()
