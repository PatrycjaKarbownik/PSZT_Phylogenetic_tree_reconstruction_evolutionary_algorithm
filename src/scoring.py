import random
import numpy as np


# f function used to calculate score of vertices
# x is probability
def f(x):
    if x < 0 or x > 1:
        return 0
    # We need to use here numpy since simple ** (1/3) will cause function to return complex number for x < 0.7
    return np.cbrt(x - 0.7) + 1


# As we'll work on indexes, this function just samples with replacement numbers from 0 to amount of leaves in tree
# It may output from number 5 result: 0 4 3 4 2, which means that tree will be constructed from
# leaves with numbers 0, 2, 3 and two times 4
def sample_with_replacement(data):
    result = list()
    amount_of_seq = len(data)
    length_of_seq = len(data[0])

    for i in range(amount_of_seq):
        result.append('')

    for i in range(length_of_seq):
        rand = random.randint(0, length_of_seq - 1)
        for j in range(amount_of_seq):
            result[j] += data[j][rand]
    return result


# Example of sequences:
# T A T C G
# T A T G G
# T T T C C
# Result : list ["TTT", "AAT", "TTT", "CGC", "GGC"]
def make_columns(data):
    result = list()
    # We're initializing index in list for every column in sequence (we're assuming we work with pre-aligned data)
    for sequence in range(len(data[0])):
        result.append('')

    for sequence in data:
        for i in range(len(sequence)):
            result[i] += sequence[i]

    return result


def score_tree(nodes, index_of_tree, similarity_matrix):
    pass


if __name__ == "__main__":
    example_data = ["GADAT", "TCATT", "TGTCT", "ACTGT"]
    print("Example data:")
    for example in example_data:
        print(example)

    columns = make_columns(example_data)

    new = sample_with_replacement(example_data)
    print("\nBootstrapped data:")
    for i in new:
        print(i)

    print("\nExample values of function f(x)")
    for x in (0.65, 0.70, 0.75):
        print("f({0:4.2f}) = {1:8.6f}".format(x, f(x)))
