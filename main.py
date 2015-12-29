#!/usr/bin/python3

import argparse as ap
from user_interface import *

# We need to create a special argument conversion function for troop numbers
def positive_int(string):
    """
    positive_int() converts args to positive integers for troop numbers
    """
    # Convert the argument string value to an integer
    try:
        value = int(string)
    except ValueError:
        # If it fails, raise an exception with an error message
        err_msg = '\'%s\' is not a positive integer' % string
        raise ap.ArgumentTypeError(err_msg)
    
    # If the integer conversion worked, make sure it's positive
    if value <= 0:
        # If not, raise an exception and tell the user
        err_msg = '\'%d\' is not a positive integer' % value
        raise ap.ArgumentTypeError(err_msg)
    
    return value

# Create a new parser object, which we'll add the arguments to
parser = ap.ArgumentParser(description='Calculates probabilities for Risk')

# Arguments for number of attackers and defenders
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

# Parse the arguments and extract all important data
options = parser.parse_args();

attackers = options.attackers
defenders = options.defenders

a_min = options.retreat
d_min = options.goal

interactive = options.interactive
verbose = options.verbose

# Make sure that the minimums are less than the troop numbers
# If not, print an error message and exit
if not a_min < attackers:
    error_msg = 'the argument \'retreat\' must be less than \'attackers\''
    parser.error(error_msg)

for d in defenders:
    if not d_min < d:
        error_msg = 'the argument \'goal\' must be less than \'defenders\''
        parser.error(error_msg)

# Now that we've ensured the arguments are valid, let's use them!

# TODO add campaign mode (include argument & help changes above)
# If there's more than 1 defending territory, it's campaign mode
if len(defenders) > 1:
    #TODO make print_campaign() and print_campaign_odds()
    print_campaign(attackers, defenders, a_min)
    odds = calculate_campaign(attackers, defenders, a_min)
    print_campaign_odds(odds)
# TODO fix this crappy decision structure
# Do interactive mode if the user used the -i flag
if interactive:
    interactive_mode(attackers, defenders, a_min, d_min, verbose)
#Otherwise, just calculate and print the odds of success
else:
    print_invasion(attackers, defenders, a_min, d_min, verbose)
    odds = calculate_invasion(attackers, defenders, a_min, d_min)
    print_invasion_odds(odds, d_min, verbose)
