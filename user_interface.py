"""
This module defines user interface functions for the Risk program
"""

from probability import *

def print_scenario(attackers, defenders, a_min=0, d_min=0, verbose=False):
    """
    Displays the invasion scenario that we're calculating probabilities for.
    """
    if verbose:
        # Grammar isn't very cooperative when it comes to concise coding
        if attackers == 1:
            print('1 attacker vs. ', end='')
        else:
            print('%d attackers vs. ' % attackers, end='')
        
        if defenders == 1:
            print('1 defender')
        else:
            print('%d defenders' % defenders)
        
        # Only print minimums if they're non-zero
        if a_min:
            print('The attacker wants to win with at least %d units.' % a_min)
        
        if d_min:
            print('The attacker wants to reduce the defender to %d units.' % d_min)
    else:
        # If not verbose, just print the numbers
        print('%d vs. %d' % (attackers, defenders))
        
        # Only print minimums if they're non-zero
        if a_min:
            print('r: %d' % a_min)
        
        if d_min:
            print('g: %d' % d_min)

def print_invasion_odds(outcomes, d_min, verbose=False):
    """
    Accepts the results of calculate_invasion(), sums the probabilities of all
    successful outcomes using d_min, and prints the final result.
    """
    # Get the odds of all the outcomes favorable to the attacker
    victory_prob = sum_invasion_odds(outcomes, d_min)
    
    # Print the chances of a successful invasion as a percentage
    percent = victory_prob * 100
    
    if verbose:
        print('The invasion has a %.1f%% chance of success.' % percent)
    else:
        print('%.1f%%' % percent)

def interactive_mode(attackers, defenders, a_min=0, d_min=0, verbose=False):
    """
    Prompts user for updates to the invasion scenario, then calculates and
    prints updated odds of success.
    """
    while attackers > a_min and defenders > d_min:
        # Print the current invasion scenario
        print_scenario(attackers, defenders, a_min, d_min, verbose)
        
        # Calculate and print the probabilities of the scenario's outcomes
        outcomes = calculate_invasion(attackers, defenders, a_min, d_min)
        print_invasion_odds(outcomes, d_min, verbose)
        
        # Receive a new command or scenario update.
        command = input('> ')
        
        # Enter 'q' to exit
        if command == 'q': break
        
        # Determine how many armies will be eliminated this battle
        losses = min(attackers, defenders, 2)
        
        # Interpret the command and subtract armies appropriately
        # If the attacker won the battle, the defender loses armies
        if command == 'a':
            defenders -= losses
        # If the defender won the battle, the attacker loses armies
        elif command == 'd':
            attackers -= losses
        # If the battle was a tie, each loses one.
        elif command == 't' and losses == 2:
            attackers -= 1
            defenders -= 1
        # Tell the user if they messed up
        else:
            print('\'%s\' is not a valid command.' % command)
    else:
        # If the invasion ended before the user quit, print the outcome
        if verbose:
            if defenders > d_min:
                if defenders == 1:
                    print('The defender has won with 1 army.')
                else:
                    print('The defender has won with %d armies.' % defenders)
            else:
                if attackers == 1:
                    print('The attacker has won with 1 army.')
                else:
                    print('The attacker has won with %d armies.' % attackers)
        else:
            print('%d vs. %d' % (attackers, defenders))
