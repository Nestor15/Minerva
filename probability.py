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

def calculate_invasion(attackers, defenders, a_min=0, d_min=0):
    """
    Accepts an invasion scenario, including when the attacker will retreat.
    Returns a dictionary of all possible outcomes and their probabilities.
    
    Attackers isn't just the number of attackers: it can also be a dictionary
    of all possible numbers of attackers and the probabilities of the attack
    having that many units (this is used by calculate_campaign). The defenders
    argument, however, is just a number, as the number of defenders won't vary
    in the calculations this app does.
    """
    # First, test is attackers is just a number or a dictionary with odds
    if isinstance(attackers, int):
        max_attackers = attackers
    else:
        # Find the highest possible number of attackers in the invasion
        max_attackers = max(*attackers)
    
    # Now use the highest (or only) attacker number to create odds_grid
    
    # odds_grid is a grid of possible states of the invasion and their odds.
    # Only states within the boundaries of starting troop numbers and troop
    # minimums are included in the grid. Possible scenarios are referenced
    # using odds_grid[attackers - a_min][defenders - d_min]
    x_max = max_attackers - a_min
    y_max = defenders - d_min
    odds_grid = [[0 for y in range(y_max+1)] for x in range(x_max+1)]
    
    # Set the probabilities of the "initial scenarios" of odds_grid
    if isinstance(attackers, int):
        # Simple 100% for single-integer starting scenarios
        odds_grid[x_max][y_max] = 1
    else:
        # For a dict, place each probability in the appropriate grid square
        for attackers, prob in attackers.items():
            odds_grid[attackers - a_min][y_max] = prob
    
    # Initialize the dictionary of outcomes (keys) and probabilities (values)
    outcomes = {}
    
    # Loop through the grid, from the top-right to the lower-left, calculating
    # the probabilities of all possible states and outcomes of the battle.
    for distance in range(x_max + y_max + 1):
        # Create a diagonal a distance from the top-right and loop through it
        x_start = max(0, x_max - distance)
        y_start = min(y_max, y_max - (distance - x_max))
        diagonal = zip(range(x_start, x_max + 1), range(y_start, -1, -1))
        for x, y in diagonal:
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
                x = state[0] - a_min
                y = state[1] - d_min
                
                odds_grid[x][y] += state[2]
    
    # Finally, return the possible outcomes and their probabilities
    return outcomes

def sum_invasion_odds(outcomes, d_min=0):
    """
    sum_invasion_odds() adds up the odds of the possible outcomes (generated by
    calculate_invasion) to return the odds of the invasion's success.
    """
    victory_prob = 0
    for o in outcomes:
        if o[1] <= d_min:
            victory_prob += outcomes[o]
    
    return victory_prob

def calculate_campaign(attackers, targets, a_min=0):
    """
    calculate_campaign() accepts the number of troops in the attacking
    territory, a list of troop numbers of target territories (in sequence) and
    the minimum number of troops the attacker wants in the final territory.
    
    The function returns the probabilities of all possible outcomes in an array
    of dictionaries. The array indices represent the territory the campaign
    ended in (0 being the origin of the attacks), the dictionary keys the
    number of attackers and defenders in the territory, the values the
    probability of the outcome.
    """
    #Initialize outcomes array
    outcomes = [{} for territory in range(len(targets)+1)] # +1 for origin territory
    
    # a_dict contains chances of attacker counts in current attacking territory
    a_dict = {attackers : 1}
    
    # Loop through each target territory, calculating possible outcomes
    for origin, defenders in enumerate(targets):
        # First, adjust the number of attackers for the one unit left behind
        # Remove the scenario where the attacking force is below minimum
        if a_dict.get(a_min):
            outcomes[origin][(a_min, defenders)] = a_dict[a_min]
            del(a_dict[a_min])
        
        # Subtract 1 from each attacker number for the unit left behind
        new_a_dict = {}
        for attackers, probability in a_dict.items():
            new_a_dict[attackers-1] = probability
        
        a_dict = new_a_dict
        
        # Calculate the outcomes of this invasion and loop through them
        results = calculate_invasion(a_dict, defenders, a_min)
        # Clear out a_dict to store the new results
        a_dict = {}
        for result, probability in results.items():
            a = result[0]
            d = result[1]
            # If no defenders remain, it's a win
            if d == 0:
                # Add the number of attackers and probability to a_dict
                a_dict[a] = probability
            # Otherwise, the attack failed
            else:
                # Add the probability to the correct spot in outcomes
                # If that spot doesn't yet exist for the scenario, make it
                if not outcomes[origin].get((a+1, d)):
                    outcomes[origin][(a+1, d)] = 0
                
                # Add 1 for the attacker left behind in the origin territory
                outcomes[origin][(a+1, d)] += probability
    
    # Add values remaining in a_dict (successes) to outcomes and return
    for attackers_remaining, probability in a_dict.items():
        outcomes[-1][attackers_remaining] = probability
    
    return outcomes

def sum_campaign_odds(outcomes):
    """
    sum_campaign_odds() adds up the odds of the possible outcomes (generated by
    calculate_campaign) to return the odds of the campaign's success.
    """
    victory_prob = 0
    for o in outcomes[-1]:
        victory_prob += outcomes[-1][o]
    
    return victory_prob
