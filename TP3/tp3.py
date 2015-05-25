from scipy.fftpack import dct, idct
from PIL import Image
import numpy as np
import scipy as sp
from time import time
from os import path
import matplotlib.pyplot as plt
import scipy.misc as mi
from Tables_jpeg import *

def readImage(name):
    return mi.imread('lena.tiff')


def blockShaped(arr, nrows, ncols):
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1, nrows, ncols))

def unblockShaped(arr, h, w):
    #array, 512,512
    n, nrows, ncols = arr.shape
    return (arr.reshape(h//nrows, -1, nrows, ncols).swapaxes(1,2).reshape(h, w))

def DCTransform(blocksIMG):
    DCT = []
    for block in blocksIMG:
        DCT.append(dct(dct(block.T*1., norm='ortho').T , norm='ortho'))
    return DCT

def IDCTransform(blocksDCT):
    IDCT = []
    for block in blocksDCT:
        IDCT.append(idct(idct(block.T*1., norm='ortho').T , norm='ortho').astype('int'))
    return IDCT

def quantify(blocksDCT):
    BQ = []
    for block in blocksDCT:
        BQ.append(np.round(block/(a*Q)).astype('int'))
    return BQ

def dequantify(blocksQ):
    DCT = []
    for block in blocksQ:
        DCT.append(a*Q*block)
    return DCT

def twos_complement(bin):
    comp = ''
    for i in range(len(bin)):
        if bin[i] == '0':
            comp += '1'
        else:
            comp += '0'
    return comp

def code(blocksQ):
    DC = []
    code = []

    for BQ in blocksQ:
        # codificador DC
        if len(DC) != 0:
            DC_diff = BQ[0][0] - DC[-1]
        else:
            DC_diff = BQ[0][0]
        # print "DC = %s" % DC_diff
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

        # print "AC =",
        i = 1
        while i < len(BQ_zz):
            if BQ_zz[i] != 0:
                AC_code += K5.get((numZeros, len(bin(abs(BQ_zz[i]))[2:])))
                # print (numZeros, len(bin(abs(BQ_zz[i]))[2:])),
                if BQ_zz[i] < 0:
                    AC_bin = bin(BQ_zz[i])[3:]
                    AC_code += twos_complement(AC_bin)
                    # print twos_complement(AC_bin),
                elif BQ_zz[i] > 0:
                    AC_code += bin(BQ_zz[i])[2:]
                    # print bin(BQ_zz[i])[2:],
                numZeros = 0
                if i+1 >= len(BQ_zz):
                    AC_code += K5.get((0,0))
                    # print (0,0)
                    break
            else:
                #se do i para a frente for tudo zero
                if sum(BQ_zz[i:]!=0) == 0:
                    AC_code += K5.get((0,0))
                    # print (0,0)
                    break
                #se tivermos dentro do len e se nos proximos 15 forem todos zero
                if (i + 15) < len(BQ_zz) and sum(BQ_zz[i:i+15]!=0) == 0:
                    if BQ_zz[i+15] == 0:
                        AC_code += K5.get((15,0))
                        # print (15,0),
                    else:
                        AC_code += K5.get((15,len(bin(abs(BQ_zz[i+15]))[2:])))
                        # print (15,len(bin(abs(BQ_zz[i+15]))[2:])),
                        if BQ_zz[i+15] < 0:
                            AC_bin = bin(BQ_zz[i+15])[3:]
                            AC_code += twos_complement(AC_bin)
                            # print twos_complement(AC_bin),
                        elif BQ_zz[i+15] > 0:
                            AC_code += bin(BQ_zz[i+15])[2:]
                            # print BQ_zz[i+15],
                    i += 16
                    if i+16 >= len(BQ_zz):
                        AC_code += K5.get((0,0))
                        # print (0,0),
                        break
                    numZeros =0
                    pass
                numZeros +=1
            i += 1

        code += map(int, AC_code)
    return code

def decode(seqBits):
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
                # print '\nAC =',
        else:
            if K5_inv.has_key(symb):
                t = K5_inv.get(symb)
                if t == (0,0):
                    # print '(0, 0)',
                    bloco_pos = 1
                    blocos.append(np.reshape(bloco[ind_zz], (8,8)).T.astype(int))
                    bloco = np.zeros(64)
                    isDC = True
                elif t == (15, 0):
                    # print '(15, 0)',
                    bloco_pos += 16
                else:
                    num_zeros = t[0]
                    size = t[1]
                    num_bin = ''.join(map(str, seqBits[i+1:i+1+size]))
                    # print '(' + str(num_zeros) +', '+ str(size) + ') ' + str(num_bin),
                    if num_bin[0] == '0':
                        num_bin = '-'+twos_complement(num_bin)
                    num = int(num_bin, 2)
                    bloco[bloco_pos + num_zeros] = num
                    bloco_pos += num_zeros + 1
                    i += size
                symb = ''
        i += 1
    # print
    return blocos

def SNR(original, quantificado):

    original = np.asarray(original).reshape(-1).astype('float')
    quantificado = np.asarray(quantificado).reshape(-1).astype('float')

    erro = quantificado - original
    SNR = 10.*np.log10(sum(original**2)/sum(erro**2))

    return SNR


def write(seqBits, fileName):
    packed = np.packbits(seqBits)
    np.save(fileName, packed)
    return packed


def read(fileName):
    compressedFile = np.load(fileName)
    seqBits = np.unpackbits(compressedFile)
    return seqBits[:len(CODE)]


if __name__ == "__main__":

    sizeIni = 1. * path.getsize('lena.tiff')
    print "tamanho lena.tiff %s" % sizeIni
    qualitys = [10,25,50,75,90]
    snrs = []
    txs  = []

    for i in range(len(qualitys)):


        quality = qualitys[i]
        print 'comprimindo imagem com qualidade %s...' % quality

        I = readImage('lena.tiff')
        # print "Image %s:\n%s\n" % (I.shape, I)

        BLOCKS = blockShaped(I, I.shape[0]/64, I.shape[1]/64)
        # print "Blocks:\n%s\n" % BLOCKS

        a = quality_factor(quality)
        # print "alfa:\n%s\n" % a

        DCT = DCTransform(BLOCKS)
        # print "DCT:\n%s\n" % DCT

        BQ = quantify(DCT)
        # print "Quantified:\n%s\n" % BQ

        t0 = time()
        CODE = code(BQ)
        t1 = time()
        print "time code: " + str(t1 - t0)
        # print "code:\n%s\n" % CODE

        write(CODE, 'lena'+str(quality))
        CODE1 = read('lena'+str(quality)+'.npy')
        # print "code new:\n%s\n" % CODE1

        t0 = time()
        BQ1 = decode(CODE1)
        t1 = time()
        print "time decode: " + str(t1 - t0)
        # print "Quantified new:\n%s\n" % BQ1

        DCT1 = dequantify(BQ1)
        # print "DCT new:\n%s\n" % DCT1

        BLOCKS1 = IDCTransform(DCT1)
        # print "BLOCKS new:\n%s\n" % BLOCKS1

        I1 = unblockShaped(np.asarray(BLOCKS1), 512, 512)
        # print "Image new:\n%s\n" % I1

        img = Image.fromarray(I1.astype('uint8'), 'L')
        img.save("lenaJPEG"+str(quality)+".bmp")

        snr = SNR(I,I1)
        print "snr: %s" % snr
        snrs.append(snr)

        sizeEnd = path.getsize('lena'+str(quality)+'.npy')
        print "lena.npy size:  %s" % sizeEnd

        tx = sizeIni/sizeEnd
        print "taxa: %s" % tx
        txs.append(tx)
        print


    plt.figure()
    plt.grid(True)
    plt.plot(snrs, txs)
    plt.xlabel("SNR")
    plt.ylabel("taxa de compressao")

    x = Image.open("lena.tiff")
    x.save("lena.jpeg", "JPEG", quality=50)
    sizeJPG = path.getsize('lena.jpeg')
    print "taxa jpg: %s" % (sizeIni/sizeJPG)

    plt.show()