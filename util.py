

def pad_matrix(matrix):
    if not isinstance(matrix, list):
        raise Exception('Values input has to be a list of integer lists')

    size = len(matrix)
    for row in matrix:
        if len(row) > size:
            size = len(row)

        for col in row:
            if not isinstance(col, int):
                raise Exception('All row values have to be integers.')

    [matrix.append([]) for _ in range(len(matrix), size)]
    [row.append(0) for row in matrix for _ in range(len(row), size)]

    return size


def sort(solution):
    def row(x):
        return x[0]

    solution.sort(key=row)

    return solution
