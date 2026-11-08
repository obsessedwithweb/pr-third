import unittest
from levels import EXEMPLE_1_FIG7, EXEMPLE_2_FIG7
from model import SokobanPuzzle
from deadlocks import get_corner_deadlocks, get_line_deadlocks, get_static_deadlocks

class TestDeadlocks(unittest.TestCase):
    def test_figure7_example1_deadlocks(self):
        puzzle = SokobanPuzzle(EXEMPLE_1_FIG7)
        corners = get_corner_deadlocks(puzzle)
        lines = get_line_deadlocks(puzzle, corners)
        all_deadlocks = get_static_deadlocks(puzzle)

        expected_corners = {(1, 2), (1, 4), (1, 5), (5, 2), (5, 4), (5, 5)}
        expected_lines = {(2, 5), (3, 5), (4, 5)}

        self.assertEqual(corners, expected_corners)
        self.assertEqual(lines, expected_lines)
        self.assertEqual(all_deadlocks, expected_corners | expected_lines)

    def test_figure7_example2_deadlocks(self):
        puzzle = SokobanPuzzle(EXEMPLE_2_FIG7)
        corners = get_corner_deadlocks(puzzle)
        lines = get_line_deadlocks(puzzle, corners)
        all_deadlocks = get_static_deadlocks(puzzle)

        expected_corners = {(1, 4), (2, 6), (3, 1), (4, 4), (4, 6)}
        expected_lines = {(3, 6), (4, 5)}

        self.assertEqual(corners, expected_corners)
        self.assertEqual(lines, expected_lines)
        self.assertEqual(all_deadlocks, expected_corners | expected_lines)

if __name__ == '__main__':
    unittest.main()
