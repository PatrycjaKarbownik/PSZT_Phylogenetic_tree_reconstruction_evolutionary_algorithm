names_of_sequences = []

def loadname():
    n = 0
    with open("../data/sequences.txt", "r") as file:
        for line in file:
            n += 1
            if n % 2 == 1:
                first_line = line.rstrip(' ').split()
                name = first_line[0]
            else:
                names_of_sequences.append(name)
    file.close()

loadname()

class Leaf:
    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.number = 0
        for i, sequence_name in enumerate(names_of_sequences):
            if(sequence_name==name):
                self.number = 2**i
        if (self.number==0):
            print("PRZYPAL...")

    def __str__(self):
        string = self.name + ' ' + str(self.year)
        return string

    def __eq__(self, other):
        return self.number == other.number


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
        self.number = left.number + right.number

    def __str__(self):
        string = "left: " + str(self.left) + " right: " + str(self.right)
        return string

    def __eq__(self, other):
        if self.number != other.number:
            return False
        return ((self.left == other.left) and (self.right == other.right)) or ((self.right == other.left) and (self.left == other.right))
