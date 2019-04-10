import numpy as np

from parallel import parallel, _match_score, gap_penalty
from symmetric_matrix import SymmetricMatrix


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
    # look for sequence with maximal sum of similarity
    for column in range(len(leaves)):
        sum = 0
        for row in range(len(leaves)):
            sum += similarity_matrix[column, row]
        if sum > max:
            max = sum
            index = column
    return index


# Needleman-Wunsch algorithm with n x m score matrix
def _simple_needleman_wunsch_score(seq1, seq2):
    length_of_seq1, length_of_seq2 = len(seq1), len(seq2)
    result = np.empty([length_of_seq1 + 1, length_of_seq2 + 1], int)  # prepare matrix for scoring the alignment

    # complete row and column with gap penalty - it will ease later computations
    for i in range(length_of_seq1 + 1):
        result[i][0] = i * gap_penalty
    for j in range(length_of_seq2 + 1):
        result[0][j] = j * gap_penalty

    # complete other cell in matrix - write the best score in cell (dynamic programming)
    for j in range(1, length_of_seq2 + 1):
        for i in range(1, length_of_seq1 + 1):
            gap1 = result[i][j-1] + gap_penalty
            gap2 = result[i-1][j] + gap_penalty
            align = result[i-1][j-1] + _match_score(seq1[i-1], seq2[j-1])
            result[i][j] = max(gap1, gap2, align)

    return result


# return from bottom right cell to the top left to produce aligned sequences
def _get_aligned_sequences(score, seq1, seq2):
    length_of_seq1, length_of_seq2 = len(seq1), len(seq2)
    j = length_of_seq2
    i = length_of_seq1
    seq1_aligned = ''
    seq2_aligned = ''
    while i > 0 or j > 0:
        # check if algorithm goes from up, aside or from diagonal
        if score[i][j] == score[i - 1][j - 1] + _match_score(seq1[i - 1], seq2[j - 1]):
            seq1_aligned += seq1[i - 1]
            seq2_aligned += seq2[j - 1]
            i -= 1
            j -= 1
        elif score[i][j] == score[i - 1][j] + gap_penalty:
            seq1_aligned += seq1[i - 1]
            seq2_aligned += '-'
            i -= 1
        else:
            seq1_aligned += '-'
            seq2_aligned += seq2[j - 1]
            j -= 1

    # reverse alignment to be able to read from the first nucleotide
    seq1_aligned = seq1_aligned[::-1]
    seq2_aligned = seq2_aligned[::-1]
    return [seq1_aligned, seq2_aligned]


def pairwise_alignment(seq1, seq2):
    score = _simple_needleman_wunsch_score(seq1, seq2)
    return _get_aligned_sequences(score, seq1, seq2)


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

    seq3 = "ACTGGTCAT"
    seq4 = "ACGGATCGTATC"

    print(pairwise_alignment(seq3, seq4))
    #print(multiple_alignment(similarity_matrix, leaves))
