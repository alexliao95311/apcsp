"""
AP CSP 1.2.4 - Maze Creation
Student: Alex Liao

This program creates a spiral maze foundation using turtle graphics.
The maze consists of concentric squares that create a spiral pattern.

Pseudocode for square spiral:
1. Decide on number of walls for the spiral
2. Start from center and work out
3. Use a for loop and the range function
4. On each iteration, turn your turtle and grow the size of the wall
5. Don't forget to include mainloop to control the screen
"""

import turtle

# Configuration variables - these control the maze appearance
# Avoiding "magic numbers" by using named variables
NUM_WALLS = 8  # Number of walls in the spiral
PATH_WIDTH = 20  # Distance between walls (width of the path)
WALL_COLOR = "black"  # Color for the maze walls

# Create the turtle for drawing the maze
maze_painter = turtle.Turtle()
maze_painter.speed(0)  # Fastest drawing speed
maze_painter.color(WALL_COLOR)
maze_painter.pensize(2)

# Create the screen
screen = turtle.Screen()
screen.title("Spiral Maze Foundation")
screen.bgcolor("white")

def draw_spiral_maze():
    """
    Draws a spiral maze using a continuous path.
    Creates a proper spiral by drawing each wall segment sequentially.
    """
    # Start near the center so the spiral grows out nicely
    start_offset = PATH_WIDTH / 2
    maze_painter.penup()
    maze_painter.goto(-start_offset, -start_offset)
    maze_painter.setheading(0)
    maze_painter.pendown()
    
    length = PATH_WIDTH  # first segment length
    segments = NUM_WALLS * 4 + 1   # enough segments to create NUM_WALLS of growth and a tail
    
    for k in range(segments):
        maze_painter.forward(length)
        maze_painter.left(90)
        # increase length after every 2 sides to keep spacing even
        if k % 2 == 1:
            length += PATH_WIDTH
    
    # Add the final line extending from the outermost square
    maze_painter.forward(PATH_WIDTH)

# Draw the maze
draw_spiral_maze()

# Hide the turtle when done drawing
maze_painter.hideturtle()

# Keep the window open
turtle.mainloop()
