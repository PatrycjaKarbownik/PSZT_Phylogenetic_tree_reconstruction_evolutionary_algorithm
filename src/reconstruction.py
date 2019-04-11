from alignment import calculate_similarities, multiple_alignment
from nodes import *
from phylogenetic_tree import *
import scoring
import graphic_tree
import time
import multiprocessing as mp
from substitution_matrix import SubstitutionMatrix

tmp_leaves = []
leaves = []
start_time = time.clock()

# We're using manager which will provide a shared list between processes
manager = mp.Manager()
trees = manager.list()


def EvolutionFunc(tmp_leaves, leaves):
    sub_matrix = SubstitutionMatrix(True)
    best_tree = None
    global trees

    while not sub_matrix.reached_stop():
        sub_matrix.change_substitution_matrix()
        similarity_matrix = calculate_similarities(tmp_leaves, sub_matrix)
        node = create_tree(similarity_matrix, leaves)
        columns = scoring.make_columns(tmp_leaves)
        score = scoring.score_tree(node, columns, leaves, sub_matrix)
        if sub_matrix.has_better_bootstrap_value(score):
            best_tree = (node, score)

    trees.append(best_tree)


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

proc_num = int(input("Number of processes: "))

processes = []
for i in range(proc_num):
    new_proc = mp.Process(target=EvolutionFunc, args=(tmp_leaves, leaves, ))
    new_proc.start()
    processes.append(new_proc)

while not all(not process.is_alive() for process in processes):
    pass

print("Time of everything: " + str(time.clock() - start_time))

trees = sorted(trees, key=lambda tree: tree[1])

graphic_tree.run_graphics(trees)
