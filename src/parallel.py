import numpy as np

A = 0
G = 1
C = 2
T = 3
GAP = 4

gap_penalty = -5

substitution_matrix = [[10,             -1,             -3,             -4,     gap_penalty],
                       [-1,              7,             -5,             -3,     gap_penalty],
                       [-3,             -5,              9,              0,     gap_penalty],
                       [-4,             -3,              0,              8,     gap_penalty],
                       [gap_penalty, gap_penalty,  gap_penalty,  gap_penalty,       2]]


def _match_score(nucleotide1, nucleotide2):
    return {
        ('A', 'A'): substitution_matrix[A][A],
        ('A', 'G'): substitution_matrix[A][G],
        ('A', 'C'): substitution_matrix[A][C],
        ('A', 'T'): substitution_matrix[A][T],
        ('A', '-'): substitution_matrix[A][GAP],
        ('G', 'A'): substitution_matrix[G][A],
        ('G', 'G'): substitution_matrix[G][G],
        ('G', 'C'): substitution_matrix[G][C],
        ('G', 'T'): substitution_matrix[G][T],
        ('G', '-'): substitution_matrix[G][GAP],
        ('C', 'A'): substitution_matrix[C][A],
        ('C', 'G'): substitution_matrix[C][G],
        ('C', 'C'): substitution_matrix[C][C],
        ('C', 'T'): substitution_matrix[C][T],
        ('C', '-'): substitution_matrix[C][GAP],
        ('T', 'A'): substitution_matrix[T][A],
        ('T', 'G'): substitution_matrix[T][G],
        ('T', 'C'): substitution_matrix[T][C],
        ('T', 'T'): substitution_matrix[T][T],
        ('T', '-'): substitution_matrix[T][GAP],
        ('-', 'A'): substitution_matrix[GAP][A],
        ('-', 'G'): substitution_matrix[GAP][G],
        ('-', 'T'): substitution_matrix[GAP][T],
        ('-', 'C'): substitution_matrix[GAP][C],
        ('-', '-'): substitution_matrix[GAP][GAP],

    }[nucleotide1, nucleotide2]


def simple_parallel(seq1, seq2):  # compare two sequences char-to-char
    length_of_seq = len(seq1)
    score = 0
    for i in range(length_of_seq):
        score += _match_score(seq1[i], seq2[i])

    return score


def _max_match(score, i, nucleotide1, nucleotide2):
    match = score[i-1][0] + _match_score(nucleotide1, nucleotide2), i-1, 0
    gap_first = score[i][0] + gap_penalty, i, 0
    gap_second = score[i-1][1] + gap_penalty, i-1, 1

    return max(match, gap_first, gap_second)


def _swap_columns(array, frm, to):
    array[:, [frm, to]] = array[:, [to, frm]]


def _prepare_columns(rows, initialize_value):
    result = np.empty([rows + 1, 2], int)  # use matrix with 2 columns to minimalizing computational complexity

    for x in range(rows + 1):
        result[x][0] = x * initialize_value
        result[x][1] = 0

    return result


# def parallel(seq1, seq2):
#     length_of_seq1 = len(seq1)
#     length_of_seq2 = len(seq2)
#     # prepare temp table to calculate score for the best alignment
#     score = _prepare_columns(length_of_seq1, gap_penalty)
#     # stripped Needleman-Wunsch algorithm using dynamic programming
#     return _calculate_score(score, seq1, seq2, 0, length_of_seq2, 0, length_of_seq1)[length_of_seq1][0]


def _calculate_score(seq1, seq2, length_of_seq1, length_of_seq2):
    # length_of_seq2 = end_j - begin_j
    # length_of_seq1 = end_i - begin_i

    # prepare temp table to calculate score for the best alignment
    score = _prepare_columns(length_of_seq1, gap_penalty)

    j = 1
    while j <= length_of_seq2:
        score[0][1] = j * gap_penalty
        i = 1
        while i <= length_of_seq1:
            score[i][1] = float(_max_match(score, i, seq1[i-1], seq2[j-1])[0])
            i += 1
        _swap_columns(score, 0, 1)
        j += 1

    return score

def _calculate_indexes(score, seq1, seq2, begin_i, end_i, begin_j, end_j):
    length_of_seq1 = end_i - begin_i
    # prepare temp table to calculate score for the best alignment
    indexes = _prepare_columns(length_of_seq1, 1)

    j = begin_j + 1
    while j <= end_j:
        score[0][1] = j * gap_penalty
        indexes[0][1] = 0
        i = begin_i + 1
        while i <= length_of_seq1:
            max_match = _max_match(score, i, seq1[i - 1], seq2[j - 1])
            score[i][1], index_i, index_j = float(max_match[0]), int(max_match[1]), int(max_match[2])
            indexes[i][1] = indexes[index_i, index_j]
            i += 1
        _swap_columns(score, 0, 1)
        _swap_columns(indexes, 0, 1)
        print(score)
        print(indexes)
        j += 1
    return indexes[length_of_seq1][0]


def parallel(seq1, seq2):
    length_of_seq1, length_of_seq2 = len(seq1), len(seq2)
    return _calculate_score(seq1, seq2, length_of_seq1, length_of_seq2)[length_of_seq1][0]


def needleman_wunsch(result, seq1, seq2, begin_i, end_i, begin_j, end_j):
    length_of_seq1 = end_i - begin_i
    length_of_seq2 = end_j - begin_j
    if length_of_seq1 <= 2 and length_of_seq2 <=2:
        # return STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP
        pass
    m_div_2 = begin_j + int((end_j - begin_j) / 2) + ((end_j - begin_j) % 2 > 0)
    length_of_seq2 = m_div_2 - begin_j


    if begin_i != 0:
        length_of_seq1 += 1
    if begin_j !=0:
        length_of_seq2 += 1
    score = _calculate_score(seq1, seq2, length_of_seq1, length_of_seq2)
    print(score)
    index = _calculate_indexes(score, seq1, seq2, begin_i, end_i, m_div_2, end_j)
    print(index)
    result.append([index - 1, m_div_2 - 1])

    left = needleman_wunsch(result, seq1, seq2, begin_i, index, begin_j, m_div_2)
    right = needleman_wunsch(result, seq1, seq2, index, end_i, m_div_2, end_j)
    result = left + result.append([index - 1, m_div_2 - 1]) + right

    return result




if __name__ == "__main__":
    input = open("../data/sequence_presentation.txt", "r")

    sequence1 = input.readline().rstrip('\n')
    sequence2 = input.readline().rstrip('\n')

    # print(parallel(sequence1, sequence2))
    result = []
    print(needleman_wunsch(result, sequence1, sequence2, 0, len(sequence1), 0, len(sequence2)))
    print(result)
