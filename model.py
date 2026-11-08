class SokobanPuzzle:
    MOVES = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1)
    }

    def __init__(self, board):
        if isinstance(board, list):
            self.board = [list(row) for row in board]
        else:
            self.board = [list(line) for line in board.strip().split('\n')]
        self.rows = len(self.board)
        self.cols = max(len(row) for row in self.board)
        for row in self.board:
            if len(row) < self.cols:
                row.extend(['O'] * (self.cols - len(row)))

    def findPlayer(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] in ('R', '.'):
                    return r, c
        raise ValueError("Player not found")

    def get_boxes(self):
        boxes = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] in ('B', '*'):
                    boxes.append((r, c))
        return boxes

    def get_unplaced_boxes(self):
        boxes = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'B':
                    boxes.append((r, c))
        return boxes

    def get_targets(self):
        targets = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] in ('S', '.', '*'):
                    targets.append((r, c))
        return targets

    def isGoal(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'B':
                    return False
        return True

    def successorFunction(self):
        successors = []
        p_row, p_col = self.findPlayer()
        p_char = self.board[p_row][p_col]

        for action, (dr, dc) in self.MOVES.items():
            new_r, new_c = p_row + dr, p_col + dc
            if not (0 <= new_r < self.rows and 0 <= new_c < self.cols):
                continue

            target_cell = self.board[new_r][new_c]

            if target_cell in (' ', 'S'):
                new_board = [row[:] for row in self.board]
                new_board[p_row][p_col] = 'S' if p_char == '.' else ' '
                new_board[new_r][new_c] = '.' if target_cell == 'S' else 'R'
                successors.append((action, SokobanPuzzle(new_board)))

            elif target_cell in ('B', '*'):
                box_next_r, box_next_c = new_r + dr, new_c + dc
                if 0 <= box_next_r < self.rows and 0 <= box_next_c < self.cols:
                    box_dest_cell = self.board[box_next_r][box_next_c]
                    if box_dest_cell in (' ', 'S'):
                        new_board = [row[:] for row in self.board]
                        new_board[p_row][p_col] = 'S' if p_char == '.' else ' '
                        new_board[new_r][new_c] = '.' if target_cell == '*' else 'R'
                        new_board[box_next_r][box_next_c] = '*' if box_dest_cell == 'S' else 'B'
                        successors.append((action, SokobanPuzzle(new_board)))

        return successors

    def to_tuple(self):
        return tuple(tuple(row) for row in self.board)

    def __eq__(self, other):
        return isinstance(other, SokobanPuzzle) and self.to_tuple() == other.to_tuple()

    def __hash__(self):
        return hash(self.to_tuple())


class Node:
    def __init__(self, state, parent=None, action=None, step_cost=1):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = 0 if parent is None else parent.g + step_cost
        self.f = 0
        self.h = 0

    def setF(self, heuristic_val):
        self.h = heuristic_val
        self.f = self.g + heuristic_val

    def getPath(self):
        path = []
        curr = self
        while curr is not None:
            path.append(curr.state)
            curr = curr.parent
        path.reverse()
        return path

    def getSolution(self):
        actions = []
        curr = self
        while curr.parent is not None:
            actions.append(curr.action)
            curr = curr.parent
        actions.reverse()
        return actions

    def __lt__(self, other):
        return self.f < other.f
