from util import pad_matrix


class IncrementalAssignmentAlgorithm(object):

    def __init__(self, values, solution):
        self.size = pad_matrix(values)
        self.values = values
        self.input_solution = solution
        self.steps = 0

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

        new_assignments = self.recursive_reassign(self.input_solution, open_assignment)

        print(' ')
        print(' ')
        print(f'Algorithm Returned in {self.steps} steps')
        print(f'Final Assignment:')
        print(' ')
        self.print_assignment(new_assignments, None)

        return new_assignments, self.size, self.steps

    def recursive_reassign(self, assignments, open_assignment):
        self.print_assignment(assignments, open_assignment)

        greates_value_increase = 0
        swap = None

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

            if cur_a_delta + open_a_delta > greates_value_increase:
                greates_value_increase = cur_a_delta + open_a_delta

                if cur_a_delta > open_a_delta:
                    swap = (new_cur_a, prev_cur_a, new_open_a)  # add, remove, new_open

                elif open_a_delta > cur_a_delta:
                    swap = (new_open_a, prev_cur_a, new_cur_a)  # add, remove, new_open

                else:
                    swap = (new_open_a, prev_cur_a, new_cur_a)  # add, remove, new_open

        if swap is not None:
            # We shouldn't have to recalculate the value delta for reversing the swap that we just did.
            # So, would it be fair to just remove the new assignment as long as the cur and open delta are not equal?
            assignments.append(swap[0])
            assignments.remove(swap[1])

            return self.recursive_reassign(assignments, swap[2])
        else:
            return assignments + [open_assignment]

    def print_assignment(self, assignments, open_a):

        print(f'------------------------------------------------')
        print(f'Assignments: {assignments}')
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
