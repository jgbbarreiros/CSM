def test1(n, l):
    h = len(l)
    w = len(l[0])
    m = 0
    for y in range(h):
        for x in range(w):
            new = formula(n, l[y][x])
            if new < m:
                m = new
    return m

def test2(n, l):
    h = len(l)
    w = len(l[0])
    m = 0
    a = [0,0]
    for y in range(h):
        for x in range(w):
            new = formula(n, l[y][x])
            if new < m:
                m = new
                a = [x,y]
    return a

def test3(n, l):
    # m = min((h,w), key = lambda x, y: formula(n, l[y][x] ))
    m = min([(x,y) for y in range(len(l)) for x in range(len(l[0]))], key = lambda (x, y): formula(n, l[y][x]))
    print m, formula(n, l[m[1]][m[0]])
    return m

def formula(n1, n2):
    return n1-n2

# [[0, 1, 2], [0, -1, -2]]
# [0][0] 1 -   0  =  1
# [0][1] 1 -   1  =  0
# [0][2] 1 -   2  = -1 <--
# [1][0] 1 -   0  =  1
# [1][1] 1 - (-1) =  2
# [1][2] 1 - (-2) =  3
# min = -1
# arg = [2, 0] # x, y

# t1, t2, t3 = None, None, None
# t1 = test1(1, [range(0,3,1), range(0,-3,-1)])
# t2 = test2(1, [range(0,3,1), range(0,-3,-1)])
# t3 = test3(1, [range(0,3,1), range(0,-3,-1)])
# if(t1):
#     print "TEST1\n\tmin = %s" % t1
# if(t2):
#     print "TEST2\n\targ = %s" % t2
# if(t3):
#     print "TEST3\n\tmin = %s" % t3

n = 1
l = [range(0,3,1), range(0,-3,-1)]

valores_formula = [formula(n, l[y][x]) for y in range(len(l)) for x in range(len(l[0]))]
print valores_formula

min_val = min([formula(n, l[y][x]) for y in range(len(l)) for x in range(len(l[0]))])
print min_val

arg_min = min([[(x, y), l] for y in range(len(l)) for x in range(len(l[0]))], key = lambda (y, x): formula(n, l[y][x]))
print arg_min

min_val_arg_min = min([[formula(n, l[y][x]), (y, x), l[y][x]] for y in range(len(l)) for x in range(len(l[0]))])
print min_val_arg_min