"""
AP CSP 1.2.4 - Maze Creation with Doors
Student: Alex Liao

This program creates a spiral maze with doors (openings) in the walls.
Doors are placed at the same location on each wall for simplicity.

Pseudocode for adding doors:
1. Draw part of the wall (10 pixels)
2. Lift the pen to create an opening
3. Move forward by twice the path width (door opening size)
4. Put the pen down to continue drawing the wall
5. Complete the rest of the wall

Question: Why is the door opening twice the path width?
Answer: The door opening should match the width of the path between walls.
Since paths are created by the space between parallel walls, and each wall
grows by one path width, the total path width is effectively twice the
increment value. This ensures the door is wide enough for navigation.
"""

import turtle

# Configuration variables - these control the maze appearance
NUM_WALLS = 8  # Number of walls in the spiral
PATH_WIDTH = 40  # Distance between walls (width of the path)
WALL_COLOR = "black"  # Color for the maze walls

# Create the turtle for drawing the maze
maze_painter = turtle.Turtle()
maze_painter.speed(0)  # Fastest drawing speed
maze_painter.color(WALL_COLOR)
maze_painter.pensize(2)

# Create the screen
screen = turtle.Screen()
screen.title("Spiral Maze with Doors")
screen.bgcolor("white")

def draw_spiral_maze_with_doors():
    """
    Draws a spiral maze with doors in each wall.
    Each door is placed 10 pixels from the start of each wall side.
    The door opening is twice the path width to match the path size.
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
        # Draw first part of wall (10 pixels before door)
        maze_painter.forward(10)
        
        # Create door opening
        maze_painter.penup()  # Lift pen to stop drawing
        maze_painter.forward(PATH_WIDTH * 2)  # Move forward without drawing (door opening)
        maze_painter.pendown()  # Put pen down to continue drawing
        
        # Draw the rest of the wall
        remaining_length = length - 10 - (PATH_WIDTH * 2)
        maze_painter.forward(remaining_length)
        
        maze_painter.left(90)
        # increase length after every 2 sides to keep spacing even
        if k % 2 == 1:
            length += PATH_WIDTH
    
    # Add the final line extending from the outermost square
    maze_painter.forward(PATH_WIDTH)

# Draw the maze with doors
draw_spiral_maze_with_doors()

# Hide the turtle when done drawing
maze_painter.hideturtle()

# Keep the window open
turtle.mainloop()
