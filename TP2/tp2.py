# -*- coding: utf-8 -*-

from time import time
from os import path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def shannonFano(simbols, prob):
    size = 0
    for i in range(len(prob)):
        if prob[i] != 0:
            size += 1
    probNoZeros = np.empty((size, 2), dtype=int)
    pos = 0
    for i in range(len(prob)):
        if prob[i] != 0:
            probNoZeros[pos][0] = prob[i]
            probNoZeros[pos][1] = simbols[i]
            pos += 1
    s = sorted(probNoZeros, key=lambda x: -x[0])
    idx = zip(*s)[1]
    code = codeTree(zip(*s)[0])

    return [list(c) for c in zip(idx, code)]

def codeTree(prob):
    l = 0
    r = 0
    for i in range(len(prob)):
        l = prob[:i + 1]
        r = prob[i + 1:]
        if sum(l) >= sum(r):
            break
    if len(l) == 1:
        fl = ['0']
    else:
        fl = codeTree(l)
        for i in range(len(fl)):
            fl[i] = '0' + fl[i]
    if len(r) == 1:
        fr = ['1']
    else:
        fr = codeTree(r)
        for i in range(len(fr)):
            fr[i] = '1' + fr[i]
    return fl+fr

def compress(data, table):
    code = []
    for i in range(len(data)):
        for j in range(len(table)):
            if data[i] == table[j][0]:
                code += map(int, table[j][1])
    return code

def write(seqBits, fileName):
    packed = np.packbits(seqBits)
    np.save(fileName, packed)
    return packed

def read(fileName):
    file = np.load(fileName)
    seqBits = np.unpackbits(file)
    return seqBits

def decompress(seqBits, table):
    data = []
    symb = ''
    for i in range(len(seqBits)):
        symb += str(seqBits[i])
        for j in range(len(table)):
            if symb == table[j][1]:
                data.append(table[j][0])
    return data

if __name__ == "__main__":

    img = Image.open("lena.tiff")

    #create histogram
    h = img.histogram()
    plt.plot(h)

    # convert image into a sequence
    imgData0 = img.getdata()

    # Shannon-Fano coding
    t0 = time()
    codeTable = shannonFano(np.arange(0,256),h)
    t1 = time()
    print "time:" + str(t1 - t0)

    # codifica e grava ficheiro
    seqBit0 = compress(imgData0, codeTable)
    write(seqBit0, 'lena')
    t2 = time()
    print "time:" + str(t2 - t1)

    # lê ficheiro e descodifica
    seqBit1 = read('lena.npy')
    imgData1 = decompress(seqBit1, codeTable)
    t3 = time()
    print "time: " + str(t3 - t2)

    sizeIni = path.getsize('lena.tiff')
    sizeEnd = path.getsize('lena.npy')
    print "taxa: " + str(1.* sizeIni / sizeEnd)