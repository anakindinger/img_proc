#===============================================================================
# Atividade: Implementação filtro da média
#-------------------------------------------------------------------------------
# Enunciado: 
'''Objetivo: implemente 3 algoritmos para o filtro da média:
- Algoritmo “ingênuo”.
- Filtro separável (escolha se quer fazer com ou sem aproveitar as somas anteriores).
- Algoritmo com imagens integrais.


Notas:
- Coloque as 3 implementações no mesmo arquivo, junto com um programa principal que permita testá-las.
- Para imagens coloridas, processar cada canal RGB independentemente.
- Tratamento das margens: na implementação com imagens integrais, fazer média considerando somente os pixels válidos; nas outras pode simplesmente ignorar posições cujas janelas ficariam fora da imagem.
- O pacote tem algumas imagens para comparação. Se estiver usando OpenCV, compare os resultados com os da função blur da biblioteca (exceto pelas margens, o resultado deve ser igual!).
'''
#-------------------------------------------------------------------------------
# # Universidade Tecnológica Federal do Paraná
#===============================================================================

import numpy as np
import cv2
import sys
#from google.colab.patches import cv2_imshow

#===============================================================================

INPUT_IMAGE =  'camaleao.png'

# CONSTANTES

JAN_LARGURA = 9
JAN_ALTURA = 9

#===============================================================================

def media_ingenua(img, largura, altura):
    '''Implementação do filtro da média com a abordagem ingênua usando for com kwargs para altura e largura.
    Parâmetros:
    img: Imagem de entrada.
    largura: Largura da janela 
    altura: Altura da janela 

    Valor de retorno: Imagem filtrada.
    '''

    if largura <= 0 or altura <= 0:
        raise ValueError("Largura e altura devem ser maiores que 0.")


    img_ingenua = np.zeros_like(img, dtype = np.float32)
    meia_largura = largura // 2 if largura > 1 else 1  # Use meia_largura apenas se largura > 1
    meia_altura = altura // 2 if altura > 1 else 1   # Use meia_altura apenas se altura > 1

    for linha in range(meia_altura, img.shape[0] - meia_altura):
        for coluna in range(meia_largura, img.shape[1] - meia_largura):
            soma = 0
            for linha_jan in range(linha - meia_altura, linha + meia_altura + 1):
                for coluna_jan in range(coluna - meia_largura, coluna + meia_largura + 1):
                    soma += img[linha_jan, coluna_jan]

            img_ingenua[linha, coluna] = soma / (largura * altura)

    return img_ingenua

#-------------------------------------------------------------------------------

def media_separavel (img, largura, altura):
    '''Implementação do filtro da média separável. esta implementação não aproveita as somas anteriores, não considera as margens e aproveita a função de média ingênua implementada anteriormente.
    Parâmetros:
    img: Imagem de entrada.
    largura: Largura da janela
    altura: Altura da janela
    retorno: Imagem filtrada.
    '''
    img_separavel = np.zeros_like(img, dtype=np.float32) #iniciando uma imagem 'vazia'
    buffer = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32) #iniciando um buffer 'vazio'
    
    #filtragem na horizontal
    buffer = media_ingenua(img, largura, 1) #aplicando a função de média ingênua na horizontal
    #filtragem na vertical
    img_separavel = media_ingenua(buffer, 1, altura) #aplicando a função de média ingênua na vertical

    return img_separavel

#-------------------------------------------------------------------------------
def media_integral(img, largura, altura):
    '''Implementação do filtro da média usando imagens integrais.
    Parâmetros:
    img: Imagem de entrada.
    largura: Largura da janela.
    altura: Altura da janela.
    Valor de retorno: Imagem filtrada.
    '''
    if largura <= 0 or altura <= 0:
        raise ValueError("Largura e altura devem ser maiores que 0.")

    img_integral = np.zeros_like(img, dtype=np.float32) #iniciando uma imagem 'vazia'
    integrais = np.zeros((img.shape[0] + 1, img.shape[1] + 1), dtype=float)
    meia_largura = largura // 2 if largura > 1 else 1  # Use meia_largura apenas se largura > 1
    meia_altura = altura // 2 if altura > 1 else 1   # Use meia_altura apenas se altura > 1

    #calculando a matriz onde vou salvar as integrais
    for linha in range(1, img.shape[0] + 1):
        for coluna in range(1, img.shape[1] + 1):
            integrais[linha, coluna] = img[linha - 1, coluna - 1] + integrais[linha - 1, coluna] + integrais[linha, coluna - 1] - integrais[linha - 1, coluna - 1]

    #calculando as médias
    for linha in range(img.shape[0]):
        for coluna in range(img.shape[1]):
            # Verifica se a janela está dentro dos limites da imagem
            linha_inicial = max(0, linha - meia_altura)
            linha_final = min(img.shape[0], linha + meia_altura + 1)
            coluna_inicial = max(0, coluna - meia_largura)
            coluna_final = min(img.shape[1], coluna + meia_largura + 1)
            
            #  ↘ - ↙ - ↗ + ↖
            soma = integrais[linha_final, coluna_final] - integrais[linha_final, coluna_inicial] - integrais[linha_inicial, coluna_final] + integrais[linha_inicial, coluna_inicial]
            area = (linha_final - linha_inicial) * (coluna_final - coluna_inicial)#calcula a area da janela que sobrepoe a imagem
            
            # Verifica se a área é maior que 0 para evitar divisão por zero
            if area > 0:
                img_integral[linha, coluna] = soma / area
            else:
                img_integral[linha, coluna] = 0

    return img_integral

   #===============================================================================

def main ():

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.

    cv2.imshow('Original', img)
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255
   

    # Aplica o filtro da média ingênua.
    img_media_ingenua = media_ingenua (img, JAN_LARGURA, JAN_ALTURA)
    img_media_ingenua = img_media_ingenua.reshape ((img.shape [0], img.shape [1]))
    img_media_ingenua = img_media_ingenua.astype (np.float32) * 255
    img_media_ingenua = cv2.normalize (img_media_ingenua, None, 0, 255, cv2.NORM_MINMAX)
    img_media_ingenua = img_media_ingenua.astype (np.uint8)
    cv2.imshow ('Filtro da média ingênua', img_media_ingenua)
    cv2.imwrite ('media_ingenua.png', img_media_ingenua)

    #Aplica o filtro da média separável.
    img_media_separavel = media_separavel (img, JAN_LARGURA, JAN_ALTURA)
    img_media_separavel = img_media_separavel.reshape ((img.shape [0], img.shape [1]))
    img_media_separavel = img_media_separavel.astype (np.float32) * 255
    img_media_separavel = cv2.normalize (img_media_separavel, None, 0, 255, cv2.NORM_MINMAX)
    img_media_separavel = img_media_separavel.astype (np.uint8)
    cv2.imshow ('Filtro da média separável', img_media_separavel)
    cv2.imwrite ('media_separavel.png', img_media_separavel)

    # Aplica o filtro da média com imagem integral.
    img_media_integral = media_integral (img, JAN_LARGURA, JAN_ALTURA)
    img_media_integral = img_media_integral.reshape ((img.shape [0], img.shape [1]))
    img_media_integral = img_media_integral.astype (np.float32) * 255
    img_media_integral = cv2.normalize (img_media_integral, None, 0, 255, cv2.NORM_MINMAX)
    img_media_integral = img_media_integral.astype (np.uint8)
    cv2.imshow ('Filtro da média com imagem integral', img_media_integral)
    cv2.imwrite ('media_integral.png', img_media_integral)


    cv2.waitKey (0)
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
