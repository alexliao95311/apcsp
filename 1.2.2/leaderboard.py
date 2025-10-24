# leaderboard.py

# Step 1: Import required libraries
import turtle as trtl

# PLTW Computer Science Notebook: Data Abstraction Notes
# Data abstraction manages complexity in a program. Ways to use abstraction:
# 1. Data abstraction provides separation between abstract properties of a data type and concrete details of its representation
# 2. Data abstractions manage complexity by giving a collection of data a name without referencing specific representation details
# 3. Data abstractions can be created using lists
# 4. Developing a data abstraction to implement in a program can result in a program that is easier to develop and maintain
# 5. Data abstractions often contain different types of elements

# Step 10: Set the levels of scoring
bronze_score = 15
silver_score = 20
gold_score = 25

# Step 10: Return names in the leaderboard file
def get_names(file_name):
    """
    Extract and return a list of player names from the leaderboard file
    Reads each line, extracts the name portion (before comma), adds to list
    """
    # PLTW Question: What are the three functions in this module, and what is each function designed to do?
    # Answer: 1. get_names() - extracts and returns player names from leaderboard file
    #         2. get_scores() - extracts and returns player scores from leaderboard file  
    #         3. update_leaderboard() - inserts new player data and maintains top 5 list
    #         4. draw_leaderboard() - displays leaderboard and messages on screen
    
    # PLTW Question: Can you tell what the open function does?
    # Answer: The open function with "r" parameter opens the file for reading and returns 
    # a file object that allows us to read the contents line by line as strings
    leaderboard_file = open(file_name, "r")  # be sure you have created this

    # use a for loop to iterate through the content of the file, one line at a time
    # note that each line in the file has the format "leader_name,leader_score" for example "Pat,50"
    # PLTW Question: What is this loop header doing?
    # Answer: This loop iterates through each line in the file, processing one complete 
    # entry at a time where each line contains "name,score" format
    names = []
    for line in leaderboard_file:
        # Skip empty lines to avoid index errors
        if line.strip() == "":
            continue
            
        leader_name = ""
        index = 0

        # TODO 1: use a while loop to read the leader name from the line (format is "leader_name,leader_score")
        
        # Step 18: Add while loop to extract name portion
        # PLTW Question: Explain what is happening in each line of the code as it executes
        # Answer: The loop checks each character in the line. If it's not a comma, it adds the character
        # to leader_name and moves to the next character. This continues building the name until comma is found.
        # PLTW Question: What character will index be pointing at when the loop ends?
        # Answer: When the loop ends, index will be pointing at the comma character that separates name from score.
        while (line[index] != ","):
            leader_name = leader_name + line[index] 
            index = index + 1

        # Step 19: Add print statement to see extracted values during testing
        # PLTW Question: Can you think of a simple line of code that can help you see their values?
        # Answer: A print statement right after the while loop will show the extracted names
        print("Extracted name:", leader_name)  # Debug output for testing

        # TODO 2: add the player name to the names list
        # Step 20: Add leader name to the names list
        names.append(leader_name)

    leaderboard_file.close()

    # TODO 6: return the names list in place of the empty list
    # Step 26: Return the list of players' names
    return names

# Step 10: Return scores from the leaderboard file  
def get_scores(file_name):
    """
    Extract and return a list of player scores from the leaderboard file
    Reads each line, extracts the score portion (after comma), converts to integer, adds to list
    """
    leaderboard_file = open(file_name, "r")  # be sure you have created this

    scores = []
    for line in leaderboard_file:
        # Skip empty lines to avoid index errors
        if line.strip() == "":
            continue
            
        leader_score = ""    
        index = 0

        # TODO 3: use a while loop to index beyond the comma, skipping the player's name
        # Step 21: Add while loop to find comma character
        while (line[index] != ","):
            index = index + 1
        
        # Step 22: Increment index to move past comma to first character of score
        index = index + 1

        # TODO 4: use a while loop to get the score
        # Step 23: Loop until newline character to extract score
        # PLTW Question: What should the loop Boolean expression check for?
        # Answer: The loop should check for the newline character "\n" which indicates the end of the line
        while (line[index] != "\n"):
            leader_score = leader_score + line[index]
            index = index + 1

        # Step 25: Add print statement to test score extraction
        print("Extracted score:", leader_score)  # Debug output for testing

        # TODO 5: add the player score to the scores list
        # Step 24: Convert string to integer and add to scores list
        # Note: Convert from string to integer since scores will be used as numerical values
        scores.append(int(leader_score))
   
    leaderboard_file.close()

    # TODO 7: return the scores in place of the empty list
    # Step 27: Return the list of players' scores
    return scores

# Step 11: Function to update leaderboard
def update_leaderboard(file_name, leader_names, leader_scores, player_name, player_score):
    """
    Update the leaderboard with a new player score if it qualifies
    Inserts new score in correct position and maintains top 5 only
    Parameters: file_name (str), leader_names (list), leader_scores (list), player_name (str), player_score (int)
    """
    leader_index = 0

    # PLTW Question: What is the length of the list?
    # Answer: The length represents how many scores are currently stored in the leaderboard

    # TODO 8: use a while loop to iterate through the leader board scores
    # Step 28: Compare player score with existing scores to find insertion point
    while (leader_index < len(leader_scores)) and (player_score <= leader_scores[leader_index]):
        leader_index = leader_index + 1

    # PLTW Question: What list are you looping through?  
    # Answer: I am looping through the leader_scores list to compare the player's score with existing high scores

    # PLTW Question: What are you adding to the list?  
    # Answer: I am adding the player's name to the leader_names list and the player's score to the leader_scores list at the appropriate index to maintain sorted order

    # Step 29: Insert new player data at correct position
    leader_names.insert(leader_index, player_name)
    leader_scores.insert(leader_index, player_score)

    # TODO 9: keep only the top 5 players
    # Step 30: Limit leaderboard to top 5 scores
    # PLTW Question: How do you want to alter the lists? 
    # Answer: I want to remove the lowest scores to keep only the top 5, so I use pop() to remove the last elements if the list exceeds 5 entries
    if len(leader_names) > 5:
        leader_names.pop()
        leader_scores.pop()

    # TODO 10: write the updated leaderboard to the file
    # Step 31: Save updated leaderboard to file
    leaderboard_file = open(file_name, "w")

    for i in range(len(leader_names)):
        leaderboard_file.write(leader_names[i] + "," + str(leader_scores[i]) + "\n")
    
    leaderboard_file.close()

# Step 12: Function to display leaderboard
def draw_leaderboard(leader_names, leader_scores):
    """
    Display the current leaderboard on screen
    Shows rank, name, and score for each player
    Parameters: leader_names (list), leader_scores (list)
    """
    font_setup = ("Arial", 20, "normal")
    trtl.clear()
    trtl.penup()
    trtl.goto(-200, 100)
    trtl.pendown()
    trtl.write("LEADERBOARD", font=font_setup)
    trtl.penup()

    # PLTW Question: What will this loop run?
    # Answer: This loop will run once for each name/score pair in the leaderboard to display the ranking

    y_position = 50
    for i in range(len(leader_names)):
        trtl.goto(-200, y_position)
        trtl.pendown()
        
        # TODO 11: use the i variable to write the correct number for each leaderboard entry
        # Step 32: Display rank number, name and score
        trtl.write(f"{i+1}. {leader_names[i]}: {leader_scores[i]}", font=font_setup)
        trtl.penup()
        
        y_position -= 30

    # PLTW Question: How do you show each leaderboard entry?
    # Answer: Each entry displays the rank number (i+1), player name, and score using trtl.write() with consistent font formatting and positioning