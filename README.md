# Gomoku 
This source code is written in Python and uses Tkinter to create a GUI. Gomoku is a game where opponents place pieces in an attempt to place 5 of the same pieces in a vertical, horizontal, or diagonal order.

The game has two modes, that determine whether the user or machine takes the first turn

## How it works
This program takes a monomial calculation approach. For every piece that is placed, all possible sets of length 5, which contain the selected piece, are generated and stored since it is necessary to complete one of those sets to win the game. 

Every set is distinguished as a favorable or unfavorable set. All points that occur in the sets are then ranked based on their overall occurrence. Each point also receives a completion scored, which is determined based on the completition of the sets that they are part of.

The unfavorable sets are checked and if their score exceeds a certain value, then the program takes a defensive approach. The defensive approach is prioritized. Offensive moves are based off favorable sets and the scores of unfavorable sets.

## Instructions
1. Ensure you Python 3 is installed
1. Download files from this repository
1. Run `python3 gomoku.py`
1. By default the program starts on "Human first" mode, but this can be changed in the options section