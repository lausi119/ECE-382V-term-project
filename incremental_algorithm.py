from util import pad_matrix, sort


class IncrementalAssignmentAlgorithm(object):

    def __init__(self, values, solution, exhaustive=False):
        self.size = pad_matrix(values)
        self.values = values
        self.input_solution = solution
        self.steps = 0
        self.cache_hits = 0
        self.exhaustive = exhaustive

        self._cache = {}

    def run(self):
        row_idxs = []
        col_idxs = []
        for x in range(0, self.size):
            row_idxs.append(x)
            col_idxs.append(x)

        initial_value = 0
        for x in self.input_solution:
            initial_value += self.values[x[0]][x[1]]
            row_idxs.remove(x[0])
            col_idxs.remove(x[1])

        open_assignment = (row_idxs[0], col_idxs[0])

        self.print_assignment(self.input_solution, open_assignment)
        new_assignments, delta = self.recursive_reassign(self.input_solution, open_assignment)

        print(' ')
        print(f'Solution: {self.input_solution}')
        print(f'Algorithm Returned in {self.steps} steps with a {delta} delta and {self.cache_hits} cache hits')
        print(f'Final Assignment:')
        print(' ')
        self.print_assignment(new_assignments, None)

        return new_assignments, self.size, self.steps, self.cache_hits

    def recursive_reassign(self, assignments, open_assignment):

        hash_key = str(hash(str(sort(assignments)))) + str(open_assignment)
        if hash_key in self._cache:
            self.cache_hits += 1
            return self._cache[hash_key]

        max_delta = 0
        max_assignments = None

        for cur_assignment in assignments:
            self.steps += 1

            updated_cur_assignment = (cur_assignment[0], open_assignment[1])
            updated_open_assignment = (open_assignment[0], cur_assignment[1])
            # updated_cur_assignment = (open_assignment[0], cur_assignment[1])
            # updated_open_assignment = (cur_assignment[0], open_assignment[1])

            cur_assignment_delta = (
                2 * self.values[updated_cur_assignment[0]][updated_cur_assignment[1]]
                - self.values[cur_assignment[0]][cur_assignment[1]]
                - self.values[open_assignment[0]][open_assignment[1]]
            )
            open_assignment_delta = (
                    2 * self.values[updated_open_assignment[0]][updated_open_assignment[1]]
                    - self.values[cur_assignment[0]][cur_assignment[1]]
                    - self.values[open_assignment[0]][open_assignment[1]]
            )

            if self.exhaustive:
                a = assignments.copy()
                a.remove(cur_assignment)
                optimal_assignment, delta = self.recursive_reassign(a, updated_cur_assignment)
                delta += cur_assignment_delta + open_assignment_delta
                if max_delta > delta:
                    max_delta = delta
                    max_assignments = optimal_assignment + [updated_open_assignment]

            elif open_assignment_delta < 0:
                a = assignments.copy()
                a.remove(cur_assignment)
                optimal_assignment, delta = self.recursive_reassign(a, updated_cur_assignment)
                delta += cur_assignment_delta + open_assignment_delta
                if max_delta > delta:
                    max_delta = delta
                    max_assignments = optimal_assignment + [updated_open_assignment]

            elif cur_assignment_delta < 0:
                a = assignments.copy()
                a.remove(cur_assignment)
                optimal_assignment, delta = self.recursive_reassign(a, updated_open_assignment)
                delta += cur_assignment_delta + open_assignment_delta
                if max_delta > delta:
                    max_delta = delta
                    max_assignments = optimal_assignment + [updated_cur_assignment]

        if max_assignments:
            self._cache[hash_key] = max_assignments, max_delta
            return max_assignments, max_delta
        else:
            self._cache[hash_key] = assignments + [open_assignment], 0
            return assignments + [open_assignment], 0

    def print_assignment(self, assignments, open_a):

        print(f'------------------------------------------------')
        print(f'Assignments: {assignments}, {open_a}')
        print(f'------------------------------------------------')

        for row in range(0, self.size):
            formatted_row = []
            for col in range(0, self.size):

                if (row, col) in assignments:
                    formatted_row.append(f'[{self.values[row][col]:0>2}]')
                elif (row, col) == open_a:
                    formatted_row.append(f'({self.values[row][col]:0>2})')
                else:
                    formatted_row.append(f' {self.values[row][col]:0>2} ')

            print(''.join(formatted_row))

        print(f'------------------------------------------------')
        print(f'------------------------------------------------')
