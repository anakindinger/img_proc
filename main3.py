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
* Garantir que os valores dos pixels permaneçam dentro da faixa válida (0-255).

3. Função de Bloom com Box Blur:

* Implementar uma função similar à anterior, recebendo a imagem original, o limiar, uma lista de tamanhos de kernel para o box blur e o número de iterações para cada kernel.
* Chamar a função de bright-pass para obter a máscara.
* Para cada tamanho de kernel na lista:
    * Aplicar o filtro de box blur (cv2.blur ou cv2.boxFilter do OpenCV) na imagem original o número especificado de vezes (iterations).
    * Aplicar a máscara das áreas brilhantes no resultado do filtro.
* Combinar os resultados dos filtros de box blur.
* Adicionar a imagem combinada de volta à original.
* Garantir a faixa de valores dos pixels.

4. Script Principal:

* Carregar uma imagem de teste usando OpenCV (cv2.imread).
* Definir os parâmetros para as duas versões do bloom (limiar, valores de sigma crescentes para o Gaussiano, tamanhos de kernel e número de iterações para o box blur).
* Chamar as duas funções de bloom com os parâmetros definidos.
* Exibir as imagens resultantes (original e com os dois tipos de bloom) usando cv2.imshow.
* Salvar as imagens resultantes usando cv2.imwrite.
* Garantir que o script lide com a possibilidade de a imagem não ser carregada corretamente.'''
#===============================================================================
def bright_pass (img, limiar):

    '''Função que aplica o filtro bright-pass na imagem.
    A imagem de entrada deve estar no formato HLS (Hue, Luminance, Saturation).
    O filtro bright-pass é aplicado na luminância da imagem, onde os pixels com
    luminância maior que o limiar são mantidos e os demais são zerados.
    '''
    img_limiar = np.zeros (img.shape, dtype =np.uint8)
    for i in range (img.shape[0]):
        for j in range (img.shape[1]):
            # Se o pixel for maior que o limiar, copia o pixel para a imagem de saída
            if img[i, j, 1] > limiar:
                img_limiar[i, j] = img[i, j]
            else:
                img_limiar[i, j] = 0

    return img_limiar

#===============================================================================
def main ():

    # Abre a imagem em formato HSL para usar a luminancia no bright-pass.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()


    cv2.imshow('Original', img)
    img = cv2.cvtColor (img, cv2.COLOR_RGB2HLS)
    print (np.max (img[:, :, 1]))
    print (np.min (img[:, :, 1]))

    #mascara = bright_pass (img, LIMIAR)
    #mascara = cv2.cvtColor (mascara, cv2.COLOR_HLS2RGB)
    #cv2.imshow ('Mascara', mascara)

   

   

    cv2.waitKey (0)
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
