#!/usr/bin/python3

import argparse as ap
from .user_interface import *

def positive_int(string):
    """
    positive_int() converts args to positive integers for troop numbers
    """
    # Convert the argument string value to an integer
    try:
        value = int(string)
    except ValueError:
        # If it fails, raise an exception with an error message
        error_msg = '\'%s\' is not a positive integer' % string
        raise ap.ArgumentTypeError(error_msg)
    
    # If the integer conversion worked, make sure it's positive
    if value <= 0:
        # If not, raise an exception and tell the user
        error_msg = '%d is not a positive integer' % value
        raise ap.ArgumentTypeError(error_msg)
    
    return value

def parse_args():
    """
    Uses argparse to parse the specific arguments for minerva. THIS IS NOT THE
    SAME AS THE ARGPARSE MODULE'S ARG_PARSE() FUNCTION; there just happens to
    be no better way to name a function that parses arguments.
    """
    # Create a new parser object, which we'll add the arguments to
    parser = ap.ArgumentParser(description='Calculates probabilities for Risk')

    parser.add_argument('attackers', type=positive_int,
        help='number of attackers in the attack scenario')

    # Defenders can be a list (for campaigns)
    parser.add_argument('defenders', type=positive_int, nargs='+',
        help='defender troop count(s) in the attack scenario')

    parser.add_argument('-r', '--retreat', type=positive_int, default=0,
        metavar='R',
        help='represents when the attacker will retreat. Any scenarios in which '
             'the attacking force reaches or falls below this number of units are '
             'counted as unsuccessful by the program.')

    parser.add_argument('-g', '--goal', type=positive_int, default=0, metavar='G',
        help='number of troops the attacker wishes to reduce the defending army '
             'to. Any outcomes in which the defender\'s army size reaches or '
             'falls below this number are counted as successful by the program.')

    parser.add_argument('-i', '--interactive', action='store_true',
        help='use interactive mode. The program will prompt the user for updates '
             'to the invasion, then outputs an updated probability of success.')

    parser.add_argument('-v', '--verbose', action='store_true',
        help='verbosely print probabilities and unit counts')

    # Parse the arguments
    options = parser.parse_args();

    # Error Checking
    # Make sure the user didn't use options incompatible with campaign mode
    if len(options.defenders) > 1:
        if goal != 0:
            error_msg = '\'-g\' is incompatible with multiple defender troop counts'
            parser.error(error_msg)
        elif options.interactive:
            error_msg = 'no interactive mode for multiple defender troop counts (yet)'
            parser.error(error_msg)
        elif options.verbose:
            error_msg = 'no verbose mode for multiple defender troop counts (yet)'
            parser.error(error_msg)

    # Make sure that the minimums are less than the troop numbers
    if not options.retreat < options.attackers:
        error_msg = 'the argument \'retreat\' must be less than \'attackers\''
        parser.error(error_msg)

    # We can assume defenders has only 1 value if goal is set
    if not options.goal < options.defenders[0]:
        error_msg = 'the argument \'goal\' must be less than \'defenders\''
        parser.error(error_msg)
    
    # Finally, return the arguments
    return options

def run():
    """
    I just stuffed the rest of main's code into this function to fix th issue
    with the setup.py for now. I'll make it pretty later.
    """
    # Get args from our parse_args function (which uses the argparse module)
    args = parse_args()
    
    attackers = args.attackers
    defenders = args.defenders
    
    retreat = args.retreat
    goal = args.goal
    
    interactive = args.interactive
    verbose = args.verbose
    
    # parse_args() handles the error-checking, so we're good to go
    
    # If there's more than 1 defending territory, it's campaign mode
    if len(defenders) > 1:
        print_campaign(attackers, defenders, retreat)
        odds = calculate_campaign(attackers, defenders, retreat)
        print_campaign_odds(odds)
    # If there's only 1 territory, it's standard or interactive mode
    else:
        # Extract the single defender value from the array
        defenders = defenders[0]
        
        if interactive:
            interactive_invasion(attackers, defenders, retreat, goal, verbose)
        else:
            print_invasion(attackers, defenders, retreat, goal, verbose)
            odds = calculate_invasion(attackers, defenders, retreat, goal)
            print_invasion_odds(odds, goal, verbose)
