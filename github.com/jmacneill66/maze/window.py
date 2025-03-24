from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        # Create the root window
        self.__root = Tk()
        self.__root.title("My Window")  # Set title

        # Set window size
        self.__root.geometry(f"{width}x{height}")

        # Create a Canvas widget and add it to the window
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)  # Fill entire window

        # Flag to track if the window is running
        self.running = False

        # Bind the close event to the close() method
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        """Redraws the window by updating idle tasks and rendering the frame."""
        self.__root.update_idletasks()  # Processes events like resizing, minimizing, etc.
        self.__root.update()  # Redraws the window

    def wait_for_close(self):
        """Keeps redrawing the window until it is closed."""
        self.running = True  # Set running state to True
        while self.running:
            self.redraw()  # Keep updating the window

    def close(self):
        """Handles window closing event."""
        self.running = False  # Stop the loop
        self.__root.destroy()  # Close the window

    def draw_line(self, line, fill_color):
        """Draw a Line object onto the canvas."""
        line.draw(self.canvas, fill_color)
