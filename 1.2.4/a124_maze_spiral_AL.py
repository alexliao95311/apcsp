"""
AP CSP 1.2.4 - Maze Creation
Student: Alex Liao

This program creates a spiral maze foundation using turtle graphics.
The maze consists of concentric squares that create a spiral pattern.

Pseudocode for square spiral:
1. Decide on number of walls for the spiral
2. Start from center and work outward
3. Use for loop with range function since we know iteration count
4. On each iteration: turn turtle and grow wall size
5. Include mainloop to control screen
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
    Draws a spiral maze using concentric squares.
    Each iteration creates a square that's larger than the previous one.
    The squares are rotated to create a spiral effect.
    """
    # Start from the center and work outward
    current_size = PATH_WIDTH
    
    # Draw the spiral using a for loop
    # We know how many iterations we need, so for loop is appropriate
    for i in range(NUM_WALLS):
        # Draw one complete square for each wall
        for side in range(4):
            maze_painter.forward(current_size)
            maze_painter.left(90)
        
        # After each square, increase the size for the next iteration
        # This creates the growing spiral effect
        current_size += PATH_WIDTH
        
        # Turn to create the spiral pattern
        # This rotation creates the offset between squares
        maze_painter.left(90)

# Draw the maze
draw_spiral_maze()

# Hide the turtle when done drawing
maze_painter.hideturtle()

# Keep the window open
turtle.mainloop()
