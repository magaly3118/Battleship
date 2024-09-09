"""

Authors: Abhishek Bhatt [KU ID], Samuel Buehler [KU ID], Collins Gatimi [KU ID], Mikaela Navarro [2998217], Andrew Vanderwerf [KU ID]

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

# Set up Pygame, initialize size of screen, have users able to open/close game
pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()