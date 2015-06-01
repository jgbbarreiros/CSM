import numpy as np

# np.set_printoptions(linewidth=200)

I = np.reshape(np.arange(270*382), (270, 382))
print I

h = 240
w = 352


block_size = 16
vb = h/block_size
hb = w/block_size

print I.shape[0]-30
print I.shape[1]-30

macroBlocks = []




def IToBlocks(I):
    # blocos de 46x46 (janela de pesquisa)
    aux = []
    #y
    for j in range(15):
        for i in range(22):
            aux.append(I[j*15:46+(j*15)][i*15:46+(i*15)])
    return aux