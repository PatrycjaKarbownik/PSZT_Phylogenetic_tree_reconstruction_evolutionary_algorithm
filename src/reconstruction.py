from nodes import *
from phylogenetic_tree import *
import scoring
import time

tmp_leaves = []
leaves = []
start_time = time.clock()

def load():
    n = 0
    with open("../data/sequences.txt", "r") as file:
        for i, line in enumerate(file):
            n += 1
            if n % 2 == 1:
                first_line = line.rstrip('\n').lstrip('<').split()
                name, year = first_line[0], int(first_line[1])
            else:
                sequence = line.rstrip('\n')
                tmp_leaves.append(TmpLeaf(name, year, i, sequence))

    file.close()


load()
for leaf in tmp_leaves:
    # We provide here small workaround - we do want to have a power of two as a number, but not to the power of four
    # We're not yet sure if we want to stay with two different classes of leaves, so we'll use square root for a while
    leaves.append(Leaf(leaf.name, leaf.year, leaf.number ** (1/2)))
    print(leaf)
similarity_matrix = calculate_similarities(tmp_leaves)  # firstly calculating similarity for leaves (sequences)

node = create_tree(similarity_matrix, leaves)
columns = scoring.make_columns(tmp_leaves)
# for string in columns:
#     print(string)

print("Bootstrapped trees:")
scoring.score_tree(None, columns, leaves, None)

print("Time of everything: " + str(time.clock() - start_time))
