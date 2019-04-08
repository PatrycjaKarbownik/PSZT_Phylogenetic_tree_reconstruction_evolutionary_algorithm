"""The most crucial part of these nodes is method for comparing them. Every leaf has its unique number which is
power of two. Nodes then store information about sum of numbers in their sons.
It speeds up a lot comparing because we don't need to dive to every part of node's sons to know if they're same
or not. We achieve this by having these powers of two - you just cannot make two sums A and B where both of them
are sums of powers of two and these sums doesn't have common components"""


class Leaf:
    def __init__(self, name, year, number):
        self.name = name
        self.year = year
        self.number = 2 ** number

    def __str__(self):
        string = self.name + ' ' + str(self.year)
        return string

    def __eq__(self, other):
        return self.number == other.number


class TmpLeaf:
    def __init__(self, name, year, number, sequence):
        self.name = name
        self.year = year
        self.number = 2 ** number
        self.sequence = sequence

    def __str__(self):
        string = self.name + ' ' + str(self.year) + ' ' + self.sequence
        return string


class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.number = left.number + right.number
        self.bootstrap = 0

    def __str__(self):
        string = "(" + str(self.bootstrap) + ")" + "left: " + str(self.left) + " right: " + str(self.right)
        return string

    def __eq__(self, other):
        if self.number != other.number:
            return False
        return (((self.left == other.left) and (self.right == other.right))
                or ((self.right == other.left) and (self.left == other.right)))
