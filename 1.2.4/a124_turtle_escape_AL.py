"""
AP CSP 1.2.4 - Turtle Escape Maze Game
Student: Alex Liao

Pseudocode for square spiral:
1. Decide on number of walls for the spiral
2. Start from center and work out
3. Use a for loop and the range function
4. On each iteration, turn your turtle and grow the size of the wall
5. Don't forget to include mainloop to control the screen

Pseudocode for adding doors:
1. Draw part of the wall (10 pixels)
2. Lift the pen to create an opening
3. Move forward by twice the path width (door opening size)
4. Put the pen down to continue drawing the wall
5. Complete the rest of the wall

Pseudocode for adding barriers:
1. Draw part of the wall (10 pixels)
2. Create door opening (lift pen, move forward, put pen down)
3. Draw more wall (40 pixels past the door)
4. Turn left 90 degrees to draw perpendicular barrier
5. Draw barrier wall (twice the path width long)
6. Go back to original position
7. Turn right 90 degrees to continue original wall
8. Complete the rest of the wall

Conclusion Questoins
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

Other Questoins
Question: Why do we need to ensure door and barrier don't overlap?
Answer: If a barrier renders inside a door opening, it defeats the purpose
of the door and creates visual confusion. The barrier should block the path,
not be inside an opening.

Question: Why is it important to draw door and barrier in the correct order?
Answer: Drawing them in order prevents the turtle from having to backtrack
and redraw portions of the wall, which is inefficient and can cause visual
artifacts. We want to draw each segment only once in the correct sequence.

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

Question: Why is the door opening twice the path width?
Answer: The door opening should match the width of the path between walls.
Since paths are created by the space between parallel walls, and each wall
grows by one path width, the total path width is effectively twice the
increment value. This ensures the door is wide enough for navigation.

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
    Solid exterior walls prevent early escape. Uses validated geometry
    (no while-loops) and disables animation for instant drawing.
    """
    # ---- performance: draw off-screen, then show once ----
    screen.tracer(False)

    # geometry constants
    DOOR_W   = PATH_WIDTH * 2      # door opening along the wall
    SEP      = PATH_WIDTH * 2      # min separation between door and barrier
    MARGIN   = PATH_WIDTH          # keep features away from corners
    BAR_H    = PATH_WIDTH * 2      # barrier height (perpendicular)

    # Start near the center so the spiral grows out nicely
    start_offset = PATH_WIDTH / 2
    maze_painter.penup()
    maze_painter.goto(-start_offset, -start_offset)
    maze_painter.setheading(0)
    maze_painter.pendown()
    
    length = PATH_WIDTH                     # first segment length
    segments = NUM_WALLS * 4 + 1            # sides to draw (plus tail)
    last_solid_start = (NUM_WALLS - 1) * 4  # last "ring" is solid

    for k in range(segments):
        # Exterior ring: draw solid wall (no openings)
        if k >= last_solid_start:
            maze_painter.forward(length)

        else:
            usable = length - 2 * MARGIN  # space available for features on this wall

            # If wall is too short to place anything safely, just draw it
            if usable <= 0:
                maze_painter.forward(length)

            else:
                # Door fits only if usable >= DOOR_W
                if usable < DOOR_W:
                    maze_painter.forward(length)
                else:
                    # Door start ∈ [MARGIN, MARGIN + usable - DOOR_W]
                    door_lo = MARGIN
                    door_hi = MARGIN + usable - DOOR_W
                    door = random.randint(int(door_lo), int(door_hi))

                    # Add barriers from the 3rd wall onward (k >= 12),
                    # but only if there is *enough* room for door + separation.
                    have_barrier = (k >= 12 and usable >= DOOR_W + SEP)

                    if have_barrier:
                        # Choose a side where barrier can satisfy separation
                        left_span  = door - MARGIN
                        right_span = (MARGIN + usable) - (door + DOOR_W)
                        choices = []
                        if left_span  >= SEP: choices.append("left")
                        if right_span >= SEP: choices.append("right")

                        # If neither side can satisfy, fall back to door only
                        if not choices:
                            # draw: to door → door → rest
                            maze_painter.forward(door)
                            maze_painter.penup(); maze_painter.forward(DOOR_W); maze_painter.pendown()
                            maze_painter.forward(length - (door + DOOR_W))
                        else:
                            side = random.choice(choices)
                            if side == "left":
                                barrier = random.randint(int(MARGIN), int(door - SEP))
                                # to barrier
                                maze_painter.forward(barrier)
                                # draw barrier
                                maze_painter.left(90); maze_painter.forward(BAR_H)
                                maze_painter.back(BAR_H); maze_painter.right(90)
                                # to door
                                maze_painter.forward(door - barrier)
                                # door
                                maze_painter.penup(); maze_painter.forward(DOOR_W); maze_painter.pendown()
                                # rest
                                maze_painter.forward(length - (door + DOOR_W))
                            else:
                                barrier = random.randint(int(door + DOOR_W + SEP),
                                                         int(MARGIN + usable))
                                # to door
                                maze_painter.forward(door)
                                # door
                                maze_painter.penup(); maze_painter.forward(DOOR_W); maze_painter.pendown()
                                # to barrier
                                maze_painter.forward(barrier - (door + DOOR_W))
                                # draw barrier
                                maze_painter.left(90); maze_painter.forward(BAR_H)
                                maze_painter.back(BAR_H); maze_painter.right(90)
                                # rest
                                maze_painter.forward(length - barrier)
                    else:
                        # Early or cramped walls: door only
                        maze_painter.forward(door)
                        maze_painter.penup(); maze_painter.forward(DOOR_W); maze_painter.pendown()
                        maze_painter.forward(length - (door + DOOR_W))

        maze_painter.left(90)
        # increase length after every 2 sides to keep spacing even
        if k % 2 == 1:
            length += PATH_WIDTH

    # Add the final line extending from the outermost square
    maze_painter.forward(PATH_WIDTH)

    # ---- show everything at once ----
    screen.tracer(True)
    screen.update()

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
