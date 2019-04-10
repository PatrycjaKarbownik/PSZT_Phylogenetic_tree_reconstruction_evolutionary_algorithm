from alignment import calculate_similarities, multiple_alignment
from nodes import *
from phylogenetic_tree import *
import scoring
import graphic_tree
import time

tmp_leaves = []
leaves = []
#start_time = time.clock()

def load():
    n = 0
    with open("../data/old_sequences.txt", "r") as file:
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
for i, leaf in enumerate(tmp_leaves):
    leaves.append(Leaf(leaf.name, leaf.year, i))
    print(leaf)
similarity_matrix = calculate_similarities(tmp_leaves)  # firstly calculating similarity for leaves (sequences)
print(similarity_matrix)

multiple_alignment(similarity_matrix, tmp_leaves)






# node = create_tree(similarity_matrix, leaves)
# columns = scoring.make_columns(tmp_leaves)
# # for string in columns:
# #     print(string)
#
# score = scoring.score_tree(node, columns, leaves, None)
#
# print("Time of everything: " + str(time.clock() - start_time))
# print("Score of bootstrap: " + str(score))
#
# graphic_tree.run_graphics(node)
