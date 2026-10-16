
import tkinter as tk
from collections import deque
import random

T = 25
COLUNAS = 20
LINHAS = 20
VELOCIDADE = 100

janela = tk.Tk()
janela.title("Cobrinha automática - BFS")

canvas = tk.Canvas(
    janela,
    width=COLUNAS * T,
    height=LINHAS * T,
    highlightthickness=0
)
canvas.pack()

cobra = [(5, 5), (4, 5), (3, 5)]
pontuacao = 0

MOVIMENTOS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def criar_comida():
    livres = [
        (x, y)
        for x in range(COLUNAS)
        for y in range(LINHAS)
        if (x, y) not in cobra
    ]
    return random.choice(livres) if livres else None


comida = criar_comida()


def bfs(inicio, destino):
    fila = deque([inicio])
    pais = {inicio: None}

    while fila:
        atual = fila.popleft()

        if atual == destino:
            caminho = []

            while atual is not None:
                caminho.append(atual)
                atual = pais[atual]

            return caminho[::-1]

        for dx, dy in MOVIMENTOS:
            x = atual[0] + dx
            y = atual[1] + dy
            pos = (x, y)

            if not (0 <= x < COLUNAS and 0 <= y < LINHAS):
                continue

            if pos in cobra[:-1] and pos != destino:
                continue

            if pos not in pais:
                pais[pos] = atual
                fila.append(pos)

    return []


def cor_verde(proporcao):
    vermelho = int(70 - 25 * proporcao)
    verde = int(225 - 65 * proporcao)
    azul = int(95 - 30 * proporcao)

    return f"#{vermelho:02x}{verde:02x}{azul:02x}"


def desenhar_cobra():
    total = len(cobra)

    # Desenhar o corpo sem bordas entre as células
    for i in range(total - 1, -1, -1):
        x, y = cobra[i]
        cor = cor_verde(i / max(total - 1, 1))

        canvas.create_rectangle(
            x*T, y*T,
            (x+1)*T, (y+1)*T,
            fill=cor,
            outline=cor,
            width=0
        )

        # Conectar os segmentos sem deixar lacunas
        if i > 0:
            px, py = cobra[i-1]

            canvas.create_rectangle(
                min(x, px)*T,
                min(y, py)*T,
                (max(x, px)+1)*T,
                (max(y, py)+1)*T,
                fill=cor,
                outline=cor,
                width=0
            )


def desenhar():
    canvas.delete("all")

    # Chão quadriculado
    for y in range(LINHAS):
        for x in range(COLUNAS):
            cor = "#F4F6F4" if (x+y) % 2 == 0 else "#E8ECE8"

            canvas.create_rectangle(
                x*T, y*T,
                (x+1)*T, (y+1)*T,
                fill=cor,
                outline="#D5DCD5"
            )

    # Maçã quadrada
    if comida is not None:
        x, y = comida

        canvas.create_rectangle(
            x*T+4, y*T+4,
            (x+1)*T-4, (y+1)*T-4,
            fill="#F04444",
            outline="#D83232",
            width=2
        )

    desenhar_cobra()

    # Pontuação
    canvas.create_text(
        8, 8,
        text=f"Pontos: {pontuacao}",
        fill="#263326",
        anchor="nw",
        font=("Arial", 12, "bold")
    )


def atualizar():
    global cobra, comida, pontuacao

    if comida is None:
        desenhar()
        canvas.create_text(
            COLUNAS*T//2, LINHAS*T//2,
            text="Você venceu!",
            fill="green",
            font=("Arial", 18, "bold")
        )
        return

    caminho = bfs(cobra[0], comida)

    if caminho and len(caminho) > 1:
        proxima = caminho[1]

    else:
        caminho = bfs(cobra[0], cobra[-1])

        if caminho and len(caminho) > 1:
            proxima = caminho[1]

        else:
            opcoes = [
                (cobra[0][0]+dx, cobra[0][1]+dy)
                for dx, dy in MOVIMENTOS
            ]

            opcoes = [
                p for p in opcoes
                if 0 <= p[0] < COLUNAS
                and 0 <= p[1] < LINHAS
                and p not in cobra[:-1]
            ]

            if not opcoes:
                desenhar()
                canvas.create_text(
                    COLUNAS*T//2, LINHAS*T//2,
                    text="Fim de jogo!",
                    fill="red",
                    font=("Arial", 18, "bold")
                )
                return

            proxima = opcoes[0]

    vai_comer = proxima == comida
    ocupadas = cobra if vai_comer else cobra[:-1]

    if proxima in ocupadas:
        desenhar()
        canvas.create_text(
            COLUNAS*T//2, LINHAS*T//2,
            text="Fim de jogo!",
            fill="red",
            font=("Arial", 18, "bold")
        )
        return

    cobra.insert(0, proxima)

    if vai_comer:
        pontuacao += 1
        comida = criar_comida()
    else:
        cobra.pop()

    desenhar()
    janela.after(VELOCIDADE, atualizar)


desenhar()
janela.after(VELOCIDADE, atualizar)
janela.mainloop()
