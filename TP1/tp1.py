from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

def star_burst(angle):
    plt.figure("ex 7")

    w = 100
    h = 100

    sb = np.ones((h, w)) * 255

    rad = angle * np.pi / 180.

    for y in range(h):
        for x in range(w):
            vx = x - float(w / 2)
            vy = float(h / 2) - y

            if vx == 0:
                a = np.pi / 2.
                if vy < 0:
                    a += np.pi
            else:
                a = np.arctan(vy / vx)

            if vx < 0:
                a += np.pi

            if (vx > 0) & (vy < 0):
                a += 2 * np.pi

            for i in range(180 / angle + 1):
                if rad * i * 2 <= a <= rad * (i * 2 + 1):
                    sb[y][x] = 0

    plt.imshow(sb, cmap='gray')


if __name__ == "__main__":

    # ex 1
    plt.figure("ex 1")
    x_img = Image.open("lenac.tif")
    plt.imshow(x_img, interpolation='nearest')
    print x_img.format
    print x_img.mode
    print x_img.size
    original_size = os.path.getsize("lenac.tif")

    # ex 2

    x_img.save("file1.jpg", "JPEG", quality=80)
    print int(round(float(original_size) / os.path.getsize("file1.jpg")))
    x_img.save("file2.jpg", "JPEG", quality=10)
    print int(round(float(original_size) / os.path.getsize("file2.jpg")))

    # ex 3
    plt.figure("ex 3")
    x_gray = x_img.convert("L")
    plt.imshow(x_gray, interpolation='nearest', cmap='gray')
    x_gray.save("file2.bmp", "bmp")
    print original_size
    print os.path.getsize("file2.bmp")

    # ex 4
    plt.figure("ex 4")
    hist = x_gray.histogram()
    plt.plot(hist)
    gray_scale_num = 0
    print len(hist)
    for i in range(len(hist)):
        if hist[i] != 0:
            gray_scale_num += 1
    print gray_scale_num

    # ex 5
    plt.figure("ex 5")
    x = np.array(x_gray)

    for i in range(8):
        y = (x >= 2 ** i) & (x < 2 ** (i + 1))
        plt.subplot(3, 3, 8 - i)
        plt.imshow(y, cmap='gray')

    # ex 6
    plt.figure()
    plt.title('Exercicio 6')
    x = np.array(x_gray)
    for k in range(len(x[0])):
        for j in range(len(x[1])):
            x[k][j] = x[k][j] >> 4 << 4

    new_img = Image.fromarray(x.astype('uint8'), 'L')
    new_img.save("lena_4.bmp")
    plt.imshow(x, cmap='gray')

    # ex 7
    star_burst(20)

    plt.show()