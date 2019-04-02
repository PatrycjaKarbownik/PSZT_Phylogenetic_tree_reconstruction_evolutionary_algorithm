from parallel import parallel
from symmetric_matrix import SymmetricMatrix


def calculate_similarities(leaves):
    matrix = SymmetricMatrix(len(leaves))
    for row in range(len(matrix)):
        for column in range(row + 1):
            if row == column: continue
            matrix[row, column] = parallel(leaves[row].sequence, leaves[column].sequence)
    return matrix


def create_tree(leaves):
    similarity_matrix = calculate_similarities(leaves)
    print(similarity_matrix)
