#===============================================================================
# Atividade: Trabalho 4 - Contagem de Arroz
# Aluna: Ana Beatriz Kindinger
#-------------------------------------------------------------------------------
# Enunciado: 
'''Objetivo: escreva um programa para estimar quantos grãos de arroz aparecem em cada uma das imagens dadas (e, possivelmente, em outras que não sejam estas!).
-> IMPORTANTE: Use os mesmos parâmetros para todas as imagens.
10% de tolerancia de erros
'''
#-------------------------------------------------------------------------------
# # Universidade Tecnológica Federal do Paraná
#===============================================================================

import numpy as np
import cv2
import sys

#===============================================================================

def binarizar(img):
    img_binarizada = np.zeros_like(img)
    borrada = cv2.GaussianBlur(img, (11,11), 0)

    img_binarizada = cv2.adaptiveThreshold(borrada, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  cv2.THRESH_BINARY_INV, 11,4) 


    return img_binarizada



#===============================================================================
INPUT_IMAGES = [
    '60.bmp',
    '82.bmp',
    '114.bmp',
    '150.bmp',
    '205.bmp'
]


#===============================================================================

#abrindo a primeira imagem
img0 = cv2.imread (INPUT_IMAGES[3], cv2.IMREAD_GRAYSCALE)
if img0 is None:
    print ('Erro abrindo a imagem.\n')
    sys.exit ()




img0_bin = binarizar(img0)

cv2.imshow('Binarizada', img0_bin)
cv2.imshow('Original', img0)
cv2.waitKey (0)
cv2.destroyAllWindows ()
    
    
    
    
    
    
    
