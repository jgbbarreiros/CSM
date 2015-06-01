from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from time import time
from os import path
import scipy.misc as mi


def expand(arr, px, corner='pixel'):
    ex_arr = np.zeros((arr.shape[0]+2*px, arr.shape[1]+2*px))
    ex_arr[px:h+px, px:w+px] = arr # inserir imagem i no meio
    ex_arr[:px, px:px+w] = arr[0] # linas topo
    ex_arr[px+h:, px:px+w] = arr[-1] # linhas de baixo
    ex_arr[px:px+h,:px ] = arr.T[0][:,None] # linhas esquerda
    ex_arr[px:px+h, px+w:] = arr.T[-1][:,None] # linhas direita
    if corner == 'pixel':
        ex_arr[:px, :px] = np.ones((px, px))*arr[0, 0] # top left corner
        ex_arr[:px, px+w:] = np.ones((px, px))*arr[0, -1] # top right corner
        ex_arr[px+h:, :px] = np.ones((px, px))*arr[-1, 0] # bottom left corner
        ex_arr[px+h:, px+w:] = np.ones((px, px))*arr[-1, -1] # bottom right corner
    elif corner == 'average':
        ex_arr[:px, :px] = (arr[0, :px][::-1] + arr.T[0, :px][::-1][:,None]) / 2. # top left corner
        ex_arr[:px, px+w:] = (arr[0, -px:][::-1] + arr.T[-1:, :px][:,None]) / 2. # top right corner
        ex_arr[px+h:, :px] = (arr[-1, :px] + arr.T[0, -px:][::-1][:,None]) / 2. # bottom left corner
        ex_arr[px+h:, px+w:] = (arr[-1, -px:][::-1] + arr.T[-1, -px:][::-1][:,None]) / 2. # bottom right corner
    elif corner == 'inverted':
        ex_arr[:px, :px] = np.fliplr(np.fliplr(arr[:px, :px]).T) # top left corner
        ex_arr[:px, px+w:] = arr[:px, -px:].T # top right corner
        ex_arr[px+h:, :px] = arr[-px:, :px].T # bottom left corner
        ex_arr[px+h:, px+w:] = np.fliplr(np.fliplr(arr[-px:, -px:]).T) # bottom right corner
    else:
        # TODO raise exeption 'unknown corner value'
        pass
    return ex_arr


def mae(P, I):
    return np.sum(np.abs(P-I))


def getPImages():
    # TODO vai buscar todas as images e devolve um array
    return []


def search(I, P, type='block'):
    I_blocks = IToBlocks(I) # return blocos de 46x46 (janela de pesquisa)
    P_blocks = PToBlocks(P) # return blocos de 16x16
    P_coded_arr = [] # array de blocos P codificados
    P_vec = [] # array de pares de vectores
    for i in range(len(I_blocks)):
        P_block_coded, P_block_vec = macroSearch(I_blocks[i], P_blocks[i])
        P_coded_arr.append(P_block_coded)
        P_vec.append(P_block_vec)
    P_coded = unblock(P_coded_arr)
    return [P_coded, P_vec]


def IToBlocks(I):
    # TODO blocos de 46x46 (janela de pesquisa)
    return []


def PToBlocks(I):
    # TODO blocos de 16x16
    return []


def macroSearch(I_block, P_block):
    # TODO pequisa de Blocos P em macro Bloco I e encontar a menor "mae"
    return [] # bloco codificado e o respectivo par de vectores

def blockShaped(arr, nrows, ncols):
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1, nrows, ncols))

def unblock(P_coded_arr):
    # TODO compor a imagem codificada a partir de uma lista de Blocos 16x16
    return # bloco codificado


if __name__ == "__main__":



    ## IMAGEM 1
    img1 = Image.open("bola_seq/bola_1.tiff")
    img1.save("bola_1.jpeg", "JPEG", quality=50)
    I = np.array(img1).astype('float')
    arr = mi.imread("bola_1.jpeg").astype('float')
    h = I.shape[0] # 240
    w = I.shape[1] # 352
    I_exp = expand(I, 15, corner='pixel')
    plt.figure("Search image")
    plt.imshow((I_exp), cmap='gray', interpolation='none')

    ## IMAGEM 2 - SUBTRACAO
    # P = np.array(Image.open("bola_seq/bola_2.tiff")).astype('float')
    # P -= I1 + 127.
    # img2 = Image.fromarray(P.astype('uint8'))
    # img2.save("bola_2.jpeg", "JPEG", quality=50)
    # P1 = mi.imread("bola_2.jpeg").astype('float')
    # P1 += I1 - 127.
    # img2 = Image.fromarray(P1.astype('uint8'))
    # img2.save("bola_2.bmp", "bmp")

    ## IMAGEM 2 - MOVIMENTO
    P_coded_arr = []
    P_vec_arr = []

    P = np.array(Image.open("bola_seq/bola_2.tiff")).astype('float')
    P_arr = getPImages()

    for P in P_arr:
        P_coded, P_vec = search(I_exp, P, type='block')
        P_coded_arr.append(P_coded)
        P_vec_arr.append(P_vec)

    plt.show()