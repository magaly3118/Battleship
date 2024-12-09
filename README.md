# Battleship
## Overview
### Description
Battleship is a 2-player game where each player can position ships of various sizes (identical to their opponent's fleet) whereever they wish on a grid-based board.

During each round, the active player selects a grid position to fire at. If the selected grid position aligns with that of an enemy ship, that ship is damaged.

If every slot of a given ship has been hit, the ship will sink.

Once all ships of a given player have been sunk, the game ends, and the player with one or more remaining ships is declared the winner.

### Features
The game has two playing modes: player-vs-AI and player-vs-player. 

Additionally, players get 100 points when they hit a ship and get penalized 1 point when they miss. When a player wins a game, their score is entered on the leaderboard.

## How To Play
### Prerequisite: Pygame
To run this game, you will be required to install Pygame.

Assuming you already have Python installed, and have pip installed (usually pre-installed with Python), you should be able to simply run the following command in Command Prompt, Powershell, or Terminal depending on your OS:

```
pip install pygame
```

If that didn't work, you can find more detailed instructions to install Pygame [here](https://pypi.org/project/pygame/).

### Running the Game
To play Battleship, run the following command in Command Prompt/Powershell/Terminal from the project's directory:

`python main.py`

Assuming Python and Pygame are installed correctly, you should see a window containing instructions on how to play the game.

Note that as this game is designed to be run on a single device, players are expected to hand off control of the device between rounds in player-vs-player mode.

## About the Source Code
### What is main_.py?
`main_.py` (not to be confused with `main.py`) is a "test" file that was used during initial development for experimental features.

Effectively, it was a separate branch intended to be merged into the main branch when ready.

### Documentation
Some of the documentation was generated using Doxygen. To view this documentation, open the HTML files found in `./documentation/html/`. We recommend starting with the index file located at `./documentation/html/index.html`. 

From there, you can either click on the Namespaces tab near the top to access other pages, or you can use the search bar in the top right to search through documentation directly.

For a better experience, view these files in a browser after downloading the repository.

## Contributors
This repository was forked from Team 24's [Battleship](https://github.com/maelikax/EECS581_Project1). The features added by Team 21 were the scoreboard, the leaderboard, the player-vs-AI mode, and some additional menus needed for these.

#### Team 24
<a href="https://github.com/Gatimio" target="_blank" title="Gatimio">
  <img src="https://github.com/Gatimio.png?size=40" height="40" width="40" alt="Gatimio" />
</a>
<a href="https://github.com/sbuehler7524" target="_blank" title="sbuehler7524">
  <img src="https://github.com/sbuehler7524.png?size=40" height="40" width="40" alt="sbuehler7524" />
</a>
<a href="https://github.com/maelikax" target="_blank" title="maelikax">
  <img src="https://github.com/maelikax.png?size=40" height="40" width="40" alt="maelikax" />
</a>
<a href="https://github.com/andrewvand02" target="_blank" title="andrewvand02">
  <img src="https://github.com/andrewvand02.png?size=40" height="40" width="40" alt="andrewvand02" />
</a>
<a href="https://github.com/swagranger011" target="_blank" title="swagranger011">
  <img src="https://github.com/swagranger011.png?size=40" height="40" width="40" alt="swagranger011" />
</a>


#### Team 21
<a href="https://github.com/manvirk21" target="_blank" title="manvirk21">
  <img src="https://github.com/manvirk21.png?size=40" height="40" width="40" alt="manvirk21" />
</a>
<a href="https://github.com/MatthewMcManness" target="_blank" title="MatthewMcManness">
  <img src="https://github.com/MatthewMcManness.png?size=40" height="40" width="40" alt="MatthewMcManness" />
</a>
<a href="https://github.com/magaly3118" target="_blank" title="magaly3118">
  <img src="https://github.com/magaly3118.png?size=40" height="40" width="40" alt="magaly3118" />
</a>
<a href="https://github.com/mariamoraby9" target="_blank" title="mariamoraby9">
  <img src="https://github.com/mariamoraby9.png?size=40" height="40" width="40" alt="mariamoraby9" />
</a>
<a href="https://github.com/ShravyaMatta3" target="_blank" title="ShravyaMatta3">
  <img src="https://github.com/ShravyaMatta3.png?size=40" height="40" width="40" alt="ShravyaMatta3" />
</a>
