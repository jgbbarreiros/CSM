from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from os import path
from time import time


def getImages():
    return [Image.open("bola_seq/bola_"+str(i+1)+".tiff") for i in range(11)]

def saveCompImages(imgs):
    [img.save("ex1/comp/bola_"+str(imgs.index(img)+1)+".jpeg", "JPEG", quality=50) for img in imgs]

def getCompImages():
    return [Image.open("ex1/comp/bola_"+str(i+1)+".jpeg") for i in range(11)]

def saveDecompImages(comp_imgs):
    [comp_img.save("ex1/final/bola_"+str(comp_imgs.index(comp_img)+1)+".bmp", "bmp") for comp_img in comp_imgs]

def showImages(comp_imgs):
    for i in range(len(comp_imgs)):
        plt.figure("Image "+str(i+1))
        plt.imshow((comp_imgs[i]), cmap='gray', interpolation='none')

def compRate():
    size_init = sum(path.getsize("bola_seq/bola_"+str(i+1)+".tiff") for i in range(11))
    size_comp = sum(path.getsize("ex1/comp/bola_"+str(i+1)+".jpeg") for i in range(11))
    return float(size_init)/size_comp

def snr(originals, finals):
    snrs = []
    for i in range(11):
        original = np.asarray(originals[i]).reshape(-1).astype('float')
        quantificado = np.asarray(finals[i]).reshape(-1).astype('float')
        erro = quantificado - original
        snrs.append(10.*np.log10(sum(original**2)/sum(erro**2)))
    return snrs

if __name__ == "__main__":

    imgs = getImages()

    t0 = time()
    saveCompImages(imgs)
    t1 = time()

    t2 = time()
    decomp_imgs = getCompImages()
    t3 = time()

    saveDecompImages(decomp_imgs)

    showImages(decomp_imgs)

    print "Compression rate: %s" % compRate()
    print "Compression time: %s" % (t1-t0)
    print "Decompression time: %s" % (t3-t2)
    print "Signal noise ratio: %s" % snr(imgs, decomp_imgs)

    plt.show()