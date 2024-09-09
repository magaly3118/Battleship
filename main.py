"""

Authors: Abhishek Bhatt [KU ID], Samuel Buehler [KU ID], Collins Gatimi [KU ID], Mikaela Navarro [2998217], Andrew Vanderwerf [3075534]

Date Created: 09/09/24
Date Last Modified: 09/09/24

Program Tile: Battleship
Program Description: Create a game where two players can place their ships on their grid and try to hit each other's ships by guessing the ships' location on the grid. The first player to sink all the opponent's ships wins.

Sources: YouTube
Inputs:
Output:

"""
# Import modules
import pygame

# Run game
def runGame():
    # Set up Pygame, initialize size of screen, have users able to open/close game
    pygame.init()

    screen_width = 1200
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

# Grid for player to guess other player's location
def grid1():
    pass

# Grid for player to place their ships
def grid2():
    pass

# Create ships
def createShips():
    pass

# Place ships
def placeShips():
    pass

# Count hits
def countHits():
    pass

# Count misses
def countMisses():
    pass

# Blank screen when switching turns
def endTurn():
    pass

runGame()
