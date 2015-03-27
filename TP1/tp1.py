from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def star_burst(angle):
    plt.figure("ex 7")

    w = 100
    h = 100

    star_burst = np.ones((h, w))*255

    rad = angle * np.pi / 180.

    for y in range(h):
        for x in range(w):
            vx = x - float(w/2)
            vy = float(h/2) - y

            if vx == 0:
                a = np.pi/2.
                if vy < 0:
                    a += np.pi
            else:
                a = np.arctan(vy/vx)

            if vx < 0:
                a += np.pi

            if (vx > 0) & (vy < 0):
                a += 2*np.pi

            for i in range(180/angle + 1):
                if (rad*i*2 <= a <= rad*(i*2+1)):
                    star_burst[y][x] = 0

    plt.imshow(star_burst, cmap='gray')


if __name__ == "__main__":

    # ex 1
    plt.figure("ex 1")
    x_img = Image.open("lenac.tif")
    plt.imshow(x_img, interpolation='nearest')
    print x_img.format
    print x_img.mode
    print x_img.size

    # ex 2
    x_img.save("file1.jpg", "JPEG", quality=80)
    x_img.save("file2.jpg", "JPEG", quality=10)

    # ex 3
    plt.figure("ex 3")
    x_gray = x_img.convert("L")
    plt.imshow(x_gray, interpolation='nearest', cmap='gray')
    x_gray.save("file2.bmp", "bmp")

    # ex 4
    plt.figure("ex 4")
    hist = x_img.histogram()
    plt.plot(hist)

    # ex 5
    plt.figure("ex 5")
    x = np.array(x_gray)

    for i in range(8):
        y = (x >= 2**i) & (x < 2**(i+1))
        plt.subplot(3,3,8-i)
        plt.imshow(y, cmap='gray')

    # ex 6
    plt.figure("ex 6")
    y = x >= 2**5
    plt.imshow(y, cmap='gray')
    new_img = Image.fromarray(y.astype('uint8')*255 ,'L')
    new_img.save("lena_4.bmp")

    # ex 7
    star_burst(20)

    plt.show()

    