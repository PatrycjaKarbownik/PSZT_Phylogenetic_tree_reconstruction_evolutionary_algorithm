# Implementation of symmetric matrix


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

    def _get_index(self, key):
        column, row = key
        if column > row:
            column, row = row, column
        index = (row * (row + 1) // 2) + column
        return index


if __name__ == "__main__":
    matrix = SymmetricMatrix(4)
    for x in range(4):
        for y in range(4):
            print(str(matrix[x, y]) + " ", end='')
        print()

        print()