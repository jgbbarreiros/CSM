import numpy as np
a = ["0","1"]
b = np.array(["0"], dtype='|S500')
c = np.array(["1"])
print type(c)

d = np.hstack((b,c))
print type(d)
print d
for i in range(len(d)):
    d[i] = "1" + d[i]

print d.shape
print type(d[0])

# ["10","11"]