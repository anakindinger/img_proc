import matplotlib.pyplot as plt
import numpy as np
import time

# Definindo a função flood_fill com animação
def flood_fill_anim(img, visitado, r, c, ax, delay=0.5):
    altura, largura = img.shape

    # Marca como visitado e exibe o processo
    visitado[r, c] = True
    img_visita = img.copy()
    img_visita[r, c] = 2  # Marca o pixel visitado com valor 2 (para visualização)

    # Exibe o gráfico
    ax.clear()
    ax.imshow(img_visita, cmap='hot', interpolation='nearest')
    ax.set_title(f"Visitando ({r},{c})")
    plt.draw()
    plt.pause(delay)

    # Vizinhanca (8 conexões)
    vizinhos = [(0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in vizinhos:
        nr, nc = r + dr, c + dc
        if 0 <= nr < altura and 0 <= nc < largura:
            if img[nr, nc] == 1 and not visitado[nr, nc]:
                flood_fill_anim(img, visitado, nr, nc, ax, delay)

# Criando a imagem binária (5x5)
img = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

# Inicializando a matriz de visitados
visitado = np.zeros_like(img, dtype=bool)

# Preparando a plotagem
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(img, cmap='hot', interpolation='nearest')
plt.title("Flood Fill Recursivo")
plt.show()

# Iniciando a animação
plt.pause(1)  # Aguarda o tempo para inicializar a janela
flood_fill_anim(img, visitado, 1, 1, ax, delay=0.7)  # Começa no (1, 1)

# Finaliza a animação
plt.show()
