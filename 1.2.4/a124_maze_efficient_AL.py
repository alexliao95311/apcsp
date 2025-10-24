"""
AP CSP 1.2.4 - Efficient Maze Creation with Functions
Student: Alex Liao

This program creates a spiral maze with randomly placed doors and barriers,
using functions to eliminate code duplication and improve efficiency.

Key improvements:
- Functions for drawing doors and barriers to eliminate redundant code
- Better code organization and reusability
- Cleaner, more maintainable code structure

Question: Why is code duplication considered poor programming practice?
Answer: Code duplication makes programs harder to maintain, increases the
chance of bugs, and violates the DRY (Don't Repeat Yourself) principle.
When you need to fix a bug or make a change, you have to remember to
update it in multiple places, which is error-prone.

Question: How do functions with parameters help eliminate redundancy?
Answer: Functions allow us to write an algorithm once and reuse it with
different values (parameters). Instead of writing similar code multiple
times with different values, we create one function and call it with
the appropriate parameters each time.
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
screen.title("Efficient Random Spiral Maze")
screen.bgcolor("white")

def draw_door():
    """
    Draws a door opening in the wall.
    Lifts the pen, moves forward to create an opening, then puts pen down.
    """
    maze_painter.penup()
    maze_painter.forward(PATH_WIDTH * 2)
    maze_painter.pendown()

def draw_barrier():
    """
    Draws a barrier wall perpendicular to the main wall.
    The barrier spans the width of the path to block navigation.
    """
    maze_painter.left(90)
    maze_painter.forward(PATH_WIDTH * 2)
    maze_painter.back(PATH_WIDTH * 2)
    maze_painter.right(90)

def draw_wall_segment(length):
    """
    Draws a wall segment of the specified length.
    
    Parameters:
    length (int): The length of the wall segment to draw
    """
    maze_painter.forward(length)

def draw_spiral_maze_efficient():
    """
    Draws a spiral maze with randomly placed doors and barriers using functions.
    Eliminates code duplication by using reusable functions for common operations.
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
                    draw_wall_segment(door)
                    
                    # Draw door opening using function
                    draw_door()
                    
                    # Draw wall segment between door and barrier
                    draw_wall_segment(barrier - door - (PATH_WIDTH * 2))
                    
                    # Draw barrier using function
                    draw_barrier()
                    
                    # Draw remaining wall segment
                    remaining_length = wall_len - barrier
                    draw_wall_segment(remaining_length)
                    
                else:
                    # Barrier comes first
                    # Draw wall segment before barrier
                    draw_wall_segment(barrier)
                    
                    # Draw barrier using function
                    draw_barrier()
                    
                    # Draw wall segment between barrier and door
                    draw_wall_segment(door - barrier)
                    
                    # Draw door opening using function
                    draw_door()
                    
                    # Draw remaining wall segment
                    remaining_length = wall_len - door - (PATH_WIDTH * 2)
                    draw_wall_segment(remaining_length)
            else:
                # For first 4 walls, only draw door (no barrier to avoid errors)
                # Draw wall segment before door
                draw_wall_segment(door)
                
                # Draw door opening using function
                draw_door()
                
                # Draw remaining wall segment
                remaining_length = wall_len - door - (PATH_WIDTH * 2)
                draw_wall_segment(remaining_length)
            
            # Turn to next side of the square
            maze_painter.left(90)
        
        # After each square, increase the size for the next iteration
        current_size += PATH_WIDTH
        
        # Turn to create the spiral pattern
        maze_painter.left(90)

# Draw the maze with random doors and barriers using efficient functions
draw_spiral_maze_efficient()

# Hide the turtle when done drawing
maze_painter.hideturtle()

# Keep the window open
turtle.mainloop()
