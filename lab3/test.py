import numpy as np



matrix = np.matrix(np.zeros((6, 5)))

for i in matrix.getA():
    print(i)
    for j in i:
        print(j)

print(len(matrix))

print(matrix)