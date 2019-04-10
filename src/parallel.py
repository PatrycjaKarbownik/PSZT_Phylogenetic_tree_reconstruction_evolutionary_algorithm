import numpy as np
from substitution_matrix import SubstitutionMatrix

# Nucleotide dictionary

nucl_dict = {
    'A': 0,
    'G': 1,
    'C': 2,
    'T': 3,
    '-': 4
}

gap_penalty = -5


def _match_score(nucleotide1, nucleotide2, substitution_matrix):
    return substitution_matrix[nucl_dict[nucleotide1], nucl_dict[nucleotide2]],


def _swap_columns(array, frm, to):
    array[:, [frm, to]] = array[:, [to, frm]]


def _prepare_columns(rows, initialize_value):
    result = np.empty([rows + 1, 2], int)
    for x in range(rows + 1):
        result[x][0] = x * initialize_value
        result[x][1] = 0
    return result


# find max matching - using in Needleman-Wunsch algorithm, which use matrix with 2 columns
def _max_match_two_columns(score, i, nucleotide1, nucleotide2, substitution_matrix):
    match = score[i-1][0] + _match_score(nucleotide1, nucleotide2, substitution_matrix)
    gap_first = score[i][0] + gap_penalty
    gap_second = score[i-1][1] + gap_penalty

    return max(match, gap_first, gap_second)


# method which calculate score for pairwise alignment (only score)
def _calculate_score(seq1, seq2, length_of_seq1, length_of_seq2, substitution_matrix):
    # use matrix with 2 columns to minimalizing computational complexity
    score = _prepare_columns(length_of_seq1, gap_penalty)
    j = 1
    while j <= length_of_seq2:
        score[0][1] = j * gap_penalty
        i = 1
        while i <= length_of_seq1:
            # choose the best score from earlier calculating (dynamic programming)
            score[i][1] = _max_match_two_columns(score, i, seq1[i - 1], seq2[j - 1], substitution_matrix)
            i += 1
        # swap columns to enable later calculations in a simply way
        _swap_columns(score, 0, 1)
        j += 1

    return score


# parallel two sequences using simplified version of Needleman-Wunsch algorithm (it calculates only score of alignment)
def parallel(seq1, seq2, substitution_matrix):
    length_of_seq1, length_of_seq2 = len(seq1), len(seq2)
    return _calculate_score(seq1, seq2, length_of_seq1, length_of_seq2, substitution_matrix)[length_of_seq1][0]


if __name__ == "__main__":
    input = open("../data/sequence_presentation.txt", "r")

    seq1 = input.readline().rstrip('\n')
    seq2 = input.readline().rstrip('\n')
    seq3 = "ACTGGTCAT"
    seq4 = "ACGGATCGTATC"

