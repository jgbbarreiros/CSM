from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

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
        plt.figure("Image "+str(i+2))
        plt.imshow((comp_imgs[i]), cmap='gray', interpolation='none')
    plt.show()



if __name__ == "__main__":

    imgs = getImages()

    comp_imgs = compImages(imgs)

    saveCompImages(comp_imgs)

    comp_imgs1 = getCompImages()

    decomp_imgs = decompImages(comp_imgs1)

    saveDecompImages(decomp_imgs)

    showImages(decomp_imgs)