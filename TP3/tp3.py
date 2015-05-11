from scipy.fftpack import dct, idct
from PIL import Image
import numpy as np
import scipy as sp
from time import time
from os import path
import scipy.misc as mi
from Tables_jpeg import *

def readImage(name):
    return mi.imread('lena.tiff')

def getBlocos(img):
    Blocos = []
    for x in range(I.shape[0]/8):
        for y in range(I.shape[1]/8):
            Blocos.append(I[x*8:(x+1)*8, y*8:(y+1)*8])
    return Blocos

def getDct(bloc):
    return dct(dct(bloc.T*1., norm='ortho').T , norm='ortho')

def getIdct(dct):
    return idct(idct(dct.T*1., norm='ortho').T , norm='ortho')

def string_to_array(s):
    a = np.zeros(len(s),dtype=np.uint8)
    for i in range(len(s)):
        a[i]=s[i]
    return a


if __name__ == "__main__":
    # bloco_dct = dct(dct(bloco.T, norm='ortho').T , norm='ortho')

    I = readImage('lena.tiff')
    print "Image %s:\n%s\n" % (I.shape, I)

    Blocos = getBlocos(I)

    qualidade = 50
    a = quality_factor(qualidade)
    print "alfa:\n%s\n" % a

    DC = []

    # compressao
    for B in Blocos[:3]:

        # dct
        C = getDct(B)
        # print "DCT:\n%s\n" % C

        # idct
        # B2 = idct(idct(C.T*1., norm='ortho').T , norm='ortho')
        # print "IDCT (comparacao):\n%s\n%s\n" % (B, B2)

        # quantificacao
        BQ = np.round(C/(a*Q)).astype('int')
        print "Bloco quantificado:\n%s\n" % BQ

        # desquantificao
        # C2 = a*Q*BQ
        # print "Bloco desquantificado (comparacao):\n%s\n%s\n" % (C, C2)

        # codificador DC
        DC_diff = BQ[0][0] - DC[-1]
        DC.append(BQ[0][0])
        if DC_diff < 0:
            DC_bin = bin(DC_diff)[3:]
            for i in range(len(DC_bin)):
                if DC_bin[i] == '0':
                    DC_bin[i] = '1'
                else:
                    DC_bin[i] = '0'
            DC_code = K3.get(len(DC_bin)) + DC_bin
        elif DC_diff == 0:
            DC_code = "00"
        else:
            DC_bin = bin(DC_diff)[2:]
            DC_code = K3.get(len(DC_bin)) + DC_bin

        # codificador AC
        AC_e = []
        numZeros = 0
        BQ_zz = BQ.flatten(order='F')[np.argsort(ind_zz)].astype(int)
        for i in range(1, len(BQ_zz)):
            if BQ_zz[i] != 0:
                AC_e.append((numZeros, BQ_zz[i]))
                numZeros = 0
            else:
                numZeros +=1
            if i == len(BQ_zz)-1:
                AC_e.append((0,0))
        AC.append(AC_e)

    print 'numsDC %s' % DC
    print 'DC %s' % DC
    print 'AC %s' % AC

    # descompressao