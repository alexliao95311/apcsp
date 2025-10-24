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
PATH_WIDTH = 50  # Increased path width for easier navigation
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
    screen.tracer(False)

    # geometry constants
    DOOR_WIDTH = PATH_WIDTH * 2
    SEP        = PATH_WIDTH * 2      # min distance door↔barrier
    BARRIER_H  = PATH_WIDTH * 2
    MARGIN     = PATH_WIDTH          # keep features away from corners

    # start near center
    start_offset = PATH_WIDTH / 2
    maze_painter.penup()
    maze_painter.goto(-start_offset, -start_offset)
    maze_painter.setheading(0)
    maze_painter.pendown()

    length   = PATH_WIDTH
    segments = NUM_WALLS * 4 + 1

    for k in range(segments):
        usable = length - 2 * MARGIN             # space available for features
        have_barrier = (k >= 16)                 # don't try barriers on tiny walls

        if usable <= 0:
            # wall too short for any feature
            maze_painter.forward(length)

        else:
            # --- always try a door if it fits ---
            if usable < DOOR_WIDTH:
                # no room for a door; just draw the wall
                maze_painter.forward(length)
            else:
                # door start is clamped so the  door fits entirely
                door_lo = MARGIN
                door_hi = MARGIN + usable - DOOR_WIDTH
                door = random.randint(door_lo, int(door_hi))

                if have_barrier and usable >= DOOR_WIDTH + SEP:
                    # pick a side for the barrier that can satisfy separation
                    left_span  = door - MARGIN
                    right_span = (MARGIN + usable) - (door + DOOR_WIDTH)
                    choices = []
                    if left_span  >= SEP: choices.append("left")
                    if right_span >= SEP: choices.append("right")

                    if choices:
                        side = random.choice(choices)
                        if side == "left":
                            barrier = random.randint(MARGIN, int(door - SEP))
                            # draw: to barrier → barrier → to door → door → rest
                            maze_painter.forward(barrier)
                            maze_painter.left(90); maze_painter.forward(BARRIER_H)
                            maze_painter.back(BARRIER_H); maze_painter.right(90)
                            maze_painter.forward(door - barrier)
                            maze_painter.penup(); maze_painter.forward(DOOR_WIDTH); maze_painter.pendown()
                            maze_painter.forward(length - (door + DOOR_WIDTH))
                        else:
                            barrier = random.randint(int(door + DOOR_WIDTH + SEP),
                                                     int(MARGIN + usable))
                            # draw: to door → door → to barrier → barrier → rest
                            maze_painter.forward(door)
                            maze_painter.penup(); maze_painter.forward(DOOR_WIDTH); maze_painter.pendown()
                            maze_painter.forward(barrier - (door + DOOR_WIDTH))
                            maze_painter.left(90); maze_painter.forward(BARRIER_H)
                            maze_painter.back(BARRIER_H); maze_painter.right(90)
                            maze_painter.forward(length - barrier)
                    else:
                        # no side can satisfy SEP → just draw a door
                        maze_painter.forward(door)
                        maze_painter.penup(); maze_painter.forward(DOOR_WIDTH); maze_painter.pendown()
                        maze_painter.forward(length - (door + DOOR_WIDTH))
                else:
                    # not enough total space for door+barrier → just door
                    maze_painter.forward(door)
                    maze_painter.penup(); maze_painter.forward(DOOR_WIDTH); maze_painter.pendown()
                    maze_painter.forward(length - (door + DOOR_WIDTH))

        maze_painter.left(90)
        if k % 2 == 1:
            length += PATH_WIDTH

    maze_painter.forward(PATH_WIDTH)
    screen.tracer(True)

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
