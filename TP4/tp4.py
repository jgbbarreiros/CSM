from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from time import time
from os import path
import scipy.misc as mi


def blockShaped(arr, nrows, ncols):
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1, nrows, ncols))


if __name__ == "__main__":

    ## IMAGEM 1
    img1 = Image.open("bola_seq/bola_1.tiff")
    img1.save("bola_1.jpeg", "JPEG", quality=50)
    I = np.array(img1).astype('float')
    I1 = mi.imread("bola_1.jpeg").astype('float')

    ## IMAGEM 2 - SUBTRACAO
    P = np.array(Image.open("bola_seq/bola_2.tiff")).astype('float')
    P -= I1 + 127.
    img2 = Image.fromarray(P.astype('uint8'))
    img2.save("bola_2.jpeg", "JPEG", quality=50)
    P1 = mi.imread("bola_2.jpeg").astype('float')
    P1 += I1 - 127.
    img2 = Image.fromarray(P1.astype('uint8'))
    img2.save("bola_2.bmp", "bmp")

    ## IMAGEM 2 - MOVIMENTO
    BI1 = blockShaped(I1, 16, 16)
    P = np.array(Image.open("bola_seq/bola_2.tiff")).astype('float')
    print P
    PB = np.zeros((270, 382))
    print PB
    PB[16:240+16, 16:352+16] = P
    plt.imshow((PB), cmap='gray', interpolation='none')

    # for bi1 in BI1:
    #     pass

    plt.show()