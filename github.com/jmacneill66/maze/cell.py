import tkinter as tk
import random


class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        """Initialize a cell with walls and position on the canvas. """
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False  # Track if this cell has been processed

        self._x1 = x1  # x1y1 = top left, x2y2 = bottom right
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        # Reference to the Window object (optional for testing)
        self._win = win

    def draw(self):
        """Draw the cell walls, and remove walls visually if they no longer exist."""
        if not self._win:
            return  # Skip drawing if no window is available

        background_color = "#d9d9d9"  # Default background color

        if self.has_left_wall:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x1, self._y2, fill="black", width=2)
        else:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x1, self._y2, fill=background_color, width=2)

        if self.has_right_wall:
            self._win.canvas.create_line(
                self._x2, self._y1, self._x2, self._y2, fill="black", width=2)
        else:
            self._win.canvas.create_line(
                self._x2, self._y1, self._x2, self._y2, fill=background_color, width=2)

        if self.has_top_wall:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x2, self._y1, fill="black", width=2)
        else:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x2, self._y1, fill=background_color, width=2)

        if self.has_bottom_wall:
            self._win.canvas.create_line(
                self._x1, self._y2, self._x2, self._y2, fill="black", width=2)
        else:
            self._win.canvas.create_line(
                self._x1, self._y2, self._x2, self._y2, fill=background_color, width=2)

    def draw_move(self, to_cell, undo=False):
        """Draw a path from this cell to another cell."""
        # Calculate center points of both cells
        x1, y1 = (self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2
        x2, y2 = (to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 +
                                                    to_cell._y2) // 2

        color = "white" if undo else "red"  # Erase if undoing, otherwise draw
        self._win.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
