"""
AP CSP 1.2.4 - Maze Creation with Doors and Barriers
Student: Alex Liao

This program creates a spiral maze with doors and barriers.
Doors provide openings in walls, barriers create perpendicular walls that block paths.

Pseudocode for adding barriers:
1. Draw part of the wall (10 pixels)
2. Create door opening (lift pen, move forward, put pen down)
3. Draw more wall (40 pixels past the door)
4. Turn left 90 degrees to draw perpendicular barrier
5. Draw barrier wall (twice the path width long)
6. Go back to original position
7. Turn right 90 degrees to continue original wall
8. Complete the rest of the wall

Question: Why is the barrier wall length twice the path width?
Answer: The barrier needs to span the entire width of the path. Since each wall
increases by one path width, and we have two parallel walls creating the path,
the total path width is effectively twice the path width increment. The barrier
must block the entire path, so it needs to be twice the path width long.

Question: Why not start the for loop at 4 instead of using an if statement?
Answer: Starting the for loop at 4 would mean skipping the first 4 iterations
entirely, which would prevent the walls from growing and scaling properly.
The first few walls are essential for establishing the maze structure and size.
We need the full sequence of wall growth to maintain the proper spiral geometry.
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
screen.title("Spiral Maze with Doors and Barriers")
screen.bgcolor("white")

def draw_spiral_maze_with_barriers():
    """
    Draws a spiral maze with doors and barriers.
    Doors provide openings, barriers create perpendicular blocking walls.
    Only draws barriers for walls 4 and beyond to avoid drawing errors.
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
        
        # Only add barriers for walls 4 and beyond
        # The first 4 walls are too small to accommodate both doors and barriers
        if k >= 16:  # 4 walls * 4 sides = 16 segments
            # Draw more wall (40 pixels past the door)
            maze_painter.forward(40)
            
            # Draw barrier wall (perpendicular to the main wall)
            maze_painter.left(90)  # Turn left to face perpendicular direction
            maze_painter.forward(PATH_WIDTH * 2)  # Draw barrier wall
            maze_painter.back(PATH_WIDTH * 2)  # Go back to original position
            maze_painter.right(90)  # Turn right to face original direction
            
            # Calculate remaining wall length
            remaining_length = length - 10 - (PATH_WIDTH * 2) - 40
        else:
            # For first 4 walls, just calculate remaining length without barrier
            remaining_length = length - 10 - (PATH_WIDTH * 2)
        
        # Draw the rest of the wall
        maze_painter.forward(remaining_length)
        
        maze_painter.left(90)
        # increase length after every 2 sides to keep spacing even
        if k % 2 == 1:
            length += PATH_WIDTH
    
    # Add the final line extending from the outermost square
    maze_painter.forward(PATH_WIDTH)

# Draw the maze with doors and barriers
draw_spiral_maze_with_barriers()

# Hide the turtle when done drawing
maze_painter.hideturtle()

# Keep the window open
turtle.mainloop()
