from nodes import Node
import numpy as np
from symmetric_matrix import *
from parallel import *


def create_tree(similarity_matrix, leaves):
    nodes = leaves.copy()
    length_of_nodes = len(nodes)
    availability = np.full(length_of_nodes, True)  # creating list of boolean to read if a node can be choose to connect with other

    for i in range(length_of_nodes - 1):
        first, second = similarity_matrix.get_max(availability)  # finding the best similarity
        _connect_nodes(availability, nodes, first, second)  # connecting best suited sequences
        _correct_matrix(similarity_matrix, availability, first, second)  # correcting values in similarity_matrix because
                                                        # after connecting the similarities between nodes has change
    found = False
    while not found:  # finding last available node where is the tree
        for i in range(length_of_nodes):
            if availability[i]:
                found = True
                index_of_tree = i

    return nodes[index_of_tree]


def calculate_similarities(leaves, substitution_matrix):
    matrix = SymmetricMatrix(len(leaves))
    for row in range(len(matrix)):
        for column in range(row + 1):
            if row == column: continue
            matrix[row, column] = parallel(leaves[row].sequence, leaves[column].sequence, substitution_matrix)
    return matrix


def _connect_nodes(availability, nodes, first_node, second_node):
    nodes[first_node] = Node(nodes[first_node], nodes[second_node])  # creating new node connecting two suited nodes
    availability[second_node] = False  # changing boolean value in one of connecting nodes in order to not analyze it later


def _correct_matrix(similarity_matrix, availability, first_node, second_node):
    # TODO: correct_matrix
    # temporary it will be average of values from nodes:
    for i in range(len(similarity_matrix)):
        if availability[i] and not (i == first_node or i == second_node):
            similarity_matrix[first_node, i] = (similarity_matrix[first_node, i] + similarity_matrix[second_node, i])/2
