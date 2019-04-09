from parallel import *
from symmetric_matrix import SymmetricMatrix


def calculate_similarities_aligned(leaves):
    matrix = SymmetricMatrix(len(leaves))
    for row in range(len(matrix)):
        for column in range(row + 1):
            if row == column: continue
            matrix[row, column] = simple_parallel(leaves[row].sequence, leaves[column].sequence)
    return matrix


def calculate_similarities(leaves):
    matrix = SymmetricMatrix(len(leaves))
    for row in range(len(matrix)):
        for column in range(row + 1):
            if row == column: continue
            matrix[row, column] = parallel(leaves[row].sequence, leaves[column].sequence)
    return matrix
