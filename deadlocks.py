def get_corner_deadlocks(puzzle):
    targets = set(puzzle.get_targets())
    board = puzzle.board
    rows = puzzle.rows
    cols = puzzle.cols

    def is_wall(r, c):
        if 0 <= r < rows and 0 <= c < cols:
            return board[r][c] == 'O'
        return True

    corners = set()
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O' or (r, c) in targets:
                continue
            n = is_wall(r - 1, c)
            s = is_wall(r + 1, c)
            w = is_wall(r, c - 1)
            e = is_wall(r, c + 1)
            if (n and w) or (n and e) or (s and w) or (s and e):
                corners.add((r, c))
    return corners


def get_line_deadlocks(puzzle, corners):
    targets = set(puzzle.get_targets())
    board = puzzle.board
    rows = puzzle.rows
    cols = puzzle.cols

    def is_wall(r, c):
        if 0 <= r < rows and 0 <= c < cols:
            return board[r][c] == 'O'
        return True

    lines = set()
    corner_list = list(corners)
    for i in range(len(corner_list)):
        for j in range(len(corner_list)):
            if i == j:
                continue
            r1, c1 = corner_list[i]
            r2, c2 = corner_list[j]

            if r1 == r2 and c1 < c2:
                segment = [(r1, c) for c in range(c1 + 1, c2)]
                if segment and all(board[r][c] != 'O' and (r, c) not in targets for r, c in segment):
                    north_wall = all(is_wall(r1 - 1, c) for c in range(c1, c2 + 1))
                    south_wall = all(is_wall(r1 + 1, c) for c in range(c1, c2 + 1))
                    if north_wall or south_wall:
                        lines.update(segment)

            if c1 == c2 and r1 < r2:
                segment = [(r, c1) for r in range(r1 + 1, r2)]
                if segment and all(board[r][c] != 'O' and (r, c) not in targets for r, c in segment):
                    west_wall = all(is_wall(r, c1 - 1) for r in range(r1, r2 + 1))
                    east_wall = all(is_wall(r, c1 + 1) for r in range(r1, r2 + 1))
                    if west_wall or east_wall:
                        lines.update(segment)

    return lines


def get_static_deadlocks(puzzle):
    corners = get_corner_deadlocks(puzzle)
    lines = get_line_deadlocks(puzzle, corners)
    return corners | lines


def is_deadlock(puzzle, static_deadlocks):
    for r, c in puzzle.get_unplaced_boxes():
        if (r, c) in static_deadlocks:
            return True
    return False
