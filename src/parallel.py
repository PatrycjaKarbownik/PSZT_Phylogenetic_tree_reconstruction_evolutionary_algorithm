import numpy as np

# Nucleotide dictionary
nucl_dict = {
    'A': 0,
    'G': 1,
    'C': 2,
    'T': 3,
    '-': 4
}

gap_penalty = -5

substitution_matrix = [[10,             -1,             -3,             -4,     gap_penalty],
                       [-1,              7,             -5,             -3,     gap_penalty],
                       [-3,             -5,              9,              0,     gap_penalty],
                       [-4,             -3,              0,              8,     gap_penalty],
                       [gap_penalty, gap_penalty,  gap_penalty,  gap_penalty,       2]]


def _match_score(nucleotide1, nucleotide2):
    return substitution_matrix[nucl_dict[nucleotide1]][nucl_dict[nucleotide2]],


def _swap_columns(array, frm, to):
    array[:, [frm, to]] = array[:, [to, frm]]


def _prepare_columns(rows, initialize_value):
    result = np.empty([rows + 1, 2], int)  # use matrix with 2 columns to minimalizing computational complexity

    for x in range(rows + 1):
        result[x][0] = x * initialize_value
        result[x][1] = 0

    return result


def simple_parallel(seq1, seq2):  # compare two sequences char-to-char
    length_of_seq = len(seq1)
    score = 0
    for i in range(length_of_seq):
        score += _match_score(seq1[i], seq2[i])

    return score


def _max_match_two_columns(score, i, nucleotide1, nucleotide2):
    match = score[i-1][0] + _match_score(nucleotide1, nucleotide2), i-1, 0
    gap_first = score[i][0] + gap_penalty, i, 0
    gap_second = score[i-1][1] + gap_penalty, i-1, 1

    return max(match, gap_first, gap_second)


def _calculate_score(seq1, seq2, length_of_seq1, length_of_seq2):
    score = _prepare_columns(length_of_seq1, gap_penalty)

    j = 1
    while j <= length_of_seq2:
        score[0][1] = j * gap_penalty
        i = 1
        while i <= length_of_seq1:
            score[i][1] = float(_max_match_two_columns(score, i, seq1[i - 1], seq2[j - 1])[0])
            i += 1
        _swap_columns(score, 0, 1)
        j += 1

    return score


def parallel(seq1, seq2):
    length_of_seq1, length_of_seq2 = len(seq1), len(seq2)
    return _calculate_score(seq1, seq2, length_of_seq1, length_of_seq2)[length_of_seq1][0]


def _simple_needleman_wunsch_score(seq1, seq2):
    length_of_seq1, length_of_seq2 = len(seq1), len(seq2)
    result = np.empty([length_of_seq1 + 1, length_of_seq2 + 1], int)  # prepare matrix for scoring the alignment

    for i in range(length_of_seq1 + 1):
        result[i][0] = i * gap_penalty
    for j in range(length_of_seq2 + 1):
        result[0][j] = j * gap_penalty

    for j in range(1, length_of_seq2 + 1):
        for i in range(1, length_of_seq1 + 1):
            gap1 = result[i][j-1] + gap_penalty
            gap2 = result[i-1][j] + gap_penalty
            align = result[i-1][j-1] + _match_score(seq1[i-1], seq2[j-1])
            result[i][j] = max(gap1, gap2, align)

    return result


def get_aligned_sequences(score, seq1, seq2):
    length_of_seq1, length_of_seq2 = len(seq1), len(seq2)
    j = length_of_seq2
    i = length_of_seq1
    seq1_aligned = ''
    seq2_aligned = ''
    while i > 0 or j > 0:
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

    seq1_aligned = seq1_aligned[::-1]
    seq2_aligned = seq2_aligned[::-1]
    return seq1_aligned, seq2_aligned


def pairwise_alignment(seq1, seq2):
    score = _simple_needleman_wunsch_score(seq1, seq2)
    return get_aligned_sequences(score, seq1, seq2)


if __name__ == "__main__":
    input = open("../data/sequence_presentation.txt", "r")

    seq1 = input.readline().rstrip('\n')
    seq2 = input.readline().rstrip('\n')

    print(pairwise_alignment(seq1, seq2))

