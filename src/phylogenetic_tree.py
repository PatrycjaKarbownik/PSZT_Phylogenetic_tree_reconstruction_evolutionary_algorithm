from nodes import Node
from parallel import parallel
from symmetric_matrix import SymmetricMatrix
import numpy as np


def create_tree(nodes):
    similarity_matrix = calculate_similarities(nodes)  # firstly calculating similarity for leaves, which are in nodes list
    availability = np.full(len(nodes), True)  # creating list of boolean to read if a node can be choose to connect with other
    print(similarity_matrix)
    print(availability)

    first, second = similarity_matrix.get_max(availability)
    print(first, second)
    print(nodes[first].name, nodes[second].name + '\n')
    connect_nodes(availability, nodes, first, second)  # connecting best suited sequences
    correct_matrix(similarity_matrix, availability, first, second)
    print(similarity_matrix)
    print(availability)


def calculate_similarities(leaves):
    matrix = SymmetricMatrix(len(leaves))
    for row in range(len(matrix)):
        for column in range(row + 1):
            if row == column: continue
            matrix[row, column] = parallel(leaves[row].sequence, leaves[column].sequence)
    return matrix


def connect_nodes(availability, nodes, first_node, second_node):
    nodes[first_node] = Node(nodes[first_node], nodes[second_node])  # creating new node connecting two suited nodes
    availability[second_node] = False  # changing boolean value in one of connecting nodes in order to not analyze it later

    for node in nodes:
        print(node)


def correct_matrix(similarity_matrix, availability, first_node, second_node):
    # TODO: correct_matrix
    # temporary it will be average of values from nodes:
    for i in range(len(similarity_matrix)):
        if availability[i] and not (i == first_node or i == second_node):
            similarity_matrix[first_node, i] = (similarity_matrix[first_node, i] + similarity_matrix[second_node, i])/2
