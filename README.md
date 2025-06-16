# 🕹️ Seega RPC - Jogo de Seega com RPC em Python

Este é um projeto de um jogo de tabuleiro chamado **Seega**, implementado em Python com comunicação cliente-servidor usando **XML-RPC**. O jogo possui interface gráfica feita com **Tkinter** e permite a interação entre dois jogadores pela rede local.

## 📌 Objetivos

- Aplicar os conceitos de **Programação Paralela e Distribuída (PPD)**.
- Utilizar **RPC (Remote Procedure Call)** com o módulo `xmlrpc` do Python.
- Criar uma aplicação cliente/servidor funcional e interativa.
- Desenvolver o jogo Seega com as regras tradicionais de colocação, movimentação e captura de peças.

## 🚀 Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/DLucMv/NP1_PPD_RPC.git
cd NP1_PPD_RPC
```

### 2. Execute o servidor
No terminal:
```bash
python server.py
```
O servidor escutará conexões RPC na porta `8000`.

### 3. Execute o cliente
Em outro terminal (ou outro computador na rede local, ajustando o IP):
```bash
python clientGUI.py
```

Você precisará digitar seu nome para entrar na partida. O jogo iniciará automaticamente quando dois jogadores estiverem conectados.

## 🧠 Regras do Jogo (Seega)

- **Tabuleiro 5x5** com o centro vazio no início.
- **Fase 1: Colocação**
  - Cada jogador coloca suas 12 peças alternadamente.
- **Fase 2: Movimentação**
  - Os jogadores se revezam para mover suas peças ortogonalmente.
  - É possível capturar peças adversárias cercando-as entre duas peças próprias.
- O jogo termina quando um jogador tem 1 ou nenhuma peça.

## 📡 Arquitetura

- **Servidor (`server.py`)**: centraliza o estado do jogo e disponibiliza métodos via RPC.
- **Cliente (`clientGUI.py`)**: interface gráfica com Tkinter para interagir com o servidor.

## 📦 Requisitos

- Python 3.10 ou superior
- Bibliotecas padrão (`xmlrpc`, `tkinter`)

## 🛠️ Empacotamento (Opcional)

Para criar um executável do cliente (por exemplo com `pyinstaller`):
```bash
pyinstaller --onefile --noconsole clientGUI.py
```

## 📷 Interface

A interface gráfica permite:
- Colocar e mover peças
- Ver o estado do tabuleiro
- Enviar mensagens via chat
- Desistir da partida

## 📖 Créditos

Desenvolvido por [@DLucMv](https://github.com/DLucMv) como parte da avaliação de NP1 da disciplina de **Programação Paralela e Distribuída**.