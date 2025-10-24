"""
AP CSP 1.2.4 - Maze Creation with Random Doors and Barriers
Student: Alex Liao

This program creates a spiral maze with randomly placed doors and barriers.
Doors and barriers are positioned randomly on each wall to create a more realistic maze.

Pseudocode for randomizing door and barrier locations:
1. Import random module
2. For each wall, generate random positions for door and barrier
3. Ensure door and barrier don't overlap (distance >= path width)
4. Determine which comes first (door or barrier)
5. Draw wall segments in correct order to avoid backtracking
6. Use selection statements to handle different drawing sequences

Question: Why do we need to ensure door and barrier don't overlap?
Answer: If a barrier renders inside a door opening, it defeats the purpose
of the door and creates visual confusion. The barrier should block the path,
not be inside an opening.

Question: Why is it important to draw door and barrier in the correct order?
Answer: Drawing them in order prevents the turtle from having to backtrack
and redraw portions of the wall, which is inefficient and can cause visual
artifacts. We want to draw each segment only once in the correct sequence.
"""

import turtle
import random

# Configuration variables - these control the maze appearance
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
screen.title("Random Spiral Maze with Doors and Barriers")
screen.bgcolor("white")

def draw_spiral_maze_random():
    """
    Draws a spiral maze with randomly placed doors and barriers.
    Each wall has a door and barrier positioned randomly to create variety.
    Uses selection logic to determine drawing order and prevent overlaps.
    """
    # Start from the center and work outward
    current_size = PATH_WIDTH
    
    # Draw the spiral using a for loop
    for i in range(NUM_WALLS):
        # Calculate wall length for this iteration
        wall_len = current_size
        
        # Draw one complete square for each wall
        for side in range(4):
            # Generate random positions for door and barrier
            # Ensure they're not too close to the beginning or end of the wall
            door = random.randint(PATH_WIDTH * 2, wall_len - PATH_WIDTH * 2)
            barrier = random.randint(PATH_WIDTH * 2, wall_len - PATH_WIDTH * 2)
            
            # Ensure door and barrier don't overlap
            # If they're too close, generate new random positions
            while abs(door - barrier) < PATH_WIDTH * 2:
                # Regenerate barrier position to avoid overlap
                barrier = random.randint(PATH_WIDTH * 2, wall_len - PATH_WIDTH * 2)
            
            # Only add barriers for walls 4 and beyond (avoid drawing errors on small walls)
            if i >= 4:
                # Determine which comes first: door or barrier
                if door < barrier:
                    # Door comes first
                    # Draw wall segment before door
                    maze_painter.forward(door)
                    
                    # Draw door opening
                    maze_painter.penup()
                    maze_painter.forward(PATH_WIDTH * 2)
                    maze_painter.pendown()
                    
                    # Draw wall segment between door and barrier
                    maze_painter.forward(barrier - door - (PATH_WIDTH * 2))
                    
                    # Draw barrier
                    maze_painter.left(90)
                    maze_painter.forward(PATH_WIDTH * 2)
                    maze_painter.back(PATH_WIDTH * 2)
                    maze_painter.right(90)
                    
                    # Draw remaining wall segment
                    remaining_length = wall_len - barrier
                    maze_painter.forward(remaining_length)
                    
                else:
                    # Barrier comes first
                    # Draw wall segment before barrier
                    maze_painter.forward(barrier)
                    
                    # Draw barrier
                    maze_painter.left(90)
                    maze_painter.forward(PATH_WIDTH * 2)
                    maze_painter.back(PATH_WIDTH * 2)
                    maze_painter.right(90)
                    
                    # Draw wall segment between barrier and door
                    maze_painter.forward(door - barrier)
                    
                    # Draw door opening
                    maze_painter.penup()
                    maze_painter.forward(PATH_WIDTH * 2)
                    maze_painter.pendown()
                    
                    # Draw remaining wall segment
                    remaining_length = wall_len - door - (PATH_WIDTH * 2)
                    maze_painter.forward(remaining_length)
            else:
                # For first 4 walls, only draw door (no barrier to avoid errors)
                # Draw wall segment before door
                maze_painter.forward(door)
                
                # Draw door opening
                maze_painter.penup()
                maze_painter.forward(PATH_WIDTH * 2)
                maze_painter.pendown()
                
                # Draw remaining wall segment
                remaining_length = wall_len - door - (PATH_WIDTH * 2)
                maze_painter.forward(remaining_length)
            
            # Turn to next side of the square
            maze_painter.left(90)
        
        # After each square, increase the size for the next iteration
        current_size += PATH_WIDTH
        
        # Turn to create the spiral pattern
        maze_painter.left(90)

# Draw the maze with random doors and barriers
draw_spiral_maze_random()

# Hide the turtle when done drawing
maze_painter.hideturtle()

# Keep the window open
turtle.mainloop()
