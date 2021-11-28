from util import pad_matrix, sort


class IncrementalAssignmentAlgorithm(object):

    def __init__(self, values, solution):
        self.size = pad_matrix(values)
        self.values = values
        self.input_solution = solution
        self.steps = 0
        self.cache_hits = 0

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

            new_cur_a = (cur_assignment[0], open_assignment[1])
            prev_cur_a = (cur_assignment[0], cur_assignment[1])

            new_open_a = (open_assignment[0], cur_assignment[1])
            prev_open_a = (open_assignment[0], open_assignment[1])

            cur_a_delta = 0
            # New Assignment
            cur_a_delta += self.values[new_cur_a[0]][new_cur_a[1]]
            # Previous Assignment
            cur_a_delta -= self.values[prev_cur_a[0]][prev_cur_a[1]]

            open_a_delta = 0
            # New Assignment
            open_a_delta += self.values[new_open_a[0]][new_open_a[1]]
            # Previous Assignment
            open_a_delta -= self.values[prev_open_a[0]][prev_open_a[1]]

            if open_a_delta > cur_a_delta:
                pass

            a = assignments.copy()
            a.remove(prev_cur_a)

            optimal_assignment, delta = self.recursive_reassign(a, new_open_a)
            if max_delta > cur_a_delta + open_a_delta + delta:
                max_delta = cur_a_delta + open_a_delta + delta
                max_assignments = optimal_assignment + [new_cur_a]

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
            # spacer = []
            for col in range(0, self.size):
                # spacer.append('---')
                if (row, col) in assignments:
                    formatted_row.append(f'[{self.values[row][col]}]')
                elif (row, col) == open_a:
                    formatted_row.append(f'({self.values[row][col]})')
                else:
                    formatted_row.append(f' {self.values[row][col]} ')

            # print(''.join(spacer))
            print(''.join(formatted_row))

        print(f'------------------------------------------------')
        print(f'------------------------------------------------')
