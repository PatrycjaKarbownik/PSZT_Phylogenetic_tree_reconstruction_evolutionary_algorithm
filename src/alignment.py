from parallel import simple_parallel, parallel, pairwise_alignment
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


def _reference_sequence_index(similarity_matrix, leaves):
    max = -1
    index = -1
    for column in range(len(leaves)):
        sum = 0
        for row in range(len(leaves)):
            sum += similarity_matrix[column, row]
        if sum > max:
            max = sum
            index = column
    return index


def multiple_alignment(similarity_matrix, leaves):
    # TODO: FIX IT IMMEDIATELY
    reference_sequence_index = _reference_sequence_index(similarity_matrix, leaves)

    # pairwise alignment
    aligned_sequences = []
    for leaf in leaves:
        aligned_sequences.append(pairwise_alignment(leaves[reference_sequence_index].sequence, leaf.sequence))

    print(aligned_sequences)

    multiple_aligned_sequences = [aligned_sequences[0][0], aligned_sequences[0][1]]

    for pair in range(1, len(aligned_sequences)):
        if len(aligned_sequences[pair][0]) > len(multiple_aligned_sequences[0]):
            shorter = len(multiple_aligned_sequences[0])
        else:
            shorter = len(aligned_sequences[pair][0])

        for column in range(shorter):
            if multiple_aligned_sequences[0][column] == '-' and aligned_sequences[pair][0][column] != '-':
                aligned_sequences[pair][1] = aligned_sequences[pair][1][:column] + '-' \
                                             + aligned_sequences[pair][1][column:]
                aligned_sequences[pair][0] = aligned_sequences[pair][0][:column] + '-' \
                                             + aligned_sequences[pair][0][column:]
                column -= 1

            elif aligned_sequences[pair][0][column] == '-' and multiple_aligned_sequences[0][column] != '-':
                for sequence in range(len(multiple_aligned_sequences)):
                    multiple_aligned_sequences[sequence] = str(multiple_aligned_sequences[sequence][:column]) + '-' \
                                                           + str(multiple_aligned_sequences[sequence][column:])

        if len(aligned_sequences[pair][0]) > len(multiple_aligned_sequences[0]):
            temp = len(aligned_sequences[pair][0]) - len(multiple_aligned_sequences[0])
            for sequence in range(len(multiple_aligned_sequences)):
                for i in range(temp):
                    multiple_aligned_sequences[sequence] += '-'

        if len(aligned_sequences[pair][0]) < len(multiple_aligned_sequences[0]):
            for i in range(len(multiple_aligned_sequences[0]) - len(aligned_sequences[pair][0])):
                aligned_sequences[pair][1] += '-'
        multiple_aligned_sequences.append(aligned_sequences[pair][1])

    print(multiple_aligned_sequences)


if __name__ == "__main__":
    sequences1 = ["ATTGCCATT", "ATGGCCATT", "ATCTTCTT", "ATCCAATTTT", "ACTGACC"]
    sequences2 = ["ACT", "TCT", "CT", "ATCT", "ACT"]

    #print(multiple_alignment(similarity_matrix, leaves))
