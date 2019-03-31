import numpy as np

A = 0
G = 1
C = 2
T = 3

substitutionMatrix = [[10, -1, -3, -4],
                      [-1,  7, -5, -3],
                      [-3, -5,  9,  0],
                      [-4, -3,  0,  8]]

startingGapPenalty = -5
#extendingGapPenalty = -5


def match_score(nucleotide1, nucleotide2):
    return {
        ('A', 'A'): substitutionMatrix[A][A],
        ('A', 'G'): substitutionMatrix[A][G],
        ('A', 'C'): substitutionMatrix[A][C],
        ('A', 'T'): substitutionMatrix[A][T],
        ('G', 'A'): substitutionMatrix[G][A],
        ('G', 'G'): substitutionMatrix[G][G],
        ('G', 'C'): substitutionMatrix[G][C],
        ('G', 'T'): substitutionMatrix[G][T],
        ('C', 'A'): substitutionMatrix[C][A],
        ('C', 'G'): substitutionMatrix[C][G],
        ('C', 'C'): substitutionMatrix[C][C],
        ('C', 'T'): substitutionMatrix[C][T],
        ('T', 'A'): substitutionMatrix[T][A],
        ('T', 'G'): substitutionMatrix[T][G],
        ('T', 'C'): substitutionMatrix[T][C],
        ('T', 'T'): substitutionMatrix[T][T],

    }.get((nucleotide1, nucleotide2), startingGapPenalty) # [nucleotide1, nucleotide2]


def maxMatch(score, i,  nucleotide1, nucleotide2):
    match = score[i-1][0] + match_score(nucleotide1, nucleotide2)
    gap_first = score[i][0] + startingGapPenalty
    gap_second = score[i-1][1] + startingGapPenalty

    return max(match, gap_first, gap_second)


def parallel(seq1, seq2):
    lengthOfSeq1, lengthOfSeq2 = len(seq1), len(seq2)
    print(lengthOfSeq1, lengthOfSeq2)
    score = np.empty([lengthOfSeq1 + 1, 2], int)

    # prepare temp table
    for x in range(lengthOfSeq1 + 1):
        print(x)
        score[x][0] = x * startingGapPenalty
        score[x][1] = 0

    print(score)

    j = 1
    while j <= lengthOfSeq2:
        print(j)
        score[0][1] = j * startingGapPenalty
        i = 1
        while i <= lengthOfSeq1:
            print("j = ", j, " i = ", i)
            score[i][1] = maxMatch(score, i, seq1[i-1], seq2[j-1])
            i += 1
        print(score)
        score[0] = score[1]
        print("change")
        print(score)
        j += 1


    #score[x][x] = maxMatch(seq1[x], seq2[x])
    #score =


if __name__ == "__main__":
    input = open("../data/sequences.txt", "r")

    sequence1 = input.readline().rstrip('\n')
    sequence2 = input.readline().rstrip('\n')

    parallel(sequence1, sequence2)
