from nodes import *
from phylogenetic_tree import *
import scoring
import graphic_tree
import time
from substitution_matrix import SubstitutionMatrix

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

trees = []
sub_matrix = SubstitutionMatrix()
while not sub_matrix.reached_stop():
    sub_matrix.changeSubstitutionMatrix()
    similarity_matrix = calculate_similarities(tmp_leaves, sub_matrix)  # firstly calculating similarity for leaves (sequences)
    node = create_tree(similarity_matrix, leaves)
    columns = scoring.make_columns(tmp_leaves)
    score = scoring.score_tree(node, columns, leaves, sub_matrix)
    if sub_matrix.has_better_bootstrap_value(score):
        trees.append((node, score))
    print("DOIN")

print("Time of everything: " + str(time.clock() - start_time))

graphic_tree.run_graphics(trees)
