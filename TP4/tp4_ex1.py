from PIL import Image
import matplotlib.pyplot as plt

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
    plt.show()



if __name__ == "__main__":

    imgs = getImages()

    saveCompImages(imgs)

    decomp_imgs = getCompImages()

    saveDecompImages(decomp_imgs)

    showImages(decomp_imgs)