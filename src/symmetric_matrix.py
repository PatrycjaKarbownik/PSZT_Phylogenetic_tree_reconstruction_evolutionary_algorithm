# Implementation of symmetric matrix
# It is stored as one dimension array


class SymmetricMatrix:
    # TODO: swap columns and rows indexes
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
    def _get_index(self, key):
        column, row = key
        # Since (column, row) should have same value as (row, column), we want to operate on one of these
        if column > row:
            column, row = row, column
        index = (row * (row + 1) // 2) + column
        return index

    def get_max(self, availability):
        maximum = self._matrix[self._get_index((0, 1))]
        column_max = row_max = 0
        for row in range(self._size):
            if not availability[row]: continue
            for column in range(row + 1, self._size):
                if not availability[column]: continue
                value = self._matrix[self._get_index((column, row))]
                if maximum < value:
                    maximum = value
                    column_max = column
                    row_max = row
        # TODO: change order of returned variables if you changed indexes earlier
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


if __name__ == "__main__":
    matrix = SymmetricMatrix(4)
    print(matrix)
