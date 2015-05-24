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

def blockshaped(arr, nrows, ncols):
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))

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

def unblockshaped(arr, h, w):
    #array, 512,512
    n, nrows, ncols = arr.shape
    return (arr.reshape(h//nrows, -1, nrows, ncols)
               .swapaxes(1,2)
               .reshape(h, w))

def decode(seqBits, K3_inv, K5_inv):
    blocos = []
    bloco = np.zeros(64)
    bloco_pos = 1
    symb = ''
    isDC = True
    # for i in range(len(seqBits)):
    i = 0
    DC = []
    while i < len(seqBits):
        symb += str(seqBits[i])
        if  isDC:
            if K3_inv.has_key(symb):
                size = K3_inv.get(symb)
                if size is 0:
                    num = 0
                else:
                    num_bin = ''.join(map(str, seqBits[i+1:i+1+size]))
                    if num_bin[0] == '0':
                        num_bin = '-'+twos_complement(num_bin)
                    num = int(num_bin, 2)
                    if num_bin[0] == 0:
                        num *= -1
                if len(DC) > 0:
                    bloco[0] = DC[-1] + num
                else:
                    bloco[0] = num
                DC.append(bloco[0])
                i += size
                symb = ''
                isDC = False
        else:
            if K5_inv.has_key(symb):
                t = K5_inv.get(symb)
                if t == (0,0):
                    bloco_pos = 1
                    blocos.append(np.reshape(bloco[ind_zz], (8,8)).T.astype(int))
                    isDC = True
                elif t == (15, 0):
                    bloco_pos += 16
                else:
                    num_zeros = t[0]
                    size = t[1]
                    num_bin = ''.join(map(str, seqBits[i+1:i+1+size]))
                    if num_bin[0] == '0':
                        num_bin = '-'+twos_complement(num_bin)
                    num = int(num_bin, 2)
                    bloco[bloco_pos + num_zeros] = num
                    bloco_pos += num_zeros + 1
                    i += size
                symb = ''
        i += 1
    #     if dic.has_key(symb):
    #         data.append(dic.get(symb))
    #         symb = ''
    return blocos


if __name__ == "__main__":
    # bloco_dct = dct(dct(bloco.T, norm='ortho').T , norm='ortho')

    I = readImage('lena.tiff')
    print "Image %s:\n%s\n" % (I.shape, I)

    Blocos = blockshaped(I,8,8)

    #Blocos = getBlocos(I)


    Blocos = np.asarray(Blocos)
    # print Blocos.shape
    # Blocos = unblockshaped(Blocos,512,512)
    # print Blocos


    qualidade = 50
    a = quality_factor(qualidade)
    print "alfa:\n%s\n" % a

    DC = []
    code = []

    # compressao
    for B in Blocos:

        print "--------------------------"

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
        # print BQ
        BQ_zz = BQ.flatten(order='F')[np.argsort(ind_zz)].astype(int)
        # print BQ_zz

        print "AC =",
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
                #se do i para a frente for tudo zero
                if sum(BQ_zz[i:]!=0) == 0:
                    AC_code += K5.get((0,0))
                    print (0,0)
                    break
                #se tivermos dentro do len e se nos proximos 15 forem todos zero
                if (i + 15) < len(BQ_zz) and sum(BQ_zz[i:i+15]!=0) == 0:
                    if BQ_zz[i+15] == 0:
                        AC_code += K5.get((15,0))
                        print (15,0),
                    else:
                        AC_code += K5.get((15,len(bin(abs(BQ_zz[i+15]))[2:])))
                        print (15,len(bin(abs(BQ_zz[i+15]))[2:])),
                    i += 16
                    numZeros =0
                    pass
                numZeros +=1
            i += 1

        code += map(int, AC_code)

        # print 'DC_code %s' % DC_code
        # print 'AC_code %s' % AC_code
        print "--------------------------\n"

    print 'code %s' % code

    write(code, 'lena')
    code1 = read('lena.npy')

    print 'code %s' % code1

    Blocos_Q1 = decode(code1[:len(code1)-2], K3_inv, K5_inv)
    Blocos_Q1_test = np.asarray(Blocos_Q1)
    #shape errada ja aqui
    print Blocos_Q1_test.shape

    #print "Bloco quantificado:\n%s\n" % Blocos_Q1

    Blocos1 = []

    for Bloco_Q1 in Blocos_Q1:
        C2 = a*Q*Bloco_Q1
        B2 = idct(idct(C2.T*1., norm='ortho').T , norm='ortho')
        Blocos1.append(B2)

    Blocos1 = np.asarray(Blocos1)
    print Blocos1.shape
    #unblockshaped(Blocos1,512, 512)


    # descompressao