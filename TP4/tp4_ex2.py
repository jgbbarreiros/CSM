from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from os import path
from time import time


def getImages():
    return [Image.open("bola_seq/bola_"+str(i+1)+".tiff") for i in range(11)]

def compImages(imgs):
    imgs_arr = [np.array(img).astype('float') for img in imgs]
    imgs[0].save("ex2/comp/bola_1.jpeg", "JPEG", quality=50)
    I1 = np.array(Image.open("ex2/comp/bola_1.jpeg")).astype('float')
    P_arr = imgs_arr[1:]
    return [Image.fromarray((P-I1+127.).astype('uint8')) for P in P_arr]

def saveCompImages(imgs):
    [img.save("ex2/comp/bola_"+str(imgs.index(img)+2)+".jpeg", "JPEG", quality=50) for img in imgs]

def getCompImages():
    return [Image.open("ex2/comp/bola_"+str(i+1)+".jpeg") for i in range(11)]

def decompImages(comp_imgs):
    imgs_arr = [np.array(comp_img).astype('float') for comp_img in comp_imgs]
    I1 = imgs_arr[0]
    P_arr = imgs_arr[1:]
    return [Image.fromarray(I1.astype('uint8'))] + [Image.fromarray((P+I1-127.).astype('uint8')) for P in P_arr]

def saveDecompImages(comp_imgs):
    [comp_img.save("ex2/final/bola_"+str(comp_imgs.index(comp_img)+1)+".bmp", "bmp") for comp_img in comp_imgs]

def showImages(comp_imgs):
    for i in range(len(comp_imgs)):
        plt.figure("Image "+str(i+1))
        plt.imshow((comp_imgs[i]), cmap='gray', interpolation='none')

def compRate():
    size_init = sum(path.getsize("bola_seq/bola_"+str(i+1)+".tiff") for i in range(11))
    size_comp = sum(path.getsize("ex2/comp/bola_"+str(i+1)+".jpeg") for i in range(11))
    return float(size_init)/size_comp

def calcSnr(original_imgs, decomp_imgs):
    snrs = []
    for i in range(11):
        original = np.asarray(original_imgs[i]).reshape(-1).astype('float')
        quantificado = np.asarray(decomp_imgs[i]).reshape(-1).astype('float')
        erro = quantificado - original
        snrs.append(10.*np.log10(sum(original**2)/sum(erro**2)))
    return snrs

def calcEnergy(decomp_imgs):
    return [np.sum(np.asarray(decomp_imgs[i]).astype('float')**2)/np.sum(np.asarray(decomp_imgs[i]).astype('float'))**2 for i in range(11)]

def calcEntropy(decomp_imgs):
    entropys = []
    for i in range(11):
        h = np.asarray(decomp_imgs[i].histogram())
        prob = (h*1.)/np.sum(h)
        entropy = - np.sum([ 0 if i == 0 else i*np.log2(i) for i in prob])
        entropys.append(entropy)
    return entropys


if __name__ == "__main__":

    imgs = getImages()

    t0 = time()
    comp_imgs = compImages(imgs)
    t1 = time()

    saveCompImages(comp_imgs)

    comp_imgs1 = getCompImages()

    t2 = time()
    decomp_imgs = decompImages(comp_imgs1)
    t3 = time()

    saveDecompImages(decomp_imgs)

    showImages(decomp_imgs)

    print "Compression rate: %s" % compRate()
    print "Compression time: %s" % (t1-t0)
    print "Decompression time: %s" % (t3-t2)
    print "Signal noise ratio: %s" % calcSnr(imgs, decomp_imgs)
    print "Energy: %s" % calcEnergy(decomp_imgs)
    print "Entropy: %s" % calcEntropy(decomp_imgs)

    plt.show()