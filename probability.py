#!/usr/bin/python3
"""
This module defines functions used to calculate the odds of possible outcomes
in Risk battles, invasions, and campaigns.
"""

"""
casualty_odds is a table of possible casualty numbers and their probabilities
for the 6 possible battle scenarios
"""
casualty_odds = (
# Row for 1 attacker scenarios
(
    # 1 attacker, 1 defender
    ((0, 1, 5/12), # Attacker victory
    (1, 0, 7/12)), # Defender victory
    # 1 attacker, 2 defenders
    ((0, 1, 55/216), # Attacker victory
    (1, 0, 161/216)) # Defender victory
),
# Row for 2 attacker scenarios
(
    # 2 attackers, 1 defender
    ((0, 1, 125/216), # Attacker victory
    (1, 0, 91/216)), # Defender victory
    # 2 attackers, 2 defenders
    ((0, 2, 295/1296), # Attacker victory
    (2, 0, 581/1296), # Defender victory
    (1, 1, 420/1296)) # Tie
),
# Row for 3 attacker scenarios
(
    # 3 attackers, 1 defender
    ((0, 1, 855/1296), # Attacker victory
    (1, 0, 441/1296)), # Defender victory
    # 3 attackers, 2 defenders
    ((0, 2, 2890/7776), # Attacker victory
    (2, 0, 2275/7776), # Defender victory
    (1, 1, 2611/7776)) # Tie
)
)

def calculate_battle(attackers, defenders, chance=1):
    """
    Accepts a battle scenario and returns the probabilities of possible
    outcomes after one round of battle.
    """
    # Include the external casualty table in the function
    global casualty_odds
    
    # Set the number of dice to the maximum allowed for attacker and defender
    a = min(attackers, 3)
    d = min(defenders, 2)
    
    # Retrieve the possible troop losses for each side and their chances
    casualty_possibilities = casualty_odds[a-1][d-1] # Subtract 1 for indexing
    
    # Use possible troop losses to calculate possible outcomes
    outcomes = []
    for p in casualty_possibilities:
        result = (attackers - p[0], defenders - p[1], p[2] * chance)
        outcomes.append(result)
    
    # Return the outcomes in immutable, tuple form
    return tuple(outcomes)

def calculate_invasion(attackers, defenders, a_min=0, d_min=0, chance=1):
    """
    Accepts an invasion scenario (number of attackers and defenders), including
    when the attacker will retreat, and its chance of happening. Returns a
    dictionary of all possible outcomes and their probabilities.
    """
    
    # Create a grid of possible states of the invasion and their odds.
    # Only states within the boundaries of starting troop numbers and troop
    # minimums are included in the grid. Possible scenarios are referenced
    # using odds_grid[attackers - a_min][defenders - d_min]
    x_max = attackers - a_min
    y_max = defenders - d_min
    odds_grid = [[0 for y in range(y_max+1)] for x in range(x_max+1)]
    
    # Set the probability for the initial state (usually 100%)
    odds_grid[x_max][y_max] = chance
    
    # Initialize the dictionary of outcomes (keys) and probabilities (values)
    outcomes = {}
    
    # Loop through the grid, from the rightmost column to the left, starting
    # at the highest cell of each column.
    for x in range(x_max, -1, -1):
        for y in range(y_max, -1, -1):
            # Retrieve the probability of the current state
            prob = odds_grid[x][y]
            
            # If the current state will never happen, skip it
            if not prob: continue
            
            # Find the number of attacking and defending armies using minimums
            a = a_min + x
            d = d_min + y
            
            # If the current state is final, add its probability to outcomes
            if x == 0 or y == 0:
                outcomes[(a, d)] = prob
                continue
            
            # If not, calculate probabilities of states arising from this one
            for state in calculate_battle(a, d, prob):
                # If either force is below minimum, add it directly to outcomes
                if state[0] < a_min or state[1] < d_min:
                    outcomes[(state[0], state[1])] = state[2]
                    continue
                
                # Add the probability to the proper odds_grid position
                odds_grid[state[0] - a_min][state[1] - d_min] += state[2]
    
    # Finally, return the possible outcomes and their probabilities
    return outcomes
