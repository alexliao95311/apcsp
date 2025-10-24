# a121_catch_a_turtle.py

#-----import statements-----
import turtle as trtl  # Import turtle graphics library for game display
import random as rand  # Import random module for generating random positions, colors, sizes, and shapes
# Step 2: Add import statement for leaderboard module
import leaderboard as lb  # Import custom leaderboard module for managing high scores

#-----game configuration----
# Game appearance settings
spot_color = "pink"  
spot_size = 2 
spot_shape = "circle" 

# Game state variables
score = 0 
font_setup = ("Arial", 20, "normal") 
header_font = ("Arial", 16, "bold")  
# Step 6: Set timer to 30s
timer = 30  
counter_interval = 1000  
timer_up = False  

# Step 3: Initialize variables for leaderboard functionality
# PLTW Question: Can you tell what each variable will be used for?
# leaderboard_file_name will store the path to the text file where high scores are saved
# player_name will store the current player's name for potential leaderboard entry
leaderboard_file_name = "a122_leaderboard.txt" 
player_name = input("What's your name? ") 

# PLTW Question: Why is it better user-centered design to place the input statement asking for the user's name before the turtles are initialized?
# Answer: Getting the player's name first prevents interruption of the game flow and ensures the turtle window doesn't interfere with text input

# Customization variables for dynamic game features
colors = ["red", "blue", "green", "yellow", "orange", "purple", "cyan", "magenta"]  
sizes = [0.5, 1, 1.5, 2, 2.5, 3] 
shapes = ["circle", "square", "triangle", "turtle", "arrow", "classic"] 

#-----initialize turtle-----
spot = trtl.Turtle()  
spot.shape(spot_shape) 
spot.shapesize(spot_size)  
spot.fillcolor(spot_color)
spot.penup() 

# Initialize the score display turtle
score_writer = trtl.Turtle()  
score_writer.penup()  
score_writer.goto(-190, 160) 
score_writer.hideturtle() 
score_writer.color("black") 

# Initialize the timer display turtle
counter = trtl.Turtle()  
counter.penup() 
counter.goto(80, 160)  
counter.hideturtle() 
counter.color("black") 
#-----game functions--------
"""
change the spot's color and leave a colorful stamp
"""
def add_color_stamp():
    stamp_color = rand.choice(colors) 
    spot.fillcolor(stamp_color)  
    spot.stamp() 
    spot.fillcolor(spot_color) 

"""
change the spot's size randomly
"""
def change_size():
    new_size = rand.choice(sizes)  # Select random size from sizes list
    spot.shapesize(new_size) 

"""
change the spot's shape randomly
"""
def change_shape():
    new_shape = rand.choice(shapes)  # Select random shape from shapes list
    spot.shape(new_shape)  

"""
change the spot's position randomly using random.randint and apply visual effects
"""
def change_position():
    add_color_stamp()
    change_size()      
    change_shape() 
    new_xpos = rand.randint(-200, 200)  
    new_ypos = rand.randint(-150, 150) 
    spot.hideturtle()
    spot.goto(new_xpos, new_ypos) 
    spot.showturtle()

"""
increment score and write it on the screen
"""
def update_score():
    global score  # Access global score variable to modify it
    score += 1  
    score_writer.clear()  # Clear previous score display
    score_writer.write(f"Score: {score}", font=header_font) 

"""
start a countdown. if the time is up, display time out; otherwise, keep counting down
"""
def countdown():
    global timer, timer_up 
    counter.clear() 
    # Step 5: Add manage_leaderboard function call when timer reaches 0
    if timer <= 0: 
        counter.write("Time's Up", font=font_setup)  # Display game over message
        timer_up = True  # Set flag to indicate game is over
        manage_leaderboard() 
    else:  # If time remaining
        counter.write(f"Time: {timer}s", font=header_font)  # Display current time
        timer -= 1  # Decrease timer by 1 second
        counter.getscreen().ontimer(countdown, counter_interval)

"""
initialize all the game variables and start the game
"""
def start_game():
    global timer_up, score  
    timer_up = False
    score = 0  
    spot.showturtle()  
    score_writer.clear()  # Clear any previous score display
    score_writer.write(f"Score: {score}", font=header_font)  # Show starting score
    # Start the countdown timer
    wn.ontimer(countdown, counter_interval) 
# Step 4: Add function to manage leaderboard for top 5 scorers
def manage_leaderboard():
    """
    Manages the leaderboard functionality by getting current scores,
    determining if player qualifies for top 5, and displaying results
    """
    global score 
    global spot   
    # PLTW Question: Why are the variables preceded by the keyword global?
    # Answer: Variables are preceded by global because these functions need to access and modify 
    # variables (score and spot) that are defined outside this function's scope
    
    # Get the names and scores from the leaderboard file
    leader_names_list = lb.get_names(leaderboard_file_name) 
    leader_scores_list = lb.get_scores(leaderboard_file_name) 
    
    # Show the leaderboard with or without the current player
    if (len(leader_scores_list) < 5 or score >= leader_scores_list[4]):
        # Player made the leaderboard - update file and display with highlight
        lb.update_leaderboard(leaderboard_file_name, leader_names_list, leader_scores_list, player_name, score)
        
    # Display updated leaderboard (get fresh data after potential update)
    updated_names = lb.get_names(leaderboard_file_name)
    updated_scores = lb.get_scores(leaderboard_file_name) 
    lb.draw_leaderboard(updated_names, updated_scores)

"""
event handler for when user clicks the spot
"""
def spot_clicked(x, y):
    global timer_up  # Access global timer flag to check if game is over
    if timer_up == False:  
        change_position()  
        update_score()    
    else:  # If game time is up
        spot.hideturtle() 

# Set up the game window and start the game
wn = trtl.Screen()  
wn.bgcolor("white") 
wn.title("Catch-A-Turtle Game!") 

# Set up event handlers and start the game
spot.onclick(spot_clicked) 
start_game() 
wn.mainloop()  