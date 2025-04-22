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

#===============================================================================

INPUT_IMAGE =  ''

# CONSTANTES

TAM_JANELA = 5

#===============================================================================

def media_ingenuo (img, janela):
    ''' implementação da média ingênua usando for
    Parâmetros:
    img: imagem de entrada
    janela: tamanho de janela w x w
    
    Valor de retorno: imagem filtrada
    '''
    img_ingenua = np.zeros((img.shape[0],img.shape[1], 3), dtype=np.uint32) #iniciando uma imagem 'vazia'
    meia_janela = janela //2

    for linha in range(meia_janela, img.shape[0]-meia_janela): # range ignorando as bordas
        for coluna in range(meia_janela, img.shape[1]-meia_janela):
            soma = 0 #reinicia cada vez que a janela se move
            for lilinha in range(linha-meia_janela, linha+meia_janela+1):
                for cocoluna in range(coluna-meia_janela, coluna+meia_janela):
                    soma += img[lilinha,cocoluna]

            img_ingenua[linha,coluna] = soma/(janela**2)

    return img_ingenua

#-------------------------------------------------------------------------------

def media_separavel (img, janela):
    #essa é a que precisa de buffer!
    img_separavel = np.zeros((img.shape[0],img.shape[1], 3), dtype=np.uint32) #iniciando uma imagem 'vazia'
    meia_janela = janela //2

    return img_separavel


   #===============================================================================

def main ():

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255
    cv2.imshow ('01 - binarizada', img)
    cv2.imwrite ('01 - binarizada.png', img*255)

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza (img, THRESHOLD)
    cv2.imshow ('01 - binarizada', img)
    cv2.imwrite ('01 - binarizada.png', img*255)

    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

   
    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (1,0,1))
        

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)

   
    cv2.waitKey (0)
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
