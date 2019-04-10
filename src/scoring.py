import random
import nodes as n
import numpy as np
import phylogenetic_tree as p_tree

# Amount of bootstrapped data
boot_amount = 100


# f function used to calculate score of vertices
# x is probability
def f(x):
    if x < 0 or x > 1:
        return 0
    # We need to use here numpy since simple ** (1/3) will cause function to return complex number for x < 0.7
    return np.cbrt(x - 0.7) + 1


# As we'll work on indexes, this function just samples with replacement numbers from 0 to amount of columns in sequence
# It may output from number 5 result: 0 4 3 4 2,
def _sample_with_replacement(length_of_seq):
    result = list()

    for i in range(length_of_seq):
        rand = random.randint(0, length_of_seq - 1)
        result.append(rand)
    return result


# Example:
# T A T C G
# T A T G G
# T T T C C
# Result : list ["TTT", "AAT", "TTT", "CGC", "GGC"]
def make_columns(leaves):
    result = list()
    length = len(leaves[0].sequence)
    # We're initializing index in list for every column in sequence (we're assuming we work with pre-aligned data)
    for sequence in range(length):
        result.append('')

    for leaf in leaves:
        for i in range(length):
            result[i] += leaf.sequence[i]

    return result


def _generate_from_columns(columns):
    pass


# Later it'll be implemented not recursively
def _list_nodes(first_node):
    result = list()

    def _take_node(node, nodes_list):
        if isinstance(node, n.Leaf):
            return
        nodes_list.append(node)
        _take_node(node.left, nodes_list)
        _take_node(node.right, nodes_list)

    _take_node(first_node, result)
    return result


# Since these sequences can get big really quick we'll need to do every step of making and calculating new tree
# separately allowing memory to clear out strings we don't need
def score_tree(tree, columns, leaves, substitution_matrix):
    new_trees = []
    seq_amount = len(columns[0])
    length_of_seq = len(columns)
    # We're making list of nodes because later in algorithm we'll look for every node from basic tree in new trees
    list_of_nodes = _list_nodes(tree)

    for i in range(boot_amount):
        # len(columns) return amount of columns in sequence, which is, well, length of sequence we're looking for
        col_order = _sample_with_replacement(length_of_seq)
        new_sequences = list()
        # We initialize new sequences
        for pos in range(seq_amount):
            new_sequences.append('')
        # Now we're creating sequences based on columns order we generated
        for col in col_order:
            for pos in range(seq_amount):
                new_sequences[pos] += columns[col][pos]

        # We can now generate our new tree from bootstrapped data, starting off with leaves
        tmp_leaves = []
        for j, leaf in enumerate(leaves):
            tmp_leaves.append(n.TmpLeaf(leaf.name, leaf.year, j, new_sequences[j]))
        similarity_matrix = p_tree.calculate_similarities(tmp_leaves, substitution_matrix)
        boot_tree = p_tree.create_tree(similarity_matrix, leaves)

        # Now we can finally count what nodes from our tree are in new tree
        list_of_new_nodes = _list_nodes(boot_tree)
        for node in list_of_nodes:
            for boot_node in list_of_new_nodes:
                if node == boot_node:
                    node.bootstrap += 1
                    break

    # print("TREE WITH BOOTSTRAP: ")
    # print(tree)

    # Now after we calculated bootstrap values for all of our nodes, we have to calculate score of a tree
    score = 0
    for node in list_of_nodes:
        # print(node.bootstrap / boot_amount)
        score += f(node.bootstrap / boot_amount)

    return score


if __name__ == "__main__":
    example_data = ["GADAT", "TCATT", "TGTCT", "ACTGT"]
    print("Example data:")
    for example in example_data:
        print(example)

    new = _sample_with_replacement(len(example_data[0]))
    print("\nBootstrapped data:")
    for _ in new:
        print(_)

    print("\nExample values of function f(x)")
    for x in (0.65, 0.70, 0.75):
        print("f({0:4.2f}) = {1:8.6f}".format(x, f(x)))
