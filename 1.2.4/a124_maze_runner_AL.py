"""
AP CSP 1.2.4 - Maze with Runner
Student: Alex Liao

This program creates a spiral maze with a controllable turtle runner.
The maze runner can be controlled with arrow keys and moves with the 'g' key.

Features implemented:
- Random maze generation with doors and barriers
- Controllable maze runner with keyboard input
- Customizable runner appearance and speed
- Proper starting position for the runner
"""

import turtle
import random

# Configuration variables - these control the maze appearance
NUM_WALLS = 6  # Reduced number of walls for better navigation
PATH_WIDTH = 30  # Increased path width for easier navigation
WALL_COLOR = "black"  # Color for the maze walls
RUNNER_COLOR = "red"  # Color for the maze runner
RUNNER_SPEED = 10  # Speed of the maze runner

# Create the turtle for drawing the maze
maze_painter = turtle.Turtle()
maze_painter.speed(0)  # Fastest drawing speed
maze_painter.color(WALL_COLOR)
maze_painter.pensize(2)

# Create the screen
screen = turtle.Screen()
screen.title("Maze Runner - Use Arrow Keys to Turn, 'G' to Move")
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

def draw_spiral_maze():
    """
    Draws a spiral maze with randomly placed doors and barriers.
    Uses functions to eliminate code duplication and improve efficiency.
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
            
            # Only add barriers for walls 3 and beyond (adjusted for smaller maze)
            if i >= 3:
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
                # For first 3 walls, only draw door (no barrier to avoid errors)
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

# Create the maze runner turtle
maze_runner = turtle.Turtle()
maze_runner.shape("turtle")
maze_runner.color(RUNNER_COLOR)
maze_runner.pensize(3)
maze_runner.speed(0)  # Fastest speed for responsive movement

# Movement functions for the maze runner
def turn_up():
    """Turn the maze runner to face up (north)."""
    maze_runner.setheading(90)

def turn_down():
    """Turn the maze runner to face down (south)."""
    maze_runner.setheading(270)

def turn_left():
    """Turn the maze runner to face left (west)."""
    maze_runner.setheading(180)

def turn_right():
    """Turn the maze runner to face right (east)."""
    maze_runner.setheading(0)

def move_runner():
    """Move the maze runner forward by the specified amount."""
    maze_runner.forward(RUNNER_SPEED)

# Draw the maze first
draw_spiral_maze()

# Hide the maze drawing turtle
maze_painter.hideturtle()

# Position the maze runner at a good starting location
# Place it in the center area where there's likely to be open space
maze_runner.penup()
maze_runner.goto(PATH_WIDTH, 0)  # Start in the center area
maze_runner.pendown()

# Set up keyboard event handlers
screen.onkeypress(turn_up, "Up")
screen.onkeypress(turn_down, "Down")
screen.onkeypress(turn_left, "Left")
screen.onkeypress(turn_right, "Right")
screen.onkeypress(move_runner, "g")

# Start listening for keyboard events
screen.listen()

# Keep the window open
turtle.mainloop()
