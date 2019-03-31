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

    }.get((nucleotide1, nucleotide2), startingGapPenalty) #[nucleotide1, nucleotide2]


def parallel(seq1, seq2):
    return 0


if __name__ == "__main__":
    input = open("sequences.txt", "r")

    sequence1 = input.readline().rstrip('\n')
    sequence2 = input.readline().rstrip('\n')

    parallel(sequence1, sequence2)