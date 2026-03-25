"""
PERSONALIZED PROJECT REFERENCE - Alex Liao

========================================
PROCEDURE - Code Segment 1
(Student-developed procedure with sequencing, selection, and iteration)
========================================
"""

def determine_break(records, min_wins):
    sorted_records = sorted(records, key=lambda r: (-r["wins"], r["losses"]))

    breaking_teams = []
    for record in sorted_records:
        if record["wins"] >= min_wins:
            breaking_teams.append(record)

    num_breaking = len(breaking_teams)

    bracket_sizes = [2, 4, 8, 16, 32, 64]
    bracket_names = ["Finals", "Semis", "Quarters", "Octos", "Double Octos", "Triple Octos"]
    break_name = "Triple Octos"
    for b in range(len(bracket_sizes)):
        if bracket_sizes[b] >= num_breaking:
            if num_breaking == bracket_sizes[b]:
                break_name = "Full " + bracket_names[b]
            else:
                break_name = "Partial " + bracket_names[b]
            break

    return sorted_records, breaking_teams, break_name

"""
========================================
PROCEDURE - Code Segment 2
(Call to the student-developed procedure)
========================================
"""

sorted_records, breaking_teams, break_name = determine_break(records, min_wins)

"""
========================================
LIST - Code Segment 1
(Showing how data have been stored in the list)
========================================
"""
num_teams = 0


teams = []
for i in range(num_teams):
    teams.append("Team " + str(i + 1))

records = []
for team in teams:
    records.append({"name": team, "wins": 0, "losses": 0, "opponents": []})

"""
========================================
LIST - Code Segment 2
(Showing the data in the list being used to fulfill the program's purpose)
========================================
"""
min_wins = 9

breaking_teams = []
for record in sorted_records:
    if record["wins"] >= min_wins:
        breaking_teams.append(record)

