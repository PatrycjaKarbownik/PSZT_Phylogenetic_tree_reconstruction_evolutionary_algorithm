"""Main module responsible for connecting every piece of reconstruction"""
from alignment import calculate_similarities, multiple_alignment
from nodes import *
from phylogenetic_tree import *
import scoring
import graphic_tree
import time
import multiprocessing as mp
from substitution_matrix import SubstitutionMatrix
import parallel


# This function does the evolution and then saves the best tree to shared list
def evolution_fun(tmp_leaves, leaves):
    started_tmp_leaves = tmp_leaves
    sub_matrix = SubstitutionMatrix(True)
    best_tree = None
    global trees

    while not sub_matrix.reached_stop():
        # conteners have to be have started value
        leaves = []
        tmp_leaves = []
        for started_leaf in started_tmp_leaves:
            tmp_leaves.append(
                TmpLeaf(started_leaf.name, started_leaf.year, started_leaf.number, started_leaf.sequence))

        # Multiple alignment
        similarity_matrix = calculate_similarities(tmp_leaves, sub_matrix)
        temp_seq = multiple_alignment(similarity_matrix, tmp_leaves)
        print(len(temp_seq))
        print(len(tmp_leaves))
        for i in range(len(temp_seq)):
            tmp_leaves[i].sequence = temp_seq[i]

        for i, leaf in enumerate(tmp_leaves):
            leaves.append(Leaf(leaf.name, leaf.year, i))

        # First we generate our new substitution matrix
        sub_matrix.change_substitution_matrix()

        # We need now to calculate similiarities in order to generate new tree
        similarity_matrix = calculate_similarities(tmp_leaves, sub_matrix)
        node = create_tree(similarity_matrix, leaves)

        # Now we're scoring out tree
        columns = scoring.make_columns(tmp_leaves)
        score = scoring.score_tree(node, columns, leaves, sub_matrix)

        # At last we save our best tree. has_better_bootstrap_value automatically changes sub_matrix
        # to it's previous state if it detects that it had worse score than previous one
        if sub_matrix.has_better_bootstrap_value(score):
            best_tree = (node, score)

    trees.append(best_tree)


def load():
    n = 0
    #    with open("../data/old_sequences.txt", "r") as file:
    with open("../data/test02.txt", "r") as file:
        for i, line in enumerate(file):
            n += 1
            if n % 2 == 1:
                first_line = line.rstrip('\n').lstrip('<').split()
                name, year = first_line[0], int(first_line[1])
            else:
                sequence = line.rstrip('\n')
                tmp_leaves.append(TmpLeaf(name, year, i, sequence))

    file.close()


if __name__ == "__main__":
    mp.freeze_support()

    tmp_leaves = []
    leaves = []
    start_time = time.clock()

    # We're using manager which will provide a shared list between processes
    manager = mp.Manager()
    trees = manager.list()

    load()

    proc_num = int(input("Number of processes: "))

    # Since we want our results to be as closely to maximum as possible, we can run our algorithm parallel with
    # Randomly generated data
    processes = []
    for i in range(proc_num):
        new_proc = mp.Process(target=evolution_fun, args=(tmp_leaves, leaves,))
        new_proc.start()
        processes.append(new_proc)

    while not all(not process.is_alive() for process in processes):
        pass

    print("Time of everything: " + str(time.clock() - start_time))

    trees = sorted(trees, key=lambda tree: tree[1])

    graphic_tree.run_graphics(trees)

