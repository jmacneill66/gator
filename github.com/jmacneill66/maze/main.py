from tkinter import Tk, BOTH, Canvas
from window import *
from line import *
from cell import *
from maze import *


def main():
    win = Window(1250, 950)
    """
    # Create some Line objects
     line1 = Line(50, 50, 200, 50)
     line2 = Line(50, 100, 200, 150)
     line3 = Line(100, 200, 300, 250)

    #Draw the lines on the window
    win.draw_line(line1, "red")
    win.draw_line(line2, "blue")
    win.draw_line(line3, "green")

    # Create some Cell objects with different wall configurations
    cell1 = Cell(50, 50, 100, 100, win)  # Full walls
    cell2 = Cell(110, 50, 160, 100, win)  # No left wall
    cell3 = Cell(50, 110, 100, 160, win)  # No top wall
    cell4 = Cell(110, 110, 160, 160, win)  # No bottom wall

    # Modify walls
    cell2.has_left_wall = False
    cell3.has_top_wall = False
    cell4.has_bottom_wall = False

    # Draw cells
    cell1.draw()
    cell2.draw()
    cell3.draw()
    cell4.draw()

    # Draw paths between cells
    cell1.draw_move(cell2)  # Path from cell1 to cell2
    cell1.draw_move(cell3)  # Path from cell1 to cell3
    """
    # Create a Maze object with 35 rows, 45 cols starting at (60,25) on canvas, with cell width 25)
    maze = Maze(60, 25, 35, 45, 25, 25, win)

    # Solve the maze!
    maze.solve()

    # Wait for user to close the window
    win.wait_for_close()


if __name__ == "__main__":
    main()
