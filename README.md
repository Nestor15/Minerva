# Minerva
Minerva is a tool to calculate probabilities of invasions in the board game
_Risk_. Not only can minerva output the exact probability of success for a
given attack, it can also calculate the probability of winning with a certain
number of troops left and/or wearing the enemy's forces down to a specified
number of units. It also has an interactive mode for reevaluating the
likelihood of an attack's success as it is underway.

##Installation
You will need Python 3 and pip to install minerva.

To install:

    $ cd Minerva/
    $ pip3 install -e .
    $ minerva --help

To install in a virtual environment:

    $ cd Minerva/
    $ pyvenv env
    $ env/bin/pip3 install -e
    $ env/bin/minerva --help

Note: The `-e` means editable mode, where the source files are linked to
instead of copied. This allows you to edit and run them if you wish.

##Usage
###Basic Invasion Success Probability
The most basic function of minerva is calculating an attack's probability of
success.

Suppose the red player planned to invade a territory held by 5 blue units from
a territory containing 12. Because one unit must remain in the attacking
country, Red has an attacking force of 11. To find the likelihood of taking
Blue's territory, Red could run

    $ minerva 11 5
    11 vs. 5
    94.3%

and immediately know his chances of victory.

###Accounting For Retreats
As accurate as the probability given above is, it isn't very helpful.
Experienced _Risk_ players know that while *who* will win an invasion is
usually easy to determine, knowing *how many* troops they will win with is more
difficult but equally important.

In the above scenario, suppose that Red wants not only to take the territory
from Blue, but to hold it afterwards. Red thinks that 7 units are necessary for
this, and so will retreat if his attacking force (not including the one unit
remaining behind) reaches 7 before Blue's forces are eliminated. To find the
probability of taking the territory with at least 7 units, Red could do this:

    $ minerva 11 5 -r 7
    11 vs. 5
    r: 7
    50.7%

In the above command, the -r option is the *retreat value*. This means that any
scenario in which the attacking force shrinks to 7 or less before eliminating
the defenders counts as a loss where the attacker retreats.

###Wearing Down an Opponent's Forces
The program can also do the opposite. In a different scenario, suppose that
Green has 7 units in a territory. In an adjacent territory, Blue has a force of
5 units that Green wants to reduce to 2 so that Red, her ally, can conquer the
territory on his next turn. To find the odds of successfully wearing down the
Blue force to 2 or lower, Green can run this command:

    $ minerva 6 5 -g 2
    6 vs. 5
    g: 2
    80.0%

Now Green knows that, if she's willing to sacrifice her entire attacking force,
she has an 80% chance of reducing Blue's force to only 2 units. The -g option,
the 2 in this command, is the *goal value* of the attack, another name for the
intended number of defenders at the attack's end.

Note that it's possible for Green to reduce Blue's force to 1 below the goal
value (in this case, 1) because 2 units can be lost each round of combat.
These scenarios are included in the probability calculation, so if you intend
to reduce a territory's force without conquering it, use ```-g 2``` instead of
```-g 1```, which would include "accidentally" taking the territory as a
successful outcome.

The goal and retreat value options can be combined. If you want to wear down an
opponent's forces without losing too many of your own, run a command such as

    $ minerva 10 6 -g 2 -r 5
    10 vs. 6
    r: 5
    g: 2
    69.1%

###Interactive Mode
The above uses of minerva are great for evaluating a potential attack, but
aren't very useful once an attack is underway. If you need the odds of success
multiple times for the same invasion, typing an entire command with the
appropriate ```-g``` and ```-r``` arguments can be tedious.

To get up-to-date information on the invasion's chances, use interactive mode.
Interactive mode prompts you for updates to the current state of the battle and
prints an updated probability of success. When using interactive mode, enter
```a``` if the attacker wins a die roll, ```d``` if the defender wins it, or
```t``` if it's a tie (each player loses one unit). Here's an example of
interactive mode in action:

    $ minerva 7 5 -i
    7 vs. 5
    73.6%
    > t
    6 vs. 4
    74.5%
    > a
    6 vs. 2
    93.4%
    > t
    5 vs. 1
    99.0%
    > a
    5 vs. 0

Both the ```-r``` and ```-g``` flags are compatible with interactive mode.
