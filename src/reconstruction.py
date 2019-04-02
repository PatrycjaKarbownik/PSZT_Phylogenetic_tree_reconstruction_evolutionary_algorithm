from leaf import Leaf
from phylogenetic_tree import create_tree

leaves = []


def load():
    n = 0
    with open("../data/sequences.txt", "r") as file:
        for line in file:
            n += 1
            if (n % 2 == 1):
                first_line = line.rstrip('\n').lstrip('<').split()
                name, year = first_line[0], int(first_line[1])
            else:
                sequence = line.rstrip('\n')
               # print(name, year, sequence)
                leaves.append(Leaf(name, year, sequence))


load()
for leaf in leaves:
    print(leaf)
create_tree(leaves)

#similarity_matrix = calculate_similarities(leaves)
#print(similarity_matrix)