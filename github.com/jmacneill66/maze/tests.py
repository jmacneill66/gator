import unittest
from tkinter import Tk, BOTH, Canvas
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )


class TestMaze(unittest.TestCase):
    def test_break_entrance_and_exit(self):
        """Test that the entrance and exit walls are properly removed."""
        maze = Maze(0, 0, 5, 5, 40, 40)  # No Window for testing

        # Entrance (top-left) should have no top wall
        self.assertFalse(maze._cells[0][0].has_top_wall)

        # Exit (bottom-right) should have no bottom wall
        self.assertFalse(maze._cells[4][4].has_bottom_wall)

    def test_reset_cells_visited(self):
        """Test that cell visited attribute is reset to False after maze is drawn"""
        maze = Maze(0, 0, 5, 5, 40, 40)  # No Window for testing
        self.assertFalse(maze._cells[4][4].visited)
        self.assertFalse(maze._cells[0][0].visited)
        self.assertFalse(maze._cells[-1][-1].visited)


if __name__ == "__main__":
    unittest.main()
