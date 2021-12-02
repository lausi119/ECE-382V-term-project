import json
import random


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


def write_to_csv(data, idx):
    with open(f'output_{idx}.csv', 'a') as f:
        for row in data:
            f.write(','.join(row) + '\n')


def sort(solution):
    def row(x):
        return x[0]

    solution.sort(key=row)

    return solution


def load_tests_from_file():
    with open('tests.json', 'r') as f:
        return json.load(f)


def generate_random_test(min_size=4, max_size=10, val_range=9, num_tests=1):
    from munkres import Munkres

    examples = []
    m = Munkres()
    for idx in range(min_size, max_size + 1):
        size = idx  # random.randint(min_size, max_size)
        for _ in range(0, num_tests):
            examples.append(_generate_random_test(m, val_range, size))

    return examples


def _generate_random_test(m, val_range, size):

    matrix = [[random.randint(0, val_range) for _ in range(0, size)] for _ in range(0, size)]
    solution = m.compute(matrix)

    # Adding the incremental
    [row.append(random.randint(0, val_range)) for row in matrix]
    matrix.append([random.randint(0, val_range) for _ in range(0, size + 1)])

    return {'values': matrix, 'solution': solution}


def validate_result(values, assignments):
    from munkres import Munkres

    m = Munkres()
    solution = m.compute(values)

    munkres_total = 0
    for a in solution:
        munkres_total += values[a[0]][a[1]]

    incremental_total = 0
    for a in assignments:
        incremental_total += values[a[0]][a[1]]

    # print('Validating:')
    # print(f'Munkres:     {munkres_total}, {sort(solution)}')
    # print(f'Incremental: {incremental_total}, {sort(assignments)}')
    # print(values)

    return incremental_total == munkres_total, incremental_total, munkres_total


def run_example(example, i):

    output_assignments, size, steps, cache_hits = IncrementalAssignmentAlgorithm(
        example['values'],
        # Couldn't load tuples from the JSON file but I am too lazy to use arrays instead,
        # so im just casting all the solution arrays from the json to tuples here
        [(a[0], a[1]) for a in example['solution']],
        i  # True if str(args.exhaustive).lower() in ('true', 't') else False
    ).run()

    return validate_result(example['values'], output_assignments)
