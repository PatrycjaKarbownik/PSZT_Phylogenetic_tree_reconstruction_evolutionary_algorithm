from nodes import *
from phylogenetic_tree import *
import scoring

tmp_leaves = []
leaves = []


def load():
    n = 0
    with open("../data/sequences.txt", "r") as file:
        for line in file:
            n += 1
            if n % 2 == 1:
                first_line = line.rstrip('\n').lstrip('<').split()
                name, year = first_line[0], int(first_line[1])
            else:
                sequence = line.rstrip('\n')
                tmp_leaves.append(TmpLeaf(name, year, sequence))

    file.close()


load()
for leaf in tmp_leaves:
    leaves.append(Leaf(leaf.name, leaf.year))
    print(leaf)
similarity_matrix = calculate_similarities(tmp_leaves)  # firstly calculating similarity for leaves (sequences)

node = create_tree(similarity_matrix, leaves)
columns = scoring.make_columns(tmp_leaves)
for string in columns:
    print(string)

# scoring.score_tree(None, columns, None, None)
