# QultureRocksChallenge-checkers
This is a Checkers Game implementation as the solution to the Qulture Rocks's challenge

## Prerequisites
- python
- pygame python library

## Installing pygame
### Run the following command on a linux terminal:
python3 -m pip install -U pygame --user

## To execute the game
### Inside the project's folder, run the following command on a linux terminal:
python3 main.py
### What should happen
The game screen should apear with the pieces already arranged and ready to play.

## To execute the game's tests
### Inside the project's folder, run the following command on a linux terminal:
python3 tests.py
### What should happen
You should see a few automated test cases run through a screen. If everything is correct, no error messages will apear.

## How to play
### Rules
The game rules can be found at https://pt.wikipedia.org/wiki/Damas
### About the game interface
- To move a piece, you can either dragg it from its tile to the one you desire, or click on top of it and then on the desired tile.
- Once a piece is selected, the game will light up all the legal moves you can make. If no tile did light up, then the piece has no legal moves.
- Messages such as who has the turn and who won the game will be presented via terminal.

## References
https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation
https://www.pygame.org/docs/
https://www.youtube.com/watch?v=FfWpgLFMI7w
