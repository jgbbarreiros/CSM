from scipy.fftpack import dct, idct
from PIL import Image
import numpy as np
import scipy as sp
from time import time
from os import path
import scipy.misc as mi
from Tables_jpeg import *


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
