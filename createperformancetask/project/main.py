# Debate Tournament Simulator
# This program simulates a debate tournament where teams compete in preliminary rounds, tracks their win/loss records, ranks them, and determines which teams break to elimination rounds

import random
def simulate_prelims(teams, num_rounds):
    """Simulates preliminary rounds and returns the team records. Each round has 1 winner. Teams can't face the same opp twice"""

    #initialize records list with team
    records = []
    for team in teams:
        records.append({"name": team, "wins": 0, "losses": 0, "opponents": []})

    #simulate preliminary rounds
    for round_num in range(1, num_rounds + 1):
        print("--- Round " + str(round_num) + " ---")

        #initialize available teams
        available = list(range(len(records)))
        random.shuffle(available)
        #initialize pairings list
        pairings = []
        #simulate pairings
        while len(available) >= 2:
            #pop first team
            team_a = available.pop(0)
            #initialize paired flag
            paired = False
            #iterate through available teams
            for j in range(len(available)):
                #get team b
                team_b = available[j]
                #check if team b has not faced team a yet
                if records[team_b]["name"] not in records[team_a]["opponents"]:
                    #remove team b from available
                    available.pop(j)
                    #add team a and team b to pairings
                    pairings.append((team_a, team_b))
                    #set paired flag to true
                    paired = True
                    break
            #if team b has not been paired and there are still available teams
            if not paired and len(available) > 0:
                #pop first team
                team_b = available.pop(0)
                #add team a and team b to pairings
                pairings.append((team_a, team_b))

        #if there is one available team
        if len(available) == 1:
            #get bye team
            bye_team = available[0]
            #increment bye team's wins
            records[bye_team]["wins"] += 1
            #print bye team's win
            print(records[bye_team]["name"] + " receives a bye (auto-win)")

        #iterate through pairings
        for pair in pairings:
            #get team a and team b
            a = pair[0]
            b = pair[1]
            #get team a and team b names
            name_a = records[a]["name"]
            name_b = records[b]["name"]
            #add team a and team b to each other's opponents
            records[a]["opponents"].append(name_b)
            records[b]["opponents"].append(name_a)

            #if team a is randomly selected to win
            if random.random() < 0.5:
                #increment team a's wins and team b's losses
                records[a]["wins"] += 1
                records[b]["losses"] += 1
                print(name_a + " defeated " + name_b)
            #if team b is randomly selected to win
            else:
                #increment team b's wins and team a's losses
                records[b]["wins"] += 1
                records[a]["losses"] += 1
                print(name_b + " defeated " + name_a)

        print()

    return records


def determine_break(records, min_wins):
    """Determines which teams break to elimination rounds based on their records. Teams with at least min_wins advance. The elim bracket is auto-selected as the smallest power of 2 that fits all qualifying teams."""

    #sort records by most wins first, then fewest losses as tiebreaker
    sorted_records = sorted(records, key=lambda r: (-r["wins"], r["losses"])) #lambda function to sort records by most wins first, then fewest losses as tiebreaker

    #initialize breaking teams list
    breaking_teams = []
    #iterate through sorted records
    for record in sorted_records:
        if record["wins"] >= min_wins:
            breaking_teams.append(record)

    num_breaking = len(breaking_teams)

    bracket_sizes = [2, 4, 8, 16, 32, 64]
    bracket_names = ["Finals", "Semis", "Quarters", "Octos", "Double Octos", "Triple Octos"]
    break_name = "Triple Octos" #default break name
    for b in range(len(bracket_sizes)):
        if bracket_sizes[b] >= num_breaking: #if bracket size is greater than or equal to number of breaking teams
            if num_breaking == bracket_sizes[b]: #if number of breaking teams is equal to bracket size
                break_name = "Full " + bracket_names[b] #set break name to full bracket name
            else:
                break_name = "Partial " + bracket_names[b] #set break name to partial bracket name
            break
    #return sorted records, breaking teams, and break name
    return sorted_records, breaking_teams, break_name


def main():
    print("=== Debate Tournament Tabulation Simulator ===")
    print("Simulates a tournament and determines which teams break to elims.\n")

    num_teams = int(input("Enter the number of teams: "))
    num_rounds = int(input("Enter the number of preliminary rounds: "))

    min_wins = int(input("Enter minimum wins needed to break: "))
    #initialize teams list
    teams = []
    #iterate through number of teams
    for i in range(num_teams):
        teams.append("Team " + str(i + 1)) #add team to teams list

    print("\n=== Simulating " + str(num_rounds) + " Preliminary Rounds ===\n")
    records = simulate_prelims(teams, num_rounds)

    #determine break
    
    sorted_records, breaking_teams, break_name = determine_break(records, min_wins)

    print("=== Final Standings ===")
    print("Rank | Team                 | Record")
    print("-" * 45)
    #iterate through sorted records
    for i in range(len(sorted_records)):
        #get rank
        rank = str(i + 1)
        #get name
        name = sorted_records[i]["name"]
        #get wins
        wins = str(sorted_records[i]["wins"])
        #get losses
        losses = str(sorted_records[i]["losses"])
        #get marker
        marker = " *" if sorted_records[i] in breaking_teams else ""
        #print rank, name, wins, losses, and marker
        print(rank.ljust(5) + "| " + name.ljust(21) + "| " + wins + "-" + losses + marker)

    print("\n=== Break to Elimination Rounds ===")
    print("Break: " + break_name + " (" + str(len(breaking_teams)) + " teams)")
    print("Min wins to qualify: " + str(min_wins) + "\n")

    #if no teams broke
    if len(breaking_teams) == 0:
        print("No teams qualified for the break.")
    else:
        #iterate through breaking teams
        for i in range(len(breaking_teams)):
            #get seed
            seed = str(i + 1)
            name = breaking_teams[i]["name"]
            wins = str(breaking_teams[i]["wins"])
            losses = str(breaking_teams[i]["losses"])
            print("Seed " + seed + ": " + name + " (" + wins + "-" + losses + ")")

    print("\n" + str(len(breaking_teams)) + " out of " + str(num_teams) + " teams advanced to elims.")

    if len(breaking_teams) == num_teams:
        print("Every team made the break!")
    elif len(breaking_teams) == 0:
        print("No teams broke - try lowering the win threshold.")
    else:
        bubble_team = breaking_teams[-1]
        print("Bubble team: " + bubble_team["name"] + " at " + str(bubble_team["wins"]) + "-" + str(bubble_team["losses"]))


main()
