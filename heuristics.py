def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def count_unplaced_boxes(puzzle):
    return len(puzzle.get_unplaced_boxes())


def h1(puzzle):
    return count_unplaced_boxes(puzzle)


def h2(puzzle):
    unplaced = count_unplaced_boxes(puzzle)
    boxes = puzzle.get_boxes()
    targets = puzzle.get_targets()
    if not targets or not boxes:
        return 0
    manhattan_sum = 0
    for b in boxes:
        min_dist = min(manhattan_distance(b, s) for s in targets)
        manhattan_sum += min_dist
    return 2 * unplaced + manhattan_sum


def h3(puzzle):
    unplaced = count_unplaced_boxes(puzzle)
    if unplaced == 0:
        return 0
    base_h2 = h2(puzzle)
    p_row, p_col = puzzle.findPlayer()
    unplaced_boxes = puzzle.get_unplaced_boxes()
    if not unplaced_boxes:
        return base_h2
    min_robot_dist = min(manhattan_distance((p_row, p_col), b) for b in unplaced_boxes)
    robot_penalty = max(0, min_robot_dist - 1)
    return base_h2 + robot_penalty
