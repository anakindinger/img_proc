#===============================================================================
# Atividade: Implementação filtro da média
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
LIMIAR = 125 # Limiar para o bright-pass, de 0 a 255
SIGMAS = [1, 2, 4, 8, 16] # Valores de sigma crescentes para o filtro Gaussiano
KERNELS = [3, 5, 7] # Tamanhos de kernel para o box blur
ITERATIONS = 3 # Número de iterações para o box blur
# CONSTANTES



#===============================================================================
#TODO
'''

2. Função de Bloom com Gaussiano:

* Implementar uma função que recebe a imagem original, o limiar do bright-pass, uma lista de valores de sigma (que devem aumentar) e o tamanho do kernel Gaussiano.
* Chamar a função de bright-pass para obter a máscara das áreas brilhantes.
* Para cada valor de sigma na lista:
    *Aplicar o filtro Gaussiano na imagem original usando a função do OpenCV (cv2.GaussianBlur).
    *Aplicar a máscara das áreas brilhantes no resultado do filtro para isolar o brilho.
* Combinar os resultados dos filtros Gaussianos com diferentes sigma (por exemplo, somando-os).
* Adicionar a imagem combinada de volta à imagem original para criar o efeito bloom.
* Garantir que os valores dos pixels permaneçam dentro da faixa válida (0-255).'''
def gaussian_bloom (img, sigmas, kernel_size):
    img_gbloom = np.zeros_like (img)
    #for s in sigmas:
    return img_gbloom

def box_bloom(img, kernels, iterations):
    '''3. Função de Bloom com Box Blur:
    Entrada:
    img é a máscara do bright-pass obtida na função bright_pass.
    kernels é uma lista de tamanhos de kernel para o box blur.
    iterations é o número de iterações para cada kernel
    Saída:
    img_bbloom é a imagem resultante do efeito bloom com box blur para ser somada à imagem original.
    '''
    img_bbloom = np.zeros_like (img)
    for k in kernels:
        for _ in range(iterations):
            # Aplica o filtro box blur na imagem
            img_bbloom = cv2.boxFilter (img, -1, (k, k))
            
    return img_bbloom
#===============================================================================
def bright_pass (img, limiar):

    '''Função que aplica o filtro bright-pass na imagem.
    A imagem de entrada deve estar no formato HLS (Hue, Luminance, Saturation).
    O filtro bright-pass é aplicado na luminância da imagem, onde os pixels com
    luminância maior que o limiar são mantidos e os demais são zerados.
    '''
    img_mascara = np.zeros_like (img) # Cria uma imagem de saída com o mesmo tamanho da imagem de entrada
    for i in range (img.shape[0]):
        for j in range (img.shape[1]):
            # Se o pixel for maior que o limiar, copia o pixel para a imagem de saída
            if img[i, j, 1] > limiar:
                img_mascara[i, j] = img[i, j]
            else:
                img_mascara[i, j] = 0

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


    img = cv2.cvtColor (img, cv2.COLOR_RGB2HLS)
    
    # Aplica o filtro bright-pass na imagem
    img_mascara = bright_pass (img, LIMIAR)
    #img_mascara = cv2.cvtColor (img_mascara, cv2.COLOR_HLS2RGB)
    cv2.imshow ('Bright-pass', img_mascara)

   

    cv2.waitKey (0)
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
