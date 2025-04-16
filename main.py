#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.82
ALTURA_MIN = 7
LARGURA_MIN = 7
N_PIXELS_MIN = 30

#===============================================================================

def binariza (img, threshold):
    ''' Binarização simples por limiarização.

    Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
    Valor de retorno: versão binarizada da img_in.'''
    imagem_binarizada = np.where(img>threshold,1,0).astype(np.float32)
    
    return imagem_binarizada


#-------------------------------------------------------------------------------

def rotula (img, largura_min, altura_min, n_pixels_min):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    altura, largura, _ = img.shape
    rotulo_atual = 0.1
    componentes = []
    visitado = np.zeros_like (img, dtype=bool) # matriz de controle para visitados

    #definindo a função flodd_fill internamente
    def flood_fill(img, visitado, r, c, pixels_componente, retang):
        altura, largura = img.shape[:2]

        # Marca como visitado
        visitado[r, c] = True
        pixels_componente.append((r, c))

        # Atualiza bounding box (retângulo envolvente)
        retang['min_r'] = min(retang['min_r'], r)
        retang['max_r'] = max(retang['max_r'], r)
        retang['min_c'] = min(retang['min_c'], c)
        retang['max_c'] = max(retang['max_c'], c)

        # Vizinhos (8 conectividade)
        vizinhos = [(0, 1), (0, -1), (1, 0), (-1, 0),
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in vizinhos:
            nr, nc = r + dr, c + dc
            if 0 <= nr < altura and 0 <= nc < largura:
                if img[nr, nc] == 1 and not visitado[nr, nc]:
                    flood_fill(img, visitado, nr, nc, pixels_componente, retang)

    for i in range(altura):
        for j in range(largura):
            if img[i, j] == 1 and not visitado[i, j]:
                pixels_componente = []
                retang = {
                    'min_r': i, 'max_r': i,
                    'min_c': j, 'max_c': j
                }

                #  Chamada recursiva começa aqui
                flood_fill(img, visitado, i, j, pixels_componente, retang)

                n_pixels = len(pixels_componente)
                largura_comp = retang['max_c'] - retang['min_c'] + 1
                altura_comp = retang['max_r'] - retang['min_r'] + 1

                if (n_pixels >= n_pixels_min and
                    largura_comp >= largura_min and
                    altura_comp >= altura_min):
                    
                    componente = {
                        'label': rotulo_atual,
                        'n_pixels': n_pixels,
                        'T': retang['min_r'],
                        'L': retang['min_c'],
                        'B': retang['max_r'],
                        'R': retang['max_c']
                    }
                    componentes.append(componente)

                    # (Opcional) Marcar na imagem
                    for (r, c) in pixels_componente:
                        img[r, c] = rotulo_atual

                    rotulo_atual += 0.1

    return componentes


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
