from scipy.fftpack import dct, idct
import scipy.misc as mi
import numpy as np

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



if __name__ == "__main__":
    i = mi.imread('lena.tiff')
    print '---------------original img---------------'
    print i

    #a = i[0:8,0:8]
    #B = to_dct(a)
    #print B
    #C = to_idct(B)
    #print C
    print '---------------img to dct---------------'
    print
    dct = comp_dct(i)
    print dct
    print '---------------dct to img---------------'
    img = decomp_idct(dct)
    print img




