from nodes import *
from phylogenetic_tree import *
import scoring
import graphic_tree
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
for i, leaf in enumerate(tmp_leaves):
    leaves.append(Leaf(leaf.name, leaf.year, i))
    print(leaf)
similarity_matrix = calculate_similarities(tmp_leaves)  # firstly calculating similarity for leaves (sequences)

node = create_tree(similarity_matrix, leaves)
columns = scoring.make_columns(tmp_leaves)
score = scoring.score_tree(node, columns, leaves, None)

node2 = create_tree(similarity_matrix, leaves)
columns = scoring.make_columns(tmp_leaves)
scoring.score_tree(node2, columns, leaves, None)

print("Time of everything: " + str(time.clock() - start_time))
print("Score of bootstrap: " + str(score))

graphic_tree.run_graphics([node, node2])
