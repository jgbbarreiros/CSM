# -*- coding: utf-8 -*-

from time import time
from os import path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math


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
    data = zip(*s)[1]
    symb = codeTree(zip(*s)[0])
    # [list(c) for c in zip(data, symb)]
    return [dict(zip(data, symb)), dict(zip(symb, data))]

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
            fl[i] = '0' + str(fl[i])
    if len(r) == 1:
        fr = ['1']
    else:
        fr = codeTree(r)
        for i in range(len(fr)):
            fr[i] = '1' + str(fr[i])
    return fl+fr

def compress(data, table):
    code = []
    for i in range(len(data)):
        code += map(int, table.get(data[i]))
    return code

def write(seqBits, fileName):
    packed = np.packbits(seqBits)
    np.save(fileName, packed)
    return packed

def read(fileName):
    compressedFile = np.load(fileName)
    seqBits = np.unpackbits(compressedFile)
    return seqBits

def decompress(seqBits, table):
    data = []
    symb = ''
    for i in range(len(seqBits)):
        symb += str(seqBits[i])
        if table.has_key(symb):
            data.append(table.get(symb))
            symb = ''
    return data

def calcEntropy(prob):
    entropy = 0
    total = sum(prob)

    for i in range(len(prob)):
        probs = prob[i]/float(total)
        if probs != 0.0:
            entropy +=  probs*math.log(probs, 2)
    return -entropy


def calcAverageBitSymb(table):
    totalBits = 0
    for i in range(len(table)):
        totalBits += len(table[i][1])
    razao = totalBits/len(table)
    return razao


def calcEficiencia(entropia, media):
    eficiencia = entropia/float(media)
    return eficiencia

if __name__ == "__main__":

    img = Image.open("lena.tiff")

    #create histogram
    hist = img.histogram()
    plt.plot(hist)

    # convert image into a sequence
    imgData0 = img.getdata()

    # Shannon-Fano coding
    t0 = time()
    codeTables = shannonFano(np.arange(0,256),hist)
    t1 = time()
    print "time:" + str(t1 - t0)

    entropia = calcEntropy(hist)
    print 'Entropy = ' + str(entropia)

    # media = calcAverageBitSymb(codeTables[1])
    # print 'Media de bits por simbolo = ' + str(media)

    # eficiencia = calcEficiencia(entropia, media)
    # print 'Eficiencia = ' + str(eficiencia)

    # codifica e grava ficheiro
    seqBit0 = compress(imgData0, codeTables[0])
    write(seqBit0, 'lena')
    t2 = time()
    print "time:" + str(t2 - t1)

    # lê ficheiro e descodifica
    seqBit1 = read('lena.npy')
    imgData1 = decompress(seqBit1, codeTables[1])
    t3 = time()
    print "time: " + str(t3 - t2)

    # print imgData1
    sizeIni = path.getsize('lena.tiff')
    sizeEnd = path.getsize('lena.npy')
    print "taxa: " + str(1.* sizeIni / sizeEnd)