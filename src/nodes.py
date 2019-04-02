class Leaf:
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
        string = str(self.left) + str(self.right)
        return string
