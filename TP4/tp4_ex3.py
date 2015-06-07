from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def getImages():
    return [Image.open("bola_seq/bola_"+str(i+1)+".tiff") for i in range(11)]

def compImages(imgs):
    imgs_arr = [np.array(img).astype('float') for img in imgs]
    imgs[0].save("ex3/comp/bola_1.jpeg", "JPEG", quality=50)
    I1 = np.array(Image.open("ex3/comp/bola_1.jpeg")).astype('float')
    I1_exp = expand(I1, 15)
    P_arr = imgs_arr[1:]
    P_coded_arr = []
    P_vecs_arr = []
    for P in P_arr:
        Pmc, P_vecs = search(I1_exp, P, search_type='fs')
        P_coded = P-Pmc+127
        P_coded_arr.append(Image.fromarray((P_coded).astype('uint8')))
        P_vecs_arr.append(P_vecs)
    return [P_coded_arr, P_vecs_arr]

def saveCompImages(imgs):
    [img.save("ex3/comp/bola_"+str(imgs.index(img)+2)+".jpeg", "JPEG", quality=50) for img in imgs]

def getCompImages():
    return [Image.open("ex3/comp/bola_"+str(i+1)+".jpeg") for i in range(11)]

def decompImages(comp_imgs, vecs):
    imgs_arr = [np.array(comp_img).astype('float') for comp_img in comp_imgs]
    I1 = imgs_arr[0]
    I1_exp = expand(I1, 15)
    P_arr = imgs_arr[1:]
    P_decoded_arr = []
    c = 0
    for P in P_arr:
        Pmc = compose(I1_exp, vecs[c])
        P1 = P + Pmc - 127
        P_decoded_arr.append(Image.fromarray(P1.astype('uint8')))
        c += 1
    return [Image.fromarray(I1.astype('uint8'))] + P_decoded_arr

def saveDecompImages(comp_imgs):
    [comp_img.save("ex3/final/bola_"+str(comp_imgs.index(comp_img)+1)+".bmp", "bmp") for comp_img in comp_imgs]

def showImages(comp_imgs):
    for i in range(len(comp_imgs)):
        plt.figure("Image "+str(i+2))
        plt.imshow((comp_imgs[i]), cmap='gray', interpolation='none')
    plt.show()

def expand(arr, px):
    h = arr.shape[0] # 240
    w = arr.shape[1] # 352
    ex_arr = np.zeros((h+2*px, w+2*px))
    ex_arr[px:h+px, px:w+px] = arr # inserir imagem i no meio
    ex_arr[:px, px:px+w] = arr[0] # linas topo
    ex_arr[px+h:, px:px+w] = arr[-1] # linhas de baixo
    ex_arr[px:px+h,:px ] = arr.T[0][:,None] # linhas esquerda
    ex_arr[px:px+h, px+w:] = arr.T[-1][:,None] # linhas direita
    ex_arr[:px, :px] = np.ones((px, px))*arr[0, 0] # top left corner
    ex_arr[:px, px+w:] = np.ones((px, px))*arr[0, -1] # top right corner
    ex_arr[px+h:, :px] = np.ones((px, px))*arr[-1, 0] # bottom left corner
    ex_arr[px+h:, px+w:] = np.ones((px, px))*arr[-1, -1] # bottom right corner
    return ex_arr

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

def blockShaped(arr, nrows, ncols):
    h, w = arr.shape
    return arr.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1, nrows, ncols)

def macroSearch(I_block, P_block):
    # pequisa de Blocos P em macro Bloco I e encontar a menor "mae"
    h, w = I_block.shape
    diff, vec, block = min([mae(P_block, I_block[y:y+16, x:x+16]), (y,x), I_block[y:y+16, x:x+16]] for y in range(h-16) for x in range(w-16))
    return [block, vec]

def mae(P, I):
    return np.sum(np.abs(P-I))

def unblockShaped(arr, h, w):
    n, nrows, ncols = arr.shape
    return arr.reshape(h//nrows, -1, nrows, ncols).swapaxes(1,2).reshape(h, w)

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

    imgs = getImages()

    comp_imgs, vecs = compImages(imgs)

    saveCompImages(comp_imgs)

    comp_imgs1 = getCompImages()

    decomp_imgs = decompImages(comp_imgs1, vecs)

    saveDecompImages(decomp_imgs)

    showImages(decomp_imgs)