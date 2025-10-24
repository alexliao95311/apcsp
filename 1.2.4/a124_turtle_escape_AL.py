"""
AP CSP 1.2.4 - Turtle Escape Maze Game
Student: Alex Liao

This is the final complete maze program with customizable features.
The turtle must navigate through a randomly generated maze to escape.

Customizations implemented:
- Solid exterior walls (no doors on outer walls)
- Timer functionality to track escape time
- Restart game feature
- Variable turtle speed controls
- Improved maze generation with better navigation

Program Description:
This program creates a spiral maze with randomly placed doors and barriers,
then allows the player to control a turtle to navigate through the maze.
The goal is to escape the maze as quickly as possible. The game includes
a timer to track performance and the ability to restart for multiple attempts.
The maze features solid exterior walls to prevent early escape and provides
a challenging navigation experience with proper door and barrier placement.

Question 1: Why is pseudocode useful?
Answer: Pseudocode is useful from both reading and writing perspectives because:
- Reading: It helps understand the logic and flow of algorithms before implementation
- Writing: It allows planning and organizing thoughts before coding, making the actual
  implementation clearer and more structured. It serves as a blueprint that can be
  easily modified and refined before committing to actual code.

Question 2: How do the door and barrier algorithms work?
Answer: The draw_door() and draw_barrier() functions work together to create maze
obstacles. The draw_door() function creates openings by lifting the pen and moving
forward, while draw_barrier() draws perpendicular walls that block paths. These
functions relate to the main maze algorithm by being called in sequence based on
their random positions - the algorithm determines which comes first using selection
logic, then draws wall segments, doors, and barriers in the correct order to avoid
backtracking and ensure proper maze structure.
"""

import turtle
import random
import time

# Configuration variables - these control the maze appearance
NUM_WALLS = 6  # Number of walls in the spiral
PATH_WIDTH = 50  # Distance between walls (width of the path)
WALL_COLOR = "black"  # Color for the maze walls
RUNNER_COLOR = "red"  # Color for the maze runner
RUNNER_SPEED = 15  # Base speed of the maze runner

# Global variables for game state
game_start_time = None
game_running = True
current_speed = RUNNER_SPEED

# Create the turtle for drawing the maze
maze_painter = turtle.Turtle()
maze_painter.speed(0)  # Fastest drawing speed
maze_painter.color(WALL_COLOR)
maze_painter.pensize(2)

# Create the screen
screen = turtle.Screen()
screen.title("Turtle Escape Maze - Arrow Keys to Turn, 'G' to Move, 'R' to Restart, +/- for Speed")
screen.bgcolor("lightblue")

# Create the maze runner turtle
maze_runner = turtle.Turtle()
maze_runner.shape("turtle")
maze_runner.color(RUNNER_COLOR)
maze_runner.pensize(3)
maze_runner.speed(0)  # Fastest speed for responsive movement

# Create a text turtle for displaying game information
text_display = turtle.Turtle()
text_display.hideturtle()
text_display.penup()
text_display.goto(-200, 200)
text_display.color("blue")

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

def update_timer():
    """Updates and displays the current game timer."""
    if game_start_time and game_running:
        elapsed_time = time.time() - game_start_time
        text_display.clear()
        text_display.write(f"Time: {elapsed_time:.1f}s | Speed: {current_speed} | Press 'R' to restart", 
                          font=("Arial", 12, "normal"))
        screen.ontimer(update_timer, 100)  # Update every 100ms

def draw_spiral_maze():
    """
    Draws a spiral maze with randomly placed doors and barriers.
    Solid exterior walls prevent early escape.
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
        # For exterior walls (last iteration), don't add doors - solid walls
        if k >= (NUM_WALLS - 1) * 4:
            # Draw solid wall for exterior
            maze_painter.forward(length)
        elif k < 8:  # First 2 walls (8 segments)
            # Draw simple wall with door
            maze_painter.forward(10)
            maze_painter.penup()
            maze_painter.forward(PATH_WIDTH * 2)
            maze_painter.pendown()
            remaining_length = length - 10 - (PATH_WIDTH * 2)
            maze_painter.forward(remaining_length)
        else:
            # For later segments, add doors and barriers
            # Generate random positions for door and barrier
            # Ensure they're not too close to the beginning or end of the wall
            # Make sure we have enough space for doors and barriers
            min_pos = PATH_WIDTH * 2
            max_pos = max(length - PATH_WIDTH * 2, min_pos + PATH_WIDTH * 2)
            
            door = random.randint(min_pos, max_pos)
            barrier = random.randint(min_pos, max_pos)
            
            # Ensure door and barrier don't overlap
            while abs(door - barrier) < PATH_WIDTH * 2:
                barrier = random.randint(min_pos, max_pos)
            
            # Only add barriers for walls 3 and beyond
            if k >= 12:  # 3 walls * 4 sides = 12 segments
                # Determine which comes first: door or barrier
                if door < barrier:
                    # Door comes first
                    draw_wall_segment(door)
                    draw_door()
                    draw_wall_segment(barrier - door - (PATH_WIDTH * 2))
                    draw_barrier()
                    remaining_length = length - barrier
                    draw_wall_segment(remaining_length)
                else:
                    # Barrier comes first
                    draw_wall_segment(barrier)
                    draw_barrier()
                    draw_wall_segment(door - barrier)
                    draw_door()
                    remaining_length = length - door - (PATH_WIDTH * 2)
                    draw_wall_segment(remaining_length)
            else:
                # For first 3 walls, only draw door
                draw_wall_segment(door)
                draw_door()
                remaining_length = length - door - (PATH_WIDTH * 2)
                draw_wall_segment(remaining_length)
        
        maze_painter.left(90)
        # increase length after every 2 sides to keep spacing even
        if k % 2 == 1:
            length += PATH_WIDTH
    
    # Add the final line extending from the outermost square
    maze_painter.forward(PATH_WIDTH)

def restart_game():
    """Restarts the game by resetting the turtle position and timer."""
    global game_start_time, game_running
    
    # Reset game state
    game_running = True
    game_start_time = time.time()
    
    # Clear the maze runner's path
    maze_runner.clear()
    maze_runner.penup()
    maze_runner.goto(PATH_WIDTH, 0)
    maze_runner.pendown()
    
    # Reset text display
    text_display.clear()
    text_display.goto(-200, 200)
    update_timer()

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
    """Move the maze runner forward by the current speed amount."""
    if game_running:
        maze_runner.forward(current_speed)

def increase_speed():
    """Increase the turtle's movement speed."""
    global current_speed
    current_speed = min(current_speed + 5, 30)  # Cap at 30

def decrease_speed():
    """Decrease the turtle's movement speed."""
    global current_speed
    current_speed = max(current_speed - 5, 5)  # Minimum of 5

# Draw the initial maze
draw_spiral_maze()

# Hide the maze drawing turtle
maze_painter.hideturtle()

# Position the maze runner at starting location
maze_runner.penup()
maze_runner.goto(PATH_WIDTH, 0)  # Start in the center area
maze_runner.pendown()

# Start the game timer
game_start_time = time.time()

# Set up keyboard event handlers
screen.onkeypress(turn_up, "Up")
screen.onkeypress(turn_down, "Down")
screen.onkeypress(turn_left, "Left")
screen.onkeypress(turn_right, "Right")
screen.onkeypress(move_runner, "g")
screen.onkeypress(restart_game, "r")
screen.onkeypress(increase_speed, "plus")
screen.onkeypress(increase_speed, "equal")  # For keyboards without separate plus key
screen.onkeypress(decrease_speed, "minus")

# Start listening for keyboard events
screen.listen()

# Start the timer display
update_timer()

# Display instructions
text_display.goto(-200, 180)
text_display.write("Use arrow keys to turn, 'G' to move forward", font=("Arial", 10, "normal"))
text_display.goto(-200, 160)
text_display.write("Press 'R' to restart, '+'/'-' to change speed", font=("Arial", 10, "normal"))

# Keep the window open
turtle.mainloop()
