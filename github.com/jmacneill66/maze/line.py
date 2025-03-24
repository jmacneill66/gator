import tkinter as tk


class Line:
    def __init__(self, x1, y1, x2, y2):
        """Initialize a line with two points."""
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas, fill_color):
        """Draw the line on the given canvas with the specified fill color."""
        canvas.create_line(self.x1, self.y1, self.x2,
                           self.y2, fill=fill_color, width=2)
