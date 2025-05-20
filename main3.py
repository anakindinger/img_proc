#===============================================================================
# Atividade: Implementação filtro da média
# Estudante: Ana Beatrix Kindinger
#-------------------------------------------------------------------------------
# Enunciado: 
'''Objetivo: implemente o efeito bloom em 2 versões, com filtragem Gaussiana e box blur.

Notas:
-> Você PODE (DEVE!) usar as funções prontas do OpenCV para os filtros.
-> Para o bright-pass, não faça binarização independente de 3 canais!
-> Observe que os valores de sigma aumentam bastante entre os filtros.
-> Lembre-se que a substituição não é de uma aplicação do filtro Gaussiano por uma do filtro da média;
*cada aplicação do filtro Gaussiano é aproximada com várias aplicações sucessivas do filtro da média!
'''
#-------------------------------------------------------------------------------
# # Universidade Tecnológica Federal do Paraná
#===============================================================================

import numpy as np
import cv2
import sys
#from google.colab.patches import cv2_imshow

#===============================================================================

INPUT_IMAGE =  'Wind Waker GC.bmp'
LIMIAR = 115 # Limiar para o bright-pass, de 0 a 255
SIGMAS = [4,16,32] # Valores de sigma crescentes para o filtro Gaussiano
KERNELS = [7,9,15,19,25] # Tamanhos de kernel para o box blur
ITERATIONS = 3 # Número de iterações para o box blur
# CONSTANTES



#===============================================================================
def gaussian_bloom (img, sigmas, kernel_size):
    ''' Função de Bloom com filtro Gaussiano:
    Entrada:
    img é a máscara do bright-pass obtida na função bright_pass.
    sigmas é uma lista de valores de sigma crescentes para o filtro Gaussiano.
    kernel_size é o tamanho do kernel para o filtro Gaussiano.
    Saída:
    img_gbloom é a imagem resultante do efeito bloom com filtro Gaussiano para ser somada à imagem original.
    '''
    img_gbloom = np.zeros_like (img)
    for s in sigmas:
        # Aplica o filtro Gaussiano na imagem
        mais_gbloom = cv2.GaussianBlur (img, (kernel_size, kernel_size), s)
        # Aplica a máscara das áreas brilhantes no resultado do filtro
        img_gbloom = cv2.addWeighted (img_gbloom, 1.0, mais_gbloom, 1.0, 0)
    return img_gbloom

def box_bloom(img, kernels):
    ''' Função de Bloom com Box Blur:
    Entrada:
    img é a máscara do bright-pass obtida na função bright_pass.
    kernels é uma lista de tamanhos de kernel para o box blur.
    Saída:
    img_bbloom é a imagem resultante do efeito bloom com box blur para ser somada à imagem original.
    '''
    img_bbloom = np.zeros_like (img)
    for k in kernels:
        for _ in range(ITERATIONS):# Aplica o filtro box blur na imagem
            mais_bbloom = cv2.boxFilter (img, -1, (k, k))
        img_bbloom = cv2.addWeighted (img_bbloom, 1.0, mais_bbloom, 0.3, 0) # Adiciona a imagem resultante do box blur à imagem de bloom
            
    return img_bbloom
#===============================================================================
def bright_pass (img, limiar):

    '''Função que aplica o filtro bright-pass na imagem.
    A imagem de entrada deve estar no formato HLS (Hue, Luminance, Saturation).
    O filtro bright-pass é aplicado na luminância da imagem, onde os pixels com
    luminância maior que o limiar são mantidos e os demais são zerados.
    '''
    img_hls = cv2.cvtColor (img, cv2.COLOR_RGB2HLS)
    img_mascara = np.zeros_like (img_hls) # Cria uma imagem de saída com o mesmo tamanho da imagem de entrada

    luminancia = img_hls[:, :, 1] # Extrai o canal de luminância da imagem HLS
    condicao = luminancia > limiar # Cria uma máscara booleana com os pixels que atendem ao critério do limiar

    img_mascara = np.where(condicao[:, :, np.newaxis], img_hls, np.zeros_like(img_hls)) # Cria a máscara com os pixels que atendem ao critério do limiar

    return img_mascara

#===============================================================================
def main ():

    '''TODO: 4. Script Principal:

    OK* Carregar uma imagem de teste usando OpenCV (cv2.imread).
    OK* Definir os parâmetros para as duas versões do bloom (limiar, valores de sigma crescentes para o Gaussiano, tamanhos de kernel e número de iterações para o box blur).
    * Chamar as duas funções de bloom com os parâmetros definidos.
    * Exibir as imagens resultantes (original e com os dois tipos de bloom) usando cv2.imshow.
    * Salvar as imagens resultantes usando cv2.imwrite.
    * Garantir que o script lide com a possibilidade de a imagem não ser carregada corretamente.'''

    # Abre a imagem em formato HSL para usar a luminancia no bright-pass.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()
    cv2.imshow('Original', img)

    mascara = bright_pass (img, LIMIAR)# Aplica o filtro bright-pass na imagem
    mascaraRGB = cv2.cvtColor (mascara, cv2.COLOR_HLS2RGB) # Converte a imagem de HLS para RGB
    cv2.imshow ('Mascara', mascaraRGB)

    gbloom = gaussian_bloom (mascaraRGB, SIGMAS, KERNELS[1]) # Aplica o filtro Gaussiano na imagem
    cv2.imshow ('Bloom Gaussiano', gbloom)
   
    bbloom = box_bloom (mascaraRGB, KERNELS) # Aplica o filtro box blur na imagem
    cv2.imshow ('Bloom Box Blur', bbloom)

    # Combina a imagem original com os efeitos de bloom
    img_gbloom = cv2.addWeighted (img, 1.0, gbloom, 0.3, 0)
    img_bbloom = cv2.addWeighted (img, 1.0, bbloom, 0.3, 0)

    cv2.imshow ('Bloom Gaussiano + Original', img_gbloom)
    cv2.imshow ('Bloom Box Blur + Original', img_bbloom)


    cv2.waitKey (0)
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
