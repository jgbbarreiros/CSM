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
    return np.sum(P-I)

def search(I, P_arr, type='block'):

    if type == 'block':
        block_size = 16
        window_size = block_size + 15*2
        h = I.shape[0]
        w = I.shape[1]
        hb = w/block_size
        vb = h/block_size
        P_coded_arr = []
        P_coded_vec_arr = []
        for P in P_arr:
            P_coded = np.empty((h,w))
            P_coded_vec = []
            P_blocks = np.reshape(blockShaped(P, block_size, block_size), (16,16))
            pos_num = [0, 0]
            min_vec = [-15, -15]
            min_mae = mae(P_blocks[pos[0], pos[1]] , I[pos[0]+x:pos[0]+x+block_size, pos[1]+y:pos[1]+y+block_size])
            min_pos = [0,0]
            for i in range(block_size**2):
                pos = [pos_num[0]*block_size-15, pos_num[1]*block_size-15]
                if (pos_num[0] >= hb-1):
                    pos_num[0] = 1
                    pos_num[1] += 1
                else:
                    pos_num[0] += 1
                for y in range(window_size-16):
                    for x in range(window_size-16):
                        new_mae = mae(P_blocks[pos[0], pos[1]], I[pos[0]+x:pos[0]+x+block_size, pos[1]+y:pos[1]+y+block_size])
                        if new_mae < min_mae:
                            min_mae = new_mae
                            min_vec = [x-15, y-15]
                            min_pos = pos_num
                P_coded[min_pos[0]+15:min_pos[1]+15] = min_mae
                P_coded_vec.append(min_vec)
            P_coded_arr.append(P_coded)
            P_coded_vec_arr.append(P_coded_vec)
        return [P_coded_arr, P_coded_vec_arr]
    else:
        return


if __name__ == "__main__":



    ## IMAGEM 1
    img1 = Image.open("bola_seq/bola_1.tiff")
    img1.save("bola_1.jpeg", "JPEG", quality=50)
    I = np.array(img1).astype('float')
    arr = mi.imread("bola_1.jpeg").astype('float')
    h = I.shape[0] # 240
    w = I.shape[1] # 352
    IS = expand(I, 15, corner='pixel')
    plt.figure("Search image")
    plt.imshow((IS), cmap='gray', interpolation='none')

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
    P = np.array(Image.open("bola_seq/bola_2.tiff")).astype('float')
    P_arr = []
    P_arr.append(P)
    P_coded_arr, P_coded_vec_arr = search(IS, P_arr, type='block')
    print P_coded_arr
    print P_coded_vec_arr


    plt.show()