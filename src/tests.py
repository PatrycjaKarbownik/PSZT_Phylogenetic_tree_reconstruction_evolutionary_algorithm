"""Simple tests written to make sure our methods for comparing nodes do the job
We did tests for this as this is crucial part of our scoring system"""

from nodes import *

if __name__ != "__main__":

    # Construction of tree1

    a1 = Leaf("a", "1")
    b1 = Leaf("b", "1")
    c1 = Leaf("c", "2")
    d1 = Leaf("d", "1")
    e1 = Leaf("e", "1")

    node11 = Node(b1, c1)
    node12 = Node(a1, node11)
    node13 = Node(d1, e1)
    tree1 = Node(node12, node13)

    # Construction of tree2
    a2 = Leaf("a", "1")
    b2 = Leaf("b", "1")
    c2 = Leaf("c", "2")
    d2 = Leaf("d", "1")
    e2 = Leaf("e", "1")

    node21 = Node(d2, e2)
    node22 = Node(b2, c2)
    node23 = Node(a2, node22)
    tree2 = Node(node21, node23)

    # Construction of tree3
    a3 = Leaf("a", "3")
    b3 = Leaf("b", "3")
    c3 = Leaf("c", "3")
    d3 = Leaf("d", "3")

    node31 = Node(b3, c3)
    node32 = Node(node31, d3)
    tree3 = Node(node32, a3)

    # Construction of tree4
    a4 = Leaf("a", "3")
    b4 = Leaf("b", "3")
    c4 = Leaf("c", "3")
    d4 = Leaf("d", "3")

    node41 = Node(c4, b4)
    node42 = Node(d4, node41)
    tree4 = Node(a4, node42)

    # Construction of tree5
    a5 = Leaf("a", "4")
    b5 = Leaf("b", "4")
    c5 = Leaf("c", "4")

    node51 = Node(a5, b5)
    tree5 = Node(node51, c5)

    # Construction of tree6
    a6 = Leaf("a", "4")
    b6 = Leaf("b", "4")
    c6 = Leaf("c", "4")

    node61 = Node(a1, c1)
    tree6 = Node(node61, b6)

    # Construction of tree7
    a7 = Leaf("a", "4")
    b7 = Leaf("b", "4")
    c7 = Leaf("c", "4")

    node71 = Node(a7, b7)
    tree7 = Node(c7, node71)


    class TreeTestError(Exception):
        pass


    try:
        if tree1 != tree2:
            raise TreeTestError("First")
        if tree3 != tree4:
            raise TreeTestError("Second")
        if tree5 == tree6:
            raise TreeTestError("Third")
        if tree5 != tree7:
            raise TreeTestError("Fourth")
        if tree6 == tree7:
            raise TreeTestError("Fifth")

    except TreeTestError as e:
        print("\033[1;31m " + str(e) + " test has failed")
