from parallel import simple_parallel, parallel#, recursive_needleman_wunsch
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
            # matrix[row, column] = recursive_needleman_wunsch(leaves[row].sequence, leaves[column].sequence,
            #                                                 0, len(leaves[column].sequence), 0)
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
    reference_sequence_index = _reference_sequence_index(similarity_matrix, leaves)
    # pairwise alignment
    aligned_sequences = [["ATTGCCATT", "ATGGCCATT"], ["ATTGCCATT", "ATCTTC-TT"], ["ATTGCCATT--", "ATC-CAATTTT"],
                          ["ATTGCCATT", "ACTGACC--"]]
    # aligned_sequences = [["ACT", "TCT"], ["ACT", "-CT"], ["A-CT", "ATCT"], ["ACT", "ACT"]]

    multiple_aligned_sequences = [aligned_sequences[0][0], aligned_sequences[0][1]]
    print(aligned_sequences)
    print(multiple_aligned_sequences)

    for pair in range(1, len(aligned_sequences)):
        print("pair = ", pair)

        if len(aligned_sequences[pair][0]) > len(multiple_aligned_sequences[0]):
            shorter = len(multiple_aligned_sequences[0])
            print("shorter if = ", shorter)
        else:
            shorter = len(aligned_sequences[pair][0])
            print("shorter else = ", shorter)

        for column in range(shorter):
            print("column = ", column)
            print("len multiple = ", len(multiple_aligned_sequences[0]))
            print("len aligned = ", len(aligned_sequences[pair][0]))

            if multiple_aligned_sequences[0][column] == '-' and aligned_sequences[pair][0][column] != '-':
                aligned_sequences[pair][1] = aligned_sequences[pair][1][:column] + '-' \
                                             + aligned_sequences[pair][1][column:]
                aligned_sequences[pair][0] = aligned_sequences[pair][0][:column] + '-' \
                                             + aligned_sequences[pair][0][column:]
                column -= 1
                print("aligned sequence AFTER = ", aligned_sequences[pair][1])

            elif aligned_sequences[pair][0][column] == '-' and multiple_aligned_sequences[0][column] != '-':
                print("WELCOME")
                for sequence in range(len(multiple_aligned_sequences)):
                    print("sequence = ", sequence)
                    multiple_aligned_sequences[sequence] = str(multiple_aligned_sequences[sequence][:column]) + '-' \
                                                           + str(multiple_aligned_sequences[sequence][column:])
                    print("multiple_aligned_sequences[sequence] AFTER = ", multiple_aligned_sequences[sequence])

        if len(aligned_sequences[pair][0]) > len(multiple_aligned_sequences[0]):
            temp = len(aligned_sequences[pair][0]) - len(multiple_aligned_sequences[0])
            for sequence in range(len(multiple_aligned_sequences)):
                print("sequence = ", sequence)
                for i in range(temp):
                    multiple_aligned_sequences[sequence] += '-'
                    print("multiple_aligned_sequences[sequence] AFTER2 = ", multiple_aligned_sequences[sequence])

        if len(aligned_sequences[pair][0]) < len(multiple_aligned_sequences[0]):
            for i in range(len(multiple_aligned_sequences[0]) - len(aligned_sequences[pair][0])):
                aligned_sequences[pair][1] += '-'
        multiple_aligned_sequences.append(aligned_sequences[pair][1])
        print(multiple_aligned_sequences)

    print(multiple_aligned_sequences)
