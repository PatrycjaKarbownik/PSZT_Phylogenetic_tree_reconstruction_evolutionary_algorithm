class Leaf:
    def __init__(self, name, year):
        self.name = name
        self.year = year

    def __str__(self):
        string = self.name + ' ' + str(self.year)
        return string


class TmpLeaf:
    def __init__(self, name, year, sequence):
        self.name = name
        self.year = year
        self.sequence = sequence

    def __str__(self):
        string = self.name + ' ' + str(self.year) + ' ' + self.sequence
        return string


class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        string = "left: " + str(self.left) + " right: " + str(self.right)
        return string

    # We'll need to compare both nodes and leaves
    def __eq__(self, other):
        if type(other) == type(Node(None, None)):
            return True
        else:
            return False
