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

sub_matrix1 = SubstitutionMatrix(initial_change=True)
similarity_matrix1 = calculate_similarities(tmp_leaves, sub_matrix1)  # firstly calculating similarity for leaves (sequences)
node = create_tree(similarity_matrix1, leaves)
columns = scoring.make_columns(tmp_leaves)
score = scoring.score_tree(node, columns, leaves, sub_matrix1)

sub_matrix2 = SubstitutionMatrix()
while not sub_matrix2.reached_stop():
    sub_matrix2.changeSubstitutionMatrix()
    similarity_matrix2 = calculate_similarities(tmp_leaves, sub_matrix2)  # firstly calculating similarity for leaves (sequences)
    node2 = create_tree(similarity_matrix2, leaves)
    columns = scoring.make_columns(tmp_leaves)
    score = scoring.score_tree(node2, columns, leaves, sub_matrix2)
    sub_matrix2.checkIfBetterBootstrapValue(score)
    print("DOIN")

print("Time of everything: " + str(time.clock() - start_time))
print("Score of bootstrap: " + str(score))

graphic_tree.run_graphics([node, node2])
