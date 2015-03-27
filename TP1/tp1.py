from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# ex 1

# remove comment plt.figure("ex 1")
x_img = Image.open("lenac.tif")
# remove comment plt.imshow(x_img, interpolation='nearest')
print x_img.format
print x_img.mode
print x_img.size

# ex 2

# remove comment x_img.save("file1.jpg", "JPEG", quality=80)
# remove comment x_img.save("file2.jpg", "JPEG", quality=10)

# ex 3

# remove comment plt.figure("ex 3")
x_gray = x_img.convert("L")
# remove comment plt.imshow(x_gray, interpolation='nearest', cmap='gray')
# remove comment x_gray.save("file2.bmp", "bmp")

# ex 4

# remove comment plt.figure("ex 4")
hist = x_img.histogram()
# remove comment plt.plot(hist)

# ex 5

# remove comment plt.figure("ex 5")
x = np.array(x_gray)

for i in range(8):
    y = (x >= 2**i) & (x < 2**(i+1))
    # remove comment plt.subplot(3,3,8-i)
    # remove comment plt.imshow(y, cmap='gray')


# ex 6

# remove comment plt.figure("ex 6")
y = x >= 2**5
# remove comment plt.imshow(y, cmap='gray')
# remove comment new_img = Image.fromarray(y.astype('uint8')*255 ,'L')
# remove comment new_img.save("lena_4.bmp")


# ex 7

plt.figure("ex 7")


w = 400
h = 400

star_burst = np.ones((h, w))*255
angle = 16

rad = angle * np.pi / 180.

for y in range(h):
    for x in range(w):
        vx = x - float(w/2)
        vy = float(h/2) - y

        if vx == 0:
            a = .1
        else:
            a = np.arctan(vy/vx)
        # 1 quadrante
        if (vx > 0) & (vy > 0):
            pass

        # 2 quadrante
        if (vx < 0) & (vy > 0):
            a += np.pi

        # 3 quadrante
        if (vx < 0) & (vy < 0):
            a += np.pi

        # 4 quadrante
        if (vx > 0) & (vy < 0):
            a += 2*np.pi

        for i in range(180/angle + 1):
            if (rad*i*2 <= a < rad*(i*2+1)):
                star_burst[y][x] = 0

plt.imshow(star_burst, cmap='gray')

plt.show()