# imports
import numpy as np
from PIL import Image
import time

# functions
def bin_code_shannon_fano(prob):
    i = np.argsort(prob)[::-1][:len(prob)]
    s = sorted(prob, reverse=True)
    c = code_tree(s)
    f = np.empty((len(c)), dtype='|S' + str(len(c)))

    for x in range(len(c)):
        f[i[x]] = c[x]
    return f


def code_tree(prob):
    l = 0
    r = 0
    for i in range(len(prob)):
        l = prob[:i + 1]
        r = prob[i + 1:]
        if sum(l) >= sum(r):
            break
    if len(l) == 1:
        fl = np.array(['0'], dtype='|S100')
    else:
        fl = code_tree(l)
        for i in range(len(fl)):
            fl[i] = '0' + str(fl[i])

    if len(r) == 1:
        fr = np.array(['1'], dtype='|S100')
    else:
        fr = code_tree(r)
        for i in range(len(fr)):
            fr[i] = '1' + str(fr[i])
    return np.hstack((fl, fr))


def compress(symb, table, word):
    bits = ''
    for i in range(len(word)):
        for j in range(len(symb)):
            if (word[i] == symb[j]):
                bits = bits + str(table[j])
                j = -1
    return bits


# symbols = ["a","b","c","d","e"]
#table = ['111' '10' '01' '110' '00']
#bits = 111100111000
def decompress(symb, table, bits):
    word = ''
    aux = ''
    for i in range(len(bits)):
        aux += bits[i]
        for j in range(len(symb)):
            if (aux == table[j]):
                word += symb[j]
                aux = ''
    return word


def zeros(hist):
    size = 0
    for i in range(len(hist)):
        if hist[i] != 0:
            size += 1
    result = np.zeros((2, size))

    aux = 0
    for i in range(len(hist)):
        if hist[i] != 0:
            result[0][aux] = hist[i]
            result[1][aux] = i
            aux += 1
    return result

# main
if __name__ == "__main__":

    millis = lambda: int(round(time.time() * 1000))

    # ex 1
    symbols = np.array(["a", "b", "c", "d", "e"])
    table = np.array(['111', '10', '01', '110', '00'])
    probability = [.10, .20, .30, .10, .30]
    bin_table = bin_code_shannon_fano(probability)

    print bin_table

    # ex 2 e 3
    print bin_code_shannon_fano(probability)
    print compress(symbols, bin_code_shannon_fano(probability), symbols)
    print decompress(symbols, table, '111100111000')

    # ex 4

    # A
    lena = Image.open("lenac.tif").convert("L")
    hist = lena.histogram()

    hist_no_zeros = zeros(hist)[0]
    hist_idx = zeros(hist)[1]

    before = millis()
    lena_code = bin_code_shannon_fano(hist_no_zeros)
    diff = millis() - before
    # file = open('file_name3', 'wb')
    # file.write()

    # print diff
    #

    print hist_no_zeros[:4]
    print lena_code[:4]
    img = np.array(lena)
    print img

    # img  = [162, 162, 162]
    img_code = np.zeros((lena.size[1], lena.size[0]))
    print img_code
    for y in range(lena.size[1]):  # linha
         for x in range(lena.size[0]):  # coluna
             for i in range(len(hist_no_zeros)):  #
                 if img[y][x] == hist_no_zeros[i]:
                     pass
                     #escrever para um ficheiro o lena_code[i]

    # print lena.size[0]
    # print np.zeros((3, 2))

    # '0000' '1111' '2222' '3333'
    # '0000111122223333'
    # '00001111'

    # [[1,1,1,1,1,1,1,1,1,1,], [1,1,1,1,1,1,1,1,1,0,0]]
    # [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0]
    # [[1,1,1,1,1,1,1,1], [1,1,1,1,1,1,1,1], [1,1,1,0,0,0,0,0]]

    """
    hist = [3, 1, 3, 0, 6]
    hist_no_zeros = [3, 1, 3, 6]
    idx = [0, 1, 2, 4]
    code = ['01', '00', '101', '111']
    """

    # # img  = [162, 162, 162]
    # a = np.zeros((lena.size[1], lena.size[0]))
    # for y in range(lena.size[1]):  # linha
    #     for x in range(lena.size[0]):  # coluna
    #         for i in range(len(idx)):  #
    #             if img[y][x] == idx[i]:
    #                 a[y][x] = code[i]
    #
    #
    #                 #B