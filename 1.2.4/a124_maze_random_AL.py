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
PATH_WIDTH = 40  # Distance between walls (width of the path)
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
    screen.tracer(False)  # draw instantly; turn back on at the end for speed

    # Start near the center so the spiral grows out nicely
    start_offset = PATH_WIDTH / 2
    maze_painter.penup()
    maze_painter.goto(-start_offset, -start_offset)
    maze_painter.setheading(0)
    maze_painter.pendown()
    
    length = PATH_WIDTH
    segments = NUM_WALLS * 4 + 1

    DOOR_WIDTH = PATH_WIDTH * 2
    BARRIER_HEIGHT = PATH_WIDTH * 2
    MARGIN = PATH_WIDTH  # keep features away from corners

    for k in range(segments):
        # Decide if this wall will have a barrier (skip until walls are big)
        have_barrier = (k >= 16)

        # Compute the usable span on this wall
        usable = length - 2 * MARGIN

        if usable <= 0:
            # Wall too short for any feature; just draw it
            maze_painter.forward(length)
        else:
            # Always allow a door when there is room for it
            max_door_start = max(MARGIN, MARGIN + usable - DOOR_WIDTH)
            door = random.randint(MARGIN, max_door_start)

            if have_barrier:
                # We need room for both a door and a barrier with separation
                # Require at least separation room: usable >= DOOR_WIDTH + PATH_WIDTH*2
                if usable >= DOOR_WIDTH + PATH_WIDTH * 2:
                    # pick a barrier position with required separation from the door
                    # choose which side of the door to place the barrier
                    left_span  = door - MARGIN
                    right_span = (MARGIN + usable) - (door + DOOR_WIDTH)

                    # pick side(s) that can fit PATH_WIDTH*2 separation
                    choices = []
                    if left_span >= PATH_WIDTH * 2:
                        choices.append("left")
                    if right_span >= PATH_WIDTH * 2:
                        choices.append("right")

                    if choices:
                        side = random.choice(choices)
                        if side == "left":
                            barrier = random.randint(MARGIN, door - PATH_WIDTH * 2)
                        else:
                            barrier = random.randint(door + DOOR_WIDTH + PATH_WIDTH * 2,
                                                     MARGIN + usable)
                        # Draw in the right order
                        if barrier < door:
                            # segment to barrier
                            maze_painter.forward(barrier)
                            # draw barrier
                            maze_painter.left(90); maze_painter.forward(BARRIER_HEIGHT)
                            maze_painter.back(BARRIER_HEIGHT); maze_painter.right(90)
                            # to door
                            maze_painter.forward(door - barrier)
                            # door opening
                            maze_painter.penup(); maze_painter.forward(DOOR_WIDTH); maze_painter.pendown()
                            # rest of wall
                            maze_painter.forward(length - (door + DOOR_WIDTH))
                        else:
                            # to door
                            maze_painter.forward(door)
                            # door opening
                            maze_painter.penup(); maze_painter.forward(DOOR_WIDTH); maze_painter.pendown()
                            # to barrier
                            maze_painter.forward(barrier - (door + DOOR_WIDTH))
                            # draw barrier
                            maze_painter.left(90); maze_painter.forward(BARRIER_HEIGHT)
                            maze_painter.back(BARRIER_HEIGHT); maze_painter.right(90)
                            # rest of wall
                            maze_painter.forward(length - barrier)
                    else:
                        # Not enough room to keep separation; just draw a door
                        maze_painter.forward(door)
                        maze_painter.penup(); maze_painter.forward(DOOR_WIDTH); maze_painter.pendown()
                        maze_painter.forward(length - (door + DOOR_WIDTH))
                else:
                    # Not enough total space for both; draw only a door
                    maze_painter.forward(door)
                    maze_painter.penup(); maze_painter.forward(DOOR_WIDTH); maze_painter.pendown()
                    maze_painter.forward(length - (door + DOOR_WIDTH))
            else:
                # Early walls: only a door
                maze_painter.forward(door)
                maze_painter.penup(); maze_painter.forward(DOOR_WIDTH); maze_painter.pendown()
                maze_painter.forward(length - (door + DOOR_WIDTH))

        maze_painter.left(90)
        if k % 2 == 1:
            length += PATH_WIDTH

    maze_painter.forward(PATH_WIDTH)
    screen.tracer(True)

# Draw the maze with random doors and barriers
draw_spiral_maze_random()

# Hide the turtle when done drawing
maze_painter.hideturtle()

# Keep the window open
turtle.mainloop()
