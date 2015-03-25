from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

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

# plt.figure("ex 7")
# lsd_w = 100
# lsd_h = 100

# lsd = np.zeros((lsd_h, lsd_w))
# cursor = [lsd_h/2, lsd_w/2]

# r1 = np.zeros((lsd_w/2, 2))
# r2 = np.zeros((lsd_w/2, 2))

# for i in range(lsd_w/2):
#     r1[i] = [i + lsd_w/2, lsd_h/2]
#     r2[i] = [i + lsd_w/2, i*np.tan(2*np.pi/18.)]

# print r1
# print r2

# for x in range(lsd_w):
#     for y in range(lsd_h):
#         if (x > r2[x][0])
#         if (x > r2[y][0]+lsd_w/2 & y > r2[y][])
#             if (x > r2[x-lsd_w/2])

plt.figure("ex 7")

w = 100
h = 100

star_burst = np.ones((h, w))*255

c = [w/2, h/2]

for x in range(w):
    for y in range(h):
        v = [x - c[0], c[1] - y]
        try:
            a = np.arctan(float(v[0])/v[1])
        except Exception, e:
            a = 0
        for i in range(5):
            if (i%2 == 0):
                if ( (a >= (2*np.pi/18.*i)) & (a < (2*np.pi/18.*(i+1)) ) ):
                    star_burst[x, y] = 0

plt.imshow(star_burst, cmap='gray')

plt.show()