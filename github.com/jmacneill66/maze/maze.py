from tkinter import Tk, BOTH, Canvas
from cell import *
import time
import random


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        """Initialize the maze with a grid of cells."""
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win  # Reference to the Window object
        self._cells = []  # 2D grid of Cell objects
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.solve()
        self._solve_r(0, 0)

    def _create_cells(self):
        """Create a grid of Cell objects and draw them."""
        for i in range(self.num_cols):
            col = []
            for j in range(self.num_rows):
                x1 = self.x1 + i * self.cell_size_x
                y1 = self.y1 + j * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y
                cell = Cell(x1, y1, x2, y2, self.win)
                col.append(cell)
            self._cells.append(col)

        # Draw all cells
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        """Draw the cell at grid position (i, j)."""
        if not self.win:
            return  # Skip drawing if no window is available
        self._cells[i][j].draw()
        self._animate()

    def _break_entrance_and_exit(self):
        """Remove the entrance (top of top-left cell) and exit (bottom of bottom-right cell)."""
        if self.num_cols > 0 and self.num_rows > 0:
            # Remove the top wall of the entrance cell
            self._cells[0][0].has_top_wall = False
            self._draw_cell(0, 0)

            # Remove the bottom wall of the exit cell
            self._cells[self.num_cols - 1][self.num_rows -
                                           1].has_bottom_wall = False
            self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i, j):
        """Recursive depth-first maze generation algorithm."""
        self._cells[i][j].visited = True  # Mark current cell as visited

        while True:
            neighbors = []

            # Check all possible directions
            if i > 0 and not self._cells[i - 1][j].visited:  # Left
                neighbors.append(("left", i - 1, j))
            # Right
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                neighbors.append(("right", i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:  # Up
                neighbors.append(("up", i, j - 1))
            # Down
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                neighbors.append(("down", i, j + 1))

            if not neighbors:
                self._draw_cell(i, j)  # Draw the current cell before returning
                return

            # Pick a random neighbor (pick a random tuple)
            chosen = random.choice(neighbors)
            direction = chosen[0]
            ni = chosen[1]
            nj = chosen[2]

            # Break the wall between current cell and chosen neighbor
            if direction == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[ni][nj].has_right_wall = False
            elif direction == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[ni][nj].has_left_wall = False
            elif direction == "up":
                self._cells[i][j].has_top_wall = False
                self._cells[ni][nj].has_bottom_wall = False
            elif direction == "down":
                self._cells[i][j].has_bottom_wall = False
                self._cells[ni][nj].has_top_wall = False

            # Move to the chosen cell recursively
            self._break_walls_r(ni, nj)

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                # Reset current cell as not visited
                self._cells[i][j].visited = False

    def solve(self):
        """Solve the maze using depth-first search."""
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        """Recursive depth-first search to solve the maze."""
        self._animate()  # Visualize the process
        cell = self._cells[i][j]
        cell.visited = True  # Mark as visited

        # If we reach the goal (bottom-right cell), we're done!
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # Possible movements: left, right, up, down
        moves = [
            ("left", i - 1, j, cell.has_left_wall),
            ("right", i + 1, j, cell.has_right_wall),
            ("up", i, j - 1, cell.has_top_wall),
            ("down", i, j + 1, cell.has_bottom_wall),
        ]

        for direction, ni, nj, wall in moves:
            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows:
                next_cell = self._cells[ni][nj]
                if not wall and not next_cell.visited:
                    # Move and draw
                    cell.draw_move(next_cell)
                    if self._solve_r(ni, nj):
                        return True
                    # Backtrack if not a valid path
                    cell.draw_move(next_cell, undo=True)

        return False  # No solution found from this path

    def _animate(self):
        """Redraw the canvas with a slight delay to visualize drawing."""
        if not self.win:
            return  # Skip drawing if no window is available
        self.win.redraw()
        time.sleep(0.0001)
