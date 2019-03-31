# Implementation of symmetric matrix
# It is stored as one dimension array


class SymmetricMatrix:
    def __init__(self, size):
        if size <= 0:
            raise ValueError("Size of matrix is expected to be integer greater than 0")
        self._size = size
        self._matrix = list()
        for i in range((size + 1) * size // 2):
                self._matrix.append(i)

    def __len__(self):
        return self._size

    def __setitem__(self, key, value):
        index = self._get_index(key)
        self._matrix[index] = value

    def __getitem__(self, key):
        index = self._get_index(key)
        return self._matrix[index]

    # Since this class is represented as one-dimension array, we have to calculate index of position (row, column)
    def _get_index(self, key):
        column, row = key
        # Since (column, row) should have same value as (row, column), we want to operate on one of these
        if column > row:
            column, row = row, column
        index = (row * (row + 1) // 2) + column
        return index

    def __str__(self):
        string = ""
        for column in range(self._size):
            for row in range(self._size):
                string += str(matrix[column, row]) + " "
            string += '\n'
        return string


if __name__ == "__main__":
    matrix = SymmetricMatrix(4)
    print(matrix)
