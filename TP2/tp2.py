# imports
import numpy as np
from PIL import Image
import time

# functions
def shannon_fano(hist):

    clean_hist = zeros(hist)

    hist_no_zeros = clean_hist[0]
    hist_idx = clean_hist[1]

    print "hist no zeros / idx:"
    print hist_no_zeros[:10]
    print hist_idx[:10]
    print

    i = np.argsort(hist_no_zeros)[::-1][:len(hist_no_zeros)]
    s = sorted(hist_no_zeros, reverse=True)
    c = code_tree(s)
    f = np.empty((len(c)), dtype='|S' + str(len(c)))

    for x in range(len(c)):
        f[i[x]] = c[x]

    num_bits_symb = media_bits(f)

    print "numero medio de bits por simbolo:"
    print num_bits_symb
    print

    print "entropia:"
    print "falta a entropia"
    print

    return dic(f, hist_idx)

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

def media_bits(symb):
    total = len(symb)
    soma = 0
    for i in range(total):
        soma +=len(symb[i])
    return soma/float(total)

def dic(symb, idx):
    dic = {}
    for i in range(len(idx)):
        c = str(symb[i])
        dic.update({idx[i]:c})
    return dic

def compress2(symb, table, word):
    bits = ''
    for i in range(len(word)):
        for j in range(len(symb)):
            if word[i] == symb[j]:
                bits += str(table[j])
                j = -1
    return bits

def compress(data, dic):
    code_str=''
    row_size = len(data)
    col_size = len(data[0])
    for y in range(row_size):  #linha
        for x in range(col_size):  #coluna
            code_str += dic[data[y][x]]

    # size_str = ''
    # size_str += str(bin(row_size)[2:]) + str(bin(col_size)[2:])


    # len(size_str) + len(dic_comp) +
    code = np.zeros(len(code_str), dtype=np.uint8)
    # pos = 0


    # for i in range(len(size_str)):
    #     code[pos] = size_str[i]
    #     pos += 1

    for i in range(len(code)):
        code[i] = code_str[i]
        # pos += 1
    return code

def write(code, file_name):
    packed = np.packbits(code)
    file_w = open(file_name, 'wb')
    img = ''
    for i in range(len(packed)):
        img += str(chr(int(packed[i])))
    file_w.write(img)
    file_w.close()

def read(file_name):
    file_r = open(file_name, 'rb')
    img = file_r.read()
    code = np.zeros(len(img), dtype=np.uint8)
    for i in range(len(code)):
        code[i] = ord(img[i])
    return np.unpackbits(code)[:-1]

def decompress2(symb, table, bits):
    word = ''
    aux = ''
    for i in range(len(bits)):
        aux += bits[i]
        for j in range(len(symb)):
            if aux == table[j]:
                word += symb[j]
                aux = ''
    return word

#code = [0,1,1,0,0,1,1,0,0,]
#dic = {'10':24, '11':25}
def decompress(code, dic):
    symb = ""
    pos = 0
    size = [512,512]
    decomp_img = np.zeros((size[0],size[1]))
    for y in range(size[0]): # linha
        for x in range(size[1]): # coluna
            for i in range(pos, len(code)):
                symb += str(code[i])
                if dic.get(symb) != None:
                    #print symb
                    decomp_img[y][x] = dic.get(symb)
                    symb = ""
                    pos = i+1
                    break
    return decomp_img


# main
if __name__ == "__main__":

    millis = lambda: int(round(time.time() * 1000))

    # ex 1
    print "ex 1"
    print "####\n"
    word = 'babe'
    symbols = np.array(['a', 'b', 'c', 'd', 'e'])
    table = np.array(['111', '10', '01', '110', '00'])
    probability = [.10, .20, .30, .10, .30]
    idx = [0, 1, 2, 3, 4]
    # bin_table = bin_code_shannon_fano(probability)
    # print bin_table
    print "\n"

    # ex 2 e 3
    print "ex 2 e 3"
    print "########\n"
    # comp = compress(symbols, bin_table, word)
    # print comp
    # decomp = decompress(symbols, table, comp)
    # print decomp
    print "\n"

    # ex 4
    print "ex 4"
    print "####\n"

    # A
    lena = Image.open("lenac.tif").convert("L")
    lena_data = np.array(lena)
    print "lena:"
    print lena_data[:2]
    print

    hist = lena.histogram()
    print "hist:"
    print hist[:30]
    print

    before = millis()
    lena_dic = shannon_fano(hist)
    temp1 = millis()

    print "lena code (shannon fano):"
    print lena_dic
    print str(temp1 - before) + " milliseconds"
    print

    lena_comp = compress(lena_data, lena_dic)
    write(lena_comp, 'lena.txt')
    temp2 = millis()

    print "lena comp (compress):"
    print lena_comp
    print len(lena_comp)
    print str(temp2 - temp1) + " milliseconds"
    print

    lena_comp2 = read('lena.txt')
    print lena_comp2[:7]
    print len(lena_comp2)

    for i in range(len(lena_comp2)):
        if lena_comp[i] != lena_comp2[i]:
            print lena_comp[i]
            print lena_comp2[i]

    dic_inv = {v: k for k, v in lena_dic.items()}
    decompress(lena_comp2, dic_inv)