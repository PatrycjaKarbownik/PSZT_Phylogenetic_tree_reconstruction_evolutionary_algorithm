# Implementation of symmetric matrix
# It is stored as one dimension array
import sys


class SymmetricMatrix:

    def __init__(self, size):
        if size <= 0:
            raise ValueError("Size of matrix is expected to be integer greater than 0")
        self._size = size
        self._matrix = list()
        for i in range((size + 1) * size // 2):
            self._matrix.append(0)

    def __len__(self):
        return self._size

    def __setitem__(self, key, value):
        index = self._get_index(key)
        self._matrix[index] = value

    def __getitem__(self, key):
        index = self._get_index(key)
        return self._matrix[index]

    # Since this class is represented as one-dimension array, we have to calculate index of position (row, column)
    @staticmethod
    def _get_index(key):
        column, row = key
        # Since (column, row) should have same value as (row, column), we want to operate on one of these
        if column > row:
            column, row = row, column
        index = (row * (row + 1) // 2) + column
        return index

    def get_max(self, availability):
        maximum = -sys.maxsize
        column_max = row_max = 0
        for row in range(self._size):
            if not availability[row]:
                continue
            for column in range(row + 1, self._size):
                if not availability[column]:
                    continue
                value = self._matrix[self._get_index((column, row))]
                if maximum < value:
                    maximum = value
                    column_max = column
                    row_max = row
        return column_max, row_max

    def __str__(self):
        string = ""
        for column in range(self._size):
            tmp = ''
            for row in range(self._size):
                tmp += str(float(self._matrix[self._get_index((column, row))]))
                tmp += ' ' * (15 - len(tmp) % 15)
            string += tmp + '\n'
        return string

    def copy(self):
        new_matrix = self._matrix.copy()
        result = SymmetricMatrix(self._size)
        result._matrix = new_matrix
        return result

    # Instead of putting elements one by one manually you just give it a list of half of matrix including diagonal
    def set_from_list(self, given_list):
        if len(given_list) != len(self._matrix):
            return
        self._matrix = given_list.copy()

    # Same as set, but instead setting new values you add value to every position in matrix
    def add_from_list(self, given_list):
        if len(given_list) != len(self._matrix):
            return
        for pos, value in enumerate(given_list, 0):
            self._matrix[pos] += value

    # Same as add_from_list, but instead add value you multiply every position in matrix
    def multiply_from_list(self, given_list):
        if len(given_list) != len(self._matrix):
            return
        for pos, value in enumerate(given_list, 0):
            self._matrix[pos] *= value

if __name__ == "__main__":
    matrix = SymmetricMatrix(4)
    matrix2 = matrix.copy()
    matrix[1, 2] = 3
    print(matrix)
    print(matrix2)
    matrix2.set_from_list([1,
                           2, 3,
                           4, 5, 6,
                           7, 8, 9, 10])
    print(matrix2)
    matrix2.add_from_list([0,
                           1, 0,
                           1, 0, 1,
                           1, 1, 1, 3])
    print(matrix2)