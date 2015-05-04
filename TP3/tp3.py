from scipy.fftpack import dct, idct
from PIL import Image
import numpy as np
import scipy as sp
from time import time
from os import path
import scipy.misc as mi
from Tables_jpeg import *

def to_dct(array):
    B = dct(dct(array.T*1., norm='ortho').T, norm='ortho')
    return B

def to_idct(array):
    C = idct(idct(array.T*1., norm='ortho').T, norm='ortho')
    return C

def comp_dct(img):
    len_x = len(img) - len(img)%8
    len_y = len(img[0]) - len(img[0])%8
    aux = np.zeros((len_x,len_y))
    for i in range(len_x/8):
        for j in range(len_y/8):
            aux[i*8:(i+1)*8,j*0:(j+1)*8]=to_dct(img[i*8:(i+1)*8,j*0:(j+1)*8])
    return aux

def decomp_idct(dct):
   aux = np.zeros((len(dct),len(dct)))
   for i in range(len(dct)/8):
        for j in range(len(dct)/8):
            aux[i*8:(i+1)*8,j*0:(j+1)*8] = to_idct(dct[i*8:(i+1)*8,j*0:(j+1)*8])
   return aux



# if __name__ == "__main__":
#     i = mi.imread('lena.tiff')
#     print '---------------original img---------------'
#     print i
# 
#     #a = i[0:8,0:8]
#     #B = to_dct(a)
#     #print B
#     #C = to_idct(B)
#     #print C
#     print '---------------img to dct---------------'
#     print
#     dct = comp_dct(i)
#     print dct
#     print '---------------dct to img---------------'
#     img = decomp_idct(dct)
#     print img
    

if __name__ == "__main__":
    # bloco_dct = dct(dct(bloco.T, norm='ortho').T , norm='ortho')

    I = mi.imread('lena.tiff')
    print "Image " + str(I.shape) + ":"
    print I
    print

    # first block
    B = I[0:8, 0:8]
    print "first block"
    print B
    print

    # dct
    C = dct(dct(B.T*1., norm='ortho').T , norm='ortho')
    print "DTC:"
    print C
    print

    # idct
    B2 = idct(idct(C.T*1., norm='ortho').T , norm='ortho')
    print "IDCT (comparacao):"
    print B[0]
    print B2[0]
    print

    # quantificacao
    qualidade = 50
    a = quality_factor(qualidade)
    print "alfa:"
    print a
    print

    BQ = np.round(C/(a*Q))
    print "Bloco quantificado:"
    print BQ
    print

    # desquantificao
    C2 = a*Q*BQ
    print "Bloco desquantificado (comparacao):"
    print C[0]
    print C2[0]
    print

    # codificador DC
    DC = BQ[0]

    # codificador AC
    AC = []
    numZeros = 0
    BQ1 = BQ.reshape(64,order='F').astype('int16')
    for i in range(len(BQ1)-1):
        i += 1
        if BQ1[i] != 0:
            AC.append((numZeros, BQ1[i]))
            numZeros = 0
        else:
            numZeros +=1
        if i == (len(BQ1)-1):
            AC.append((0,0))
    print AC
