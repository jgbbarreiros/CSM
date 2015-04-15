# imports
import numpy as np

# functions


def bin_code_shannon_fano(prob):
    i = np.argsort(prob)[::-1][:len(prob)]
    s = sorted(prob, reverse=True)
    c = code_tree(s)
    f = np.empty((len(c)), dtype='|S' + str(len(c)))

    for x in range(len(c)):
        f[i[x]] = c[x]

    return f


def code_tree(prob):
    l = 0
    r = 0
    for i in range(len(prob)):
        l = prob[:i + 1]
        r = prob[i + 1:]
        if sum(l) >= sum(r):
            break
    if len(l) == 1:
        fl = np.array(['0'], dtype='|S100')
    else:
        fl = code_tree(l)
        for i in range(len(fl)):
            fl[i] = '0' + str(fl[i])

    if len(r) == 1:
        fr = np.array(['1'], dtype='|S100')
    else:
        fr = code_tree(r)
        for i in range(len(fr)):
            fr[i] = '1' + str(fr[i])
    return np.hstack((fl, fr))


# main

if __name__ == "__main__":
    print 'hello'
    # ex 1
    probability = [.10, .20, .30, .10, .30]

    bin_table = bin_code_shannon_fano(probability)
    print bin_table

    # ex 2