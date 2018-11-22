import numpy as np

import warnings

warnings.filterwarnings("ignore")


def get_minimum_except_zero(matrix):
    idr_min = 0
    idr_min_tmp = 0
    min_val = MAX

    for i in matrix:
        if min_val > i > 0:
            min_val = i
            idr_min = idr_min_tmp
        idr_min_tmp += 1

    return idr_min


MAX = 10**9 

A = np.matrix([
    [-1, 3, 0, 2, 1],
    [2, -1, 1, 2, 3],
    [1, -1, 2, 1, 0]

])

B = np.matrix([
    [1],
    [2],
    [4]
])

C = np.matrix([1, -3, 2, 1, 4])

b_size = B.size
c_size = C.size

work = np.concatenate((A, np.eye(b_size), B), axis=1)
work = np.concatenate((work, np.concatenate((C, np.zeros((1, b_size + 1))), axis=1)), axis=0)

res = []
work[b_size] *= -1


while True:
    idc_min = work[b_size, 0:c_size].argmin()

    if work[b_size, idc_min] >= 0:
        break

    tmp1 = work[0:b_size, idc_min]
    tmp2 = work[0:b_size, c_size + b_size] / tmp1

    idr_min = get_minimum_except_zero(tmp2)

    work[idr_min] = work[idr_min] / work[idr_min, idc_min]

    for i in range(0, b_size + 1):
        if i == idr_min: continue

        work[i] = work[i] - work[idr_min] * (work[i, idc_min] / work[idr_min, idc_min])

    res += [idc_min]

result = [work[work[:, i].argmax(), b_size + c_size] if i in res else 0
          for i in range(0, c_size)]

print(result)