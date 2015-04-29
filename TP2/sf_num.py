import numpy as np


def code_tree(prob, prof=0):
    l = 0
    r = 0
    for i in range(len(prob)):
        l = prob[:i + 1]
        r = prob[i + 1:]
        if sum(l) >= sum(r):
            break
    if len(l) == 1:
        fl = np.zeros(prof + 1)
    else:
        fl = code_tree(l, prof + 1)
        for i in range(len(fl)):
            fl[i][prof] = 0

    if len(r) == 1:
        fr = np.ones(prof + 1)
    else:
        fr = code_tree(r, prof+1)
        for i in range(len(fr)):
            fr[i][prof] = 1

    return np.array([fl, fr])

if __name__ == "__main__":

    p = [.10, .20, .30, .10, .30]
    s = sorted(p, reverse=True)
    # [[0,0], [0,1], [1,0], [1,1,0], [1,1,1]]
    # [[0]]
    # [[1]]
    # [[0], [1]]
    # [[0,0], [0,1]]
    print code_tree(s)