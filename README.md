# EECS 581 Project 1 Battleship

Battleship is a 2-player game where each player can position ships of various sizes (identical to their opponent's fleet) whereever they wish on a grid-based board.

During each round, the active player selects a grid position to fire at. If the selected grid position aligns with that of an enemy ship, that ship is damaged.

Once every slot of a given ship has been hit, the ship will sink.

Once all ships of a given player have been sunk, the game ends, and the player with one or more remaining ships is declared the winner.

This game is designed to be run on a single device, players are expected to hand off control of the device between rounds.

# Pygame (Prerequisite)
To run this game, you will be required to install Pygame.

Assuming you already have Python installed, and have pip installed (usually pre-installed with Python), you should be able to simply run the following command in Command Prompt, Powershell, or Terminal depending on your OS:

`pip install pygame`

If that didn't work, you can find more detailed instructions to install Pygame [here](https://pypi.org/project/pygame/).

# Documentation Instructions
Documentation was generated using Doxygen.

You can view this documentation by opening the .html files found in _./documentation/html/_. Commonly starting with the index.html file:

_./documentation/html/index.html_

It is recommended to view these .html files after the repository is downloaded to a system, so that the .html files may be viewed properly in a browser.

From there, you can either click on the Namespaces tab near the top to access other pages, or you can use the search bar in the top right to search through documentation directly.

# Playing The Game
To play Battleship, run the following command in Command Prompt/Powershell/Terminal from the project's directory:

`python main.py`

Assuming Python and Pygame are installed correctly, you should see a window containing instructions on how to play the game.

As this game is designed to be run on a single device, players are expected to hand off control of the device between rounds.

When one player has sunk the other's entire fleet of ships, the game ends.

# What is main_.py?
`main_.py` (not to be confused with `main.py`) is a "test" file that was used during initial development for experimental features.

Effectively, it was a separate branch intended to be merged into the main branch when ready.

# Score Board Implementation:

The Game gives players a hundred points when they hit a ship and subtracts 1 point when a player misses.  Scores are only entered to the leaderboard by the winner of a game.

# Version History

1.1 --  Refactored code to accomadate new AI menu and added AI ship placement, empty functions for future AI and Score features 
Clarified Code Comments

1.3 -- Impelemented Easy AI that randomly attacks unshot at tiles 
Clarified Code Comments

1.5 -- Impelemented Medium AI that randomly attacks until it hits a ship and then checks the tiles around a hit to better target large ships
Clarified Code Comments

1.7  -- Implemented simple leaderboard to test functionality
Clarified Code Comments

1.8 -- Implemented Hard AI that targets player 1's ships directly to play perfect games.
Clarified Code Comments
