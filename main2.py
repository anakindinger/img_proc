import cv2
import numpy as np
import time

def filtro_media_ingenuo(imagem, tamanho_janela):
    """
    Aplica o filtro da média de forma ingênua.

    Args:
        imagem (numpy.ndarray): A imagem de entrada (em escala de cinza ou colorida).
        tamanho_janela (int): O tamanho da janela do filtro (deve ser ímpar).

    Returns:
        numpy.ndarray: A imagem filtrada.
    """
    altura, largura = imagem.shape[:2]
    raio = tamanho_janela // 2
    imagem_filtrada = np.zeros_like(imagem, dtype=np.float32)

    # TODO: Implementar o filtro

    return imagem_filtrada.astype(imagem.dtype)

def filtro_media_separavel(imagem, tamanho_janela):
    """
    Aplica o filtro da média de forma separável.

    Args:
        imagem (numpy.ndarray): A imagem de entrada (em escala de cinza ou colorida).
        tamanho_janela (int): O tamanho da janela do filtro (deve ser ímpar).

    Returns:
        numpy.ndarray: A imagem filtrada.
    """
    altura, largura = imagem.shape[:2]
    raio = tamanho_janela // 2
    imagem_filtrada = np.zeros_like(imagem, dtype=np.float32)

    # TODO: Implementar o filtro separável aqui (horizontal e depois vertical)

    return imagem_filtrada.astype(imagem.dtype)

def filtro_media_integral_image(imagem, tamanho_janela):
    """
    Aplica o filtro da média utilizando o conceito de imagem integral.

    Args:
        imagem (numpy.ndarray): A imagem de entrada (em escala de cinza ou colorida).
        tamanho_janela (int): O tamanho da janela do filtro (deve ser ímpar).

    Returns:
        numpy.ndarray: A imagem filtrada.
    """
    altura, largura = imagem.shape[:2]
    raio = tamanho_janela // 2
    imagem_filtrada = np.zeros_like(imagem, dtype=np.float32)

    # TODO: Implementar o filtro
    
    return imagem_filtrada.astype(imagem.dtype)

if __name__ == "__main__":
    # Carrega uma imagem para teste
    try:
        imagem_colorida = cv2.imread("baboon.tiff")
        imagem_cinza = cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2GRAY)
    except FileNotFoundError:
        print("Erro: A imagem 'baboon.tiff' não foi encontrada. Certifique-se de que o arquivo existe no mesmo diretório ou forneça o caminho correto.")
        exit()

    tamanho_janela = 5

    # Teste do filtro da média ingênuo
    start_time = time.time()
    resultado_ingenuo_cinza = filtro_media_ingenuo(imagem_cinza, tamanho_janela)
    end_time = time.time()
    print(f"Tempo do filtro ingênuo (cinza): {end_time - start_time:.4f} segundos")
    cv2.imshow("Resultado Ingênuo (Cinza)", resultado_ingenuo_cinza.astype(np.uint8))
    cv2.waitKey(0)

    # Teste do filtro da média separável
    start_time = time.time()
    resultado_separavel_cinza = filtro_media_separavel(imagem_cinza, tamanho_janela)
    end_time = time.time()
    print(f"Tempo do filtro separável (cinza): {end_time - start_time:.4f} segundos")
    cv2.imshow("Resultado Separável (Cinza)", resultado_separavel_cinza.astype(np.uint8))
    cv2.waitKey(0)

    # Teste do filtro da média com imagem integral
    start_time = time.time()
    resultado_integral_cinza = filtro_media_integral_image(imagem_cinza, tamanho_janela)
    end_time = time.time()
    print(f"Tempo do filtro com imagem integral (cinza): {end_time - start_time:.4f} segundos")
    cv2.imshow("Resultado Integral (Cinza)", resultado_integral_cinza.astype(np.uint8))
    cv2.waitKey(0)

    # Comparação com a função blur do OpenCV
    resultado_opencv_cinza = cv2.blur(imagem_cinza, (tamanho_janela, tamanho_janela))
    cv2.imshow("Resultado OpenCV (Cinza)", resultado_opencv_cinza)
    cv2.waitKey(0)


    cv2.destroyAllWindows()