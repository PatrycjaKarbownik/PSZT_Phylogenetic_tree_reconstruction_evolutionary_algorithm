from symmetric_matrix import SymmetricMatrix


# Temporary function waiting for further implementation
def parallel(sequence1, sequence2):
    pass


def calculate_similarities(sequences):
    matrix = SymmetricMatrix(len(sequences))
    for row in range(len(matrix)):
        for column in range(row + 1):
            if row == column: continue
            matrix[row, column] = parallel(sequences[row], sequences[column])
    return matrix


example_sequences = ["ATATG", "TCATG", "CAGTC", "ACCAT"]
example_matrix = calculate_similarities(example_sequences)
