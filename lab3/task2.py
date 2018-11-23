import numpy as np
import random


MIN_VALUE = 0.0001
MAX_VALUE = 10000000000


def get_matrix_nw(have_list, need_list):
    matrix = np.matrix(np.zeros((size_a, size_b)))

    for (id_column, need) in enumerate(need_list):
        for (id_row, have) in enumerate(have_list):

            if have < need:
                need_list[id_column] = need - have
                matrix[id_row, id_column] = matrix[id_row, id_column]+have
            else:
                matrix[id_row, id_column] = matrix[id_row, id_column]+need
                have_list[id_row] = have - need
                break

    return matrix


def check_on_degenerate(matrix):
    count_non_zero = 0

    for cell in matrix.getA1():
        if cell: count_non_zero += 1

    return True if size_b+size_a-1 > count_non_zero else False


def get_empty_ids_cell_list(matrix):
    ids_list = []

    for (id_row, row) in enumerate(matrix.getA()):
        for (id_column, cell) in enumerate(row):

            if not cell: ids_list.append([id_row, id_column])

    return ids_list


def get_not_empty_ids_cell_list(matrix):
    ids_list = []

    for (id_row, row) in enumerate(matrix.getA()):
        for (id_column, cell) in enumerate(row):

            if cell: ids_list.append([id_row, id_column])

    return ids_list


def get_matrix_nw_with_additional_cell(matrix):

    ids_list = get_empty_ids_cell_list(matrix)
    id_row, id_column = ids_list[random.randint(0, len(ids_list))-1]

    matrix[id_row, id_column] = MIN_VALUE

    return matrix


def get_potential(C, matrix):
    u = [0] + [None]*(size_a-1)
    v = [None]*size_b

    ids_list_temp = get_not_empty_ids_cell_list(matrix)

    while ids_list_temp:
        ids_list = [ids for ids in ids_list_temp]
        ids_list_temp = []

        for id_row, id_column in ids_list:
            if u[id_row] is not None:
                v[id_column] = C[id_row, id_column]
            elif v[id_column] is not None:
                u[id_row] = C[id_row, id_column] - v[id_column]
            else:
                ids_list_temp.append([id_row, id_column])

    return u, v


def get_matrix_potential_solution(matrix, u, v, c):
    matrix_potential = np.matrix(np.zeros((size_a, size_b)))
    ids_list = get_empty_ids_cell_list(matrix)

    for (id_row, id_column) in ids_list:
        matrix_potential[id_row, id_column] = c[id_row, id_column]-u[id_row]-v[id_column]

    return matrix_potential


def get_ids_min(C):
    min_value = MAX_VALUE
    min_id_row, min_id_cell = None, None

    for (id_row, row) in enumerate(C.getA()):
        for (id_column, cell) in enumerate(row):
            if cell<0 and cell<min_value:
                min_value = cell
                min_id_row, min_id_cell = id_row, id_column

    return [min_id_row, min_id_cell]


def find(i, j):
    path = [[i, j]]

    path = find_vertical(path, i, j, i, j)
    if not path: path = find_vertical(path, i, j, i, j)

    return path


def find_horizontal(path, i, j, i0, j0):

    for id_new_column in [j-1, j+1]:

        if j == i0 and id_new_column == j0:
            path.append([i, id_new_column])
            return path

        if not id_new_column < 0 and size_b > id_new_column \
                and matrix_potential[i, id_new_column] == 0:

            path = find_vertical(path, i, id_new_column, i0, j0)
            if path:
                path.append(j, id_new_column)
                return path

    return None


def find_vertical(path, i, j, i0, j0):

    for id_new_row in [i-1, i+1]:

        if id_new_row == i0 and j == j0:
            path.append([id_new_row, j])
            return path

        if not id_new_row < 0 and size_a > id_new_row \
                and matrix_potential[id_new_row, j] == 0:

            path = find_horizontal(path, id_new_row, j, i0, j0)
            if path:
                path.append(id_new_row, j)
                return path

    return None



A = [40, 30, 30]
B = [30, 70]
C = np.matrix([[1, 2],
               [3, 2],
               [1, 4]])

size_a = len(A)
size_b = len(B)

# get basic solution
matrix = get_matrix_nw(A, B)

# exclude degenerated matrix
while check_on_degenerate(matrix):
    matrix = get_matrix_nw_with_additional_cell(matrix)

# calculate potential
U, V = get_potential(C, matrix)

# calculate potential solution
matrix_potential = get_matrix_potential_solution(matrix, U, V, C)

# get potential minimum
ids_min = get_ids_min(matrix_potential)

# get path of cycle
path = find(*ids_min)

print(path)










