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


def snr_practical(s, eq):
    """
    s = signal
    eq = erro quantificacao
    ps = soma das amostras (de um sinal) ao quadrado / comprimento do sinal
    pr = soma do erro de quantificacao ao quadrado / comprimento do erro de quant
    """
    ps = np.sum(s ** 2) / len(s)
    pr = np.sum(eq ** 2) / len(eq)
    return 10 * np.log10(ps/pr)

def twos_complement(bin):
    comp = ''
    for i in range(len(bin)):
        if bin[i] == '0':
            comp += '1'
        else:
            comp += '0'
    return comp

def write(seqBits, fileName):
    packed = np.packbits(seqBits)
    np.save(fileName, packed)
    return packed


def read(fileName):
    compressedFile = np.load(fileName)
    seqBits = np.unpackbits(compressedFile)
    return seqBits


if __name__ == "__main__":
    # bloco_dct = dct(dct(bloco.T, norm='ortho').T , norm='ortho')

    I = readImage('lena.tiff')
    print "Image %s:\n%s\n" % (I.shape, I)

    Blocos = getBlocos(I)

    qualidade = 50
    a = quality_factor(qualidade)
    print "alfa:\n%s\n" % a

    DC = []
    code = []

    # compressao
    for B in Blocos:

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
        if len(DC) != 0:
            DC_diff = BQ[0][0] - DC[-1]
        else:
            DC_diff = BQ[0][0]
        print "DC = %s" % DC_diff
        DC.append(BQ[0][0])
        DC_code = ''
        if DC_diff < 0:
            DC_bin = bin(DC_diff)[3:]
            DC_code += K3.get(len(DC_bin)) + twos_complement(DC_bin)
        elif DC_diff == 0:
            DC_code += "00"
        else:
            DC_bin = bin(DC_diff)[2:]
            DC_code += K3.get(len(DC_bin)) + DC_bin

        code += map(int, DC_code)

        # codificador AC
        AC_code = ''
        numZeros = 0
        BQ_zz = BQ.flatten(order='F')[np.argsort(ind_zz)].astype(int)
        print BQ_zz
        print "AC = ",
        # for i in range(1, len(BQ_zz)):

        i = 1
        while i < len(BQ_zz):
            if BQ_zz[i] != 0:
                print (numZeros, len(bin(abs(BQ_zz[i]))[2:])),
                AC_code += K5.get((numZeros, len(bin(abs(BQ_zz[i]))[2:])))
                # print (numZeros, len(bin(abs(BQ_zz[i]))[2:])),
                # print "---0"
                if BQ_zz[i] < 0:
                    AC_bin = bin(BQ_zz[i])[3:]
                    AC_code += twos_complement(AC_bin)
                    print twos_complement(AC_bin),
                    # print "---1"
                elif BQ_zz[i] > 0:
                    AC_code += bin(BQ_zz[i])[2:]
                    print BQ_zz[i],
                    # print "---2"
                numZeros = 0
            else:
                if sum(BQ_zz[i:]!=0) == 0:
                    AC_code += K5.get((0,0))
                    print (0,0)
                    break
                if (i + 15) < len(BQ_zz) and sum(BQ_zz[i:i+15]!=0) == 0:
                    AC_code += K5.get((15,len(bin(abs(BQ_zz[i+15]))[2:])))
                    print (15,len(bin(abs(BQ_zz[i+15]))[2:])),
                    i += 16
                    numZeros =0
                    pass
                numZeros +=1
            i += 1

        code += map(int, AC_code)

        print 'DC_code %s' % DC_code
        print 'AC_code %s' % AC_code
        print "\n--------------------------"

    print 'code %s' % code

    write(code, 'lena')

    # descompressao