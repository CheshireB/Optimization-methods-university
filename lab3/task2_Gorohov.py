import numpy as np
from queue import Queue
import random


def find(i, j):
    path = [[i, j]]
    find_v(path, i, j, i, j)
    return path


def find_h(path, i, j, i0, j0):
    for maybe in range(b_size):
        if (maybe != j and X[i, maybe] != 0):
            if find_v(path, i, maybe, i0, j0):
                path += [[i, maybe]]
                return True
    return False


def find_v(path, i, j, i0, j0):
    for maybe in range(a_size):
        if (maybe != i and X[maybe, j] != 0):
            if (maybe == i0):
                path += [[maybe, j]]
                return True
            if find_h(path, maybe, j, i0, j0):
                path += [[maybe, j]]
                return True
    return False


random.seed()

A = [40, 30, 30]
B = [30, 70]
C = np.matrix([[1, 2],
               [3, 2],
               [1, 4]])

# A = [30, 40, 20]
# B = [20, 30, 30, 10]
# C = np.matrix([[2, 3, 2, 4],
#                [3, 2, 5, 1],
#                [4, 3, 2, 6]])

# A = [30, 50, 75, 20]
# B = [20, 40, 30, 10, 50, 25]
# C = np.matrix([[1, 2, 1, 4, 5, 2],
#                [3, 3, 2, 1, 4, 3],
#                [4, 2, 5, 9, 6, 2],
#                [3, 1, 7, 3, 4, 6]])

a_size = len(A)
b_size = len(B)
a_sum = sum(A)
b_sum = sum(B)
    
if (a_sum > b_sum):
    B += [a_sum - b_sum]
    b_size += 1
    C = np.concatenate((C, np.matrix(np.zeros((b_size, 1)))), axis=1)
elif (a_sum < b_sum):
    A += [b_sum - a_sum]
    a_size += 1
    C = np.concatenate((C, np.matrix(np.zeros((1, b_size)))), axis=0)
del a_sum
del b_sum
X = np.matrix(np.zeros((a_size, b_size)))
ac = 0
bc = 0

result = [[ac, bc]]
while (True):
    xmin = min(A[ac], B[bc])
    X[ac, bc] = xmin
    A[ac] -= xmin
    B[bc] -= xmin
    if (A[ac] < B[bc]):
        ac += 1
    elif (A[ac] > B[bc]):
        bc += 1
    elif (ac == a_size - 1 and bc == b_size - 1):
        break
    else:
        X[ac + 1, bc] = 0.000000001
        result += [[ac + 1, bc]]
        ac += 1
        bc += 1
    result += [[ac, bc]]

while (True):
    while (len(result) < a_size + b_size - 1):
        ir = random.randint(0, a_size - 1)
        jr = random.randint(0, b_size - 1)
        if (X[ir, jr] == 0):
            result += [[ir, jr]]
            X[ir, jr] = 0.000000001
    U = [None] * a_size
    V = [None] * b_size
    U[result[0][0]] = 0
    ac = 0
    bc = 0
    V[result[0][1]] = C[result[0][0], result[0][1]] - U[result[0][0]]
    q = Queue()
    q.put([0, result[0][0]])
    q.put([1, result[0][1]])
    check = 1
    while (check != a_size + b_size - 1 and not q.empty()):
        axis = q.get()
        uv = axis[1]
        axis = axis[0]
        if (axis == 0):
            for index, i in enumerate(V):
                if (i == None and X[uv, index] != 0):
                    V[index] = C[uv, index] - U[uv]
                    check += 1
                    q.put([1, index])
        else:
            for index, j in enumerate(U):
                if (j == None and X[index, uv] != 0):
                    U[index] = C[index, uv] - V[uv]
                    check += 1
                    q.put([0, index])

    del q
    dmin = 0
    ijmin = [-1, -1]
    for i in range(a_size):
        for j in range(b_size):
            d = C[i, j] - U[i] - V[j]
            if (d < dmin):
                dmin = d
                ijmin = [i, j]

    if (dmin == 0):
        break

    path = find(*ijmin)
    cmin = 10000000
    result += [ijmin]
    counter = 0
    for i in path:
        if (counter == 0):
            counter = 1
        else:
            counter = 0
            if (X[i[0], i[1]] < cmin):
                cmin = X[i[0], i[1]]
                ijmin = [i[0], i[1]]
    for i in path:
        if (counter == 0):
            counter = 1
            X[i[0], i[1]] += cmin
        else:
            counter = 0
            X[i[0], i[1]] -= cmin
            if (X[i[0], i[1]] == 0):
                result.remove([i[0], i[1]])

sum = 0
for i in range(a_size):
    for j in range(b_size):
        X[i, j] = round(X[i, j], 6)
        sum += X[i, j] * C[i, j]
print(X)
print(sum)
print(path)
print(ijmin)