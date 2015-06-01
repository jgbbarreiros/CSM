from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from time import time
from os import path
import scipy.misc as mi


def blockShaped(arr, nrows, ncols):
    h, w = arr.shape
    return arr.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1, nrows, ncols)

def unblockShaped(arr, h, w):
    n, nrows, ncols = arr.shape
    return arr.reshape(h//nrows, -1, nrows, ncols).swapaxes(1,2).reshape(h, w)


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
    # Vai buscar todas as images e devolve um array
    P_arr = []
    for i in range(10):
        P = np.array(Image.open("bola_seq/bola_" + str(i + 2) + ".tiff")).astype('float')
        P_arr.append(P)
    return P_arr


def search(I, P, type='fs'):
    I_blocks = IToBlocks(I) # return blocos de 46x46 (janela de pesquisa)
    P_blocks = blockShaped(P, 16, 16) # return blocos de 16x16
    Pmc_blocks = [] # array de blocos P codificados
    P_vec = [] # array de pares de vectores
    for i in range(len(I_blocks)):
        Pmc_block, P_block_vec = macroSearch(I_blocks[i], P_blocks[i])
        Pmc_blocks.append(Pmc_block)
        P_vec.append(P_block_vec)
    Pmc = unblockShaped(np.asarray(Pmc_blocks), P.shape[0], P.shape[1])
    return [Pmc, P_vec]


def IToBlocks(I):
    # blocos de 46x46 (janela de pesquisa)
    macroBlocks = []
    for y in range(0, I.shape[0]-30, 16):
        for x in range(0, I.shape[1]-30, 16):
            macroBlocks.append(I[y:y+46, x:x+46])
    return macroBlocks


def macroSearch(I_block, P_block):
    # pequisa de Blocos P em macro Bloco I e encontar a menor "mae"
    h, w = I_block.shape
    min_dif = mae(P_block, I_block[:16, :16])
    min_block = I_block[:16, :16]
    min_vec = [-15, -15]
    for y in range(h-16):
        for x in range(w-16):
            if x == 0 and y == 0:
                pass
            new_block = I_block[y:y+16, x:x+16]
            new_dif = mae(P_block, new_block)
            if new_dif < min_dif:
                min_dif = new_dif
                min_block = new_block
                min_vec = [x-15, y-15]
    return [min_block, min_vec]



if __name__ == "__main__":



    ## IMAGEM 1
    img1 = Image.open("bola_seq/bola_1.tiff")
    img1.save("bola_1.jpeg", "JPEG", quality=50)
    I = np.array(img1).astype('float')
    arr = mi.imread("bola_1.jpeg").astype('float')
    h = I.shape[0] # 240
    w = I.shape[1] # 352
    I_exp = expand(I, 15, corner='pixel')
    # plt.figure("Search image")
    # plt.imshow((I_exp), cmap='gray', interpolation='none')

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
    P_arr = getPImages()
    # P_arr = [I]

    for P in P_arr:
        Pmc, P_vec = search(I_exp, P, type='fs')
        # print I - Pmc
        # print P_vec
        P_coded = P - Pmc + 127
        P_coded_arr.append(P_coded)
        P_vec_arr.append(P_vec)

    print P_coded_arr
    print P_vec_arr

    for i in range(len(P_coded_arr)):
        plt.figure("Image " + str(i+2))
        plt.imshow((P_coded_arr[i]), cmap='gray', interpolation='none')

    plt.show()