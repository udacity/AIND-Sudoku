from PySudoku import play


def visualize_assignments(assignments):
    """ Visualizes the set of assignments created by the Sudoku AI"""
    last_assignment = None
    filtered_assignments = []

    for i in range(len(assignments)):
        if last_assignment:
            last_assignment_items = [item for item in last_assignment.items() if len(item[1]) == 1]
            current_assignment_items = [item for item in assignments[i].items() if len(item[1]) == 1]
            shared_items = set(last_assignment_items) & set(current_assignment_items)
            if len(shared_items) < len(current_assignment_items):
                filtered_assignments.append(assignments[i])
        last_assignment = assignments[i]

    play(filtered_assignments)
