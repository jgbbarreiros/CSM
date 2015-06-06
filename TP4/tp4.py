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
    h = arr.shape[0] # 240
    w = arr.shape[1] # 352
    ex_arr = np.zeros((h+2*px, w+2*px))
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


def getPImages(num_imagens):
    # Vai buscar todas as images e devolve um array
    P_arr = []
    for i in range(num_imagens):
        P = np.array(Image.open("bola_seq/bola_" + str(i + 2) + ".tiff")).astype('float')
        P_arr.append(P)
    return P_arr


def search(I, P, search_type='fs'):
    I_blocks = IToBlocks(I) # return blocos de 46x46 (janela de pesquisa)
    P_blocks = blockShaped(P, 16, 16) # return blocos de 16x16
    Pmc_blocks = [] # array de blocos P codificados
    P_vecs = [] # array de pares de vectores
    for i in range(len(I_blocks)):
        Pmc_block, P_vec = macroSearch(I_blocks[i], P_blocks[i])
        Pmc_blocks.append(Pmc_block)
        P_vecs.append(P_vec)
    Pmc = unblockShaped(np.asarray(Pmc_blocks), P.shape[0], P.shape[1])
    return [Pmc, P_vecs]


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
    diff, vec, block = min([mae(P_block, I_block[y:y+16, x:x+16]), (y,x), I_block[y:y+16, x:x+16]] for y in range(h-16) for x in range(w-16))
    return [block, vec]

def getCodedImages(num_imagens):
    # Vai buscar todas as images e devolve um array
    img_arr = []
    for i in range(num_imagens):
        img = np.array(Image.open("ex3/bola_" + str(i + 2) + ".jpeg")).astype('float')
        img_arr.append(img)
    return img_arr

def compose(I, P_vecs):
    I_blocks = IToBlocks(I) # return blocos de 46x46 (janela de pesquisa)
    Pmc_blocks = []
    for i in range(len(I_blocks)):
        Pmc_block = getBlock(I_blocks[i], P_vecs[i])
        Pmc_blocks.append(Pmc_block)
    Pmc = unblockShaped(np.asarray(Pmc_blocks), I.shape[0]-30, I.shape[1]-30)
    return Pmc

def getBlock(block, vec):
    return block[vec[0]:vec[0]+16, vec[1]:vec[1]+16]



if __name__ == "__main__":



    ## IMAGEM 1
    # img1 = Image.open("bola_seq/bola_1.tiff")
    # img1.save("bola_1.jpeg", "JPEG", quality=50)
    # I = np.array(img1).astype('float')
    # ler ja em array
    # arr = mi.imread("bola_1.jpeg").astype('float')
    # h = I.shape[0] # 240
    # w = I.shape[1] # 352
    # I_exp = expand(I, 15, corner='pixel')
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

    ## EX3 - MOVIMENTO
    print "image 1...",
    # Ler Imagem I
    img1 = Image.open("bola_seq/bola_1.tiff")
    # Guardar a Imagem I codificada
    img1.save("ex3/bola_1.jpeg", "JPEG", quality=50)
    # Le Imagem I codificada
    I_arr = mi.imread("ex3/bola_1.jpeg").astype('float')
    print "done"
    # Imagem I como array
    I = np.array(I_arr).astype('float')
    # Imagem I expandida para pequisa mais facil
    I_exp = expand(I, 15, corner='pixel')
    # Arrays das imagens P's e respetivos
    # P_coded_arr = []
    # Array de vectores de compensacao de movimento
    P_vecs_arr = []
    # Array das imagens P
    P_arr = getPImages(10)
    # Percorre todas as imagens P's
    img_counter = 0
    for P in P_arr:
        print "image %s..." % (img_counter+2),
        Pmc, P_vecs = search(I_exp, P, search_type='fs')
        P_coded = P - Pmc + 127
        P_vecs_arr.append(P_vecs)
        Image.fromarray(P_coded.astype('uint8')).save("ex3/bola_" + str(img_counter + 2) + ".jpeg", "JPEG", quality=50)
        img_counter += 1
        print "done"

    P_coded_arr = getCodedImages(10)
    plt.imshow((I), cmap='gray', interpolation='none')
    img2 = Image.fromarray(I.astype('uint8'))
    img2.save("bola_1.bmp", "bmp")
    img_counter = 0
    for P_coded in P_coded_arr:
        Pmc = compose(I_exp, P_vecs_arr[img_counter])
        P1 = P_coded + Pmc - 127
        plt.figure("Image " + str(img_counter+2))
        plt.imshow((P1), cmap='gray', interpolation='none')
        img2 = Image.fromarray(P1.astype('uint8'))
        img2.save("bola_" + str(img_counter+2) + ".bmp", "bmp")
        img_counter += 1

    # for i in range(len(P_coded_arr)):
    #     plt.figure("Image " + str(i+2))
    #     plt.imshow((P_coded_arr[i]), cmap='gray', interpolation='none')

    plt.show()