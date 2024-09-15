"""

Authors: Abhishek Bhatt [3086901], Samuel Buehler [3031928], Collins Gatimi [2791182], Mikaela Navarro [2998217], Andrew Vanderwerf [3075534]

Date Created: 09/09/24
Date Last Modified: 09/15/24

Program Tile: Battleship
Program Description: Create a game where two players can place their ships on their grid and try to hit each other's ships by guessing the ships' location on the grid. The first player to sink all the opponent's ships wins.

Sources: YouTube, ChatGPT
Inputs:User mouse/key inputs
Output:Game screen

"""
# Import modules
import pygame

# Initialize pygame
pygame.init() 
pygame.mixer.init()#Init for music/sound

# Load sounds
hit_sound = pygame.mixer.Sound("assets/hit_sound.wav") #Sound for when a ship is hit
miss_sound = pygame.mixer.Sound("assets/miss_sound.wav") #Sound for when a miss happens
sunk_sound = pygame.mixer.Sound("assets/sunk_sound.wav") #Sound for when a ship is sunk
win_sound = pygame.mixer.Sound("assets/win_sound.wav") #Sound for when the game ends
# Set up display
WIDTH, HEIGHT = 1200, 600 #Screen width/height
win = pygame.display.set_mode((WIDTH, HEIGHT)) #Sets the dimensions for the window
pygame.display.set_caption("2-Player Battleship") #Caption for the screen

# Define colors
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (169, 169, 169)
GHOST_COLOR = (200, 200, 200)
BLUE = (0, 0, 255)  # Color for sunk ships on the ship grids
# Grid settings
CELL_SIZE = 40 #Cell size for each cell in the grid
GRID_SIZE = 10 #10x10 grid
MARGIN = 50

# Load ship images
ship_images = {
    1: pygame.image.load("assets/ship_1.png"),
    2: pygame.image.load("assets/ship_2.png"),
    3: pygame.image.load("assets/ship_3.png"),
    4: pygame.image.load("assets/ship_4.png"),
    5: pygame.image.load("assets/ship_5.png")
}

# Resize the ship images to fit the grid cells
for key in ship_images:
    ship_images[key] = pygame.transform.scale(ship_images[key], (CELL_SIZE, CELL_SIZE)) 

# Initialize grids for both players
grid1 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Player 1 ship grid
missile_board1 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Player 1 missile grid
grid2 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Player 2 ship grid
missile_board2 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Player 2 missile grid

# Default ship lengths
default_ships = [1, 2, 3, 4, 5]

font = pygame.font.Font(None, 36) #Setting the font for text in the game

def draw_grid(grid, x_offset, y_offset, player_grid=True, ghost_positions=None):
    """Draw the game grid, including ships, hits, misses, and ghost ship if present."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE #Default color before hit/miss or a ship is white
            if player_grid:  # For the player's own grid
                if grid[row][col] == 1:  # Placeholder, would color black for ships, but we filled in with png instead below
                    color = BLACK
                elif grid[row][col] == 2:  # Color red for hit
                    color = RED
                elif grid[row][col] == 3:  # #Color blue for sunk ship
                    color = BLUE
            else:  # For the missile board
                if grid[row][col] == 1:  # Color grey for miss
                    color = GREY
                elif grid[row][col] == 2:  # Color red for hit
                    color = RED
                elif grid[row][col] == 3:  # Color green for sunk enemy ship
                    color = GREEN

            if ghost_positions and (row, col) in ghost_positions: #Colors the grid grey for placement so that players can see where the ship is placed before placing it
                color = GHOST_COLOR

            pygame.draw.rect(win, color, (x_offset + col * CELL_SIZE, y_offset + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)#draws the cells into the grid based on their color determined above
            pygame.draw.rect(win, BLACK, (x_offset + col * CELL_SIZE, y_offset + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            if player_grid and grid[row][col] == 1:  # Draw ship images only on player's own grid
                ship_len = get_ship_length_from_position(grid, row, col) #finds value of ship length
                if ship_len and ship_len in ship_images: #checks if there is a ship in ship_images corresponding to the length of the given ship
                    win.blit(ship_images[ship_len], (x_offset + col * CELL_SIZE, y_offset + row * CELL_SIZE))#puts in the pngs into the given cells

def get_ship_length_from_position(grid, row, col):
    """Return the length of the ship at the given grid position, if any."""
    if grid[row][col] == 1: #If there is a ship value, which is 1 on the grid
        for ship_len in default_ships: #either 1,2,3,4,5 length ship based on battleship game
            if all(
                (col + i < GRID_SIZE and grid[row][col + i] == 1) or #Checks for length of ship vertically
                (row + i < GRID_SIZE and grid[row + i][col] == 1) #Checks for length of ship horizontally
                for i in range(ship_len) 
            ):
                return ship_len #Returns back ship length
    return None

def place_ship(grid, start_row, start_col, ship_len, orientation, ship_list):
    """Place a ship manually based on the start position and orientation and track the ship coordinates."""
    ship_coordinates = []
    if orientation == "H": #If player selects horizontal placement
        if start_col + ship_len <= GRID_SIZE: #Checks if valid placement
            if all(grid[start_row][start_col + i] == 0 for i in range(ship_len)): #checks if ship is already there
                for i in range(ship_len): #Replaces values in grid with 1 to mark player ship
                    grid[start_row][start_col + i] = 1
                    ship_coordinates.append((start_row, start_col + i)) #Coordinates of length of ship
                ship_list.append({'coordinates': ship_coordinates, 'hits': []}) #Appends shiplist with info on ship
                return True
    else: #If player selects vertical placement
        if start_row + ship_len <= GRID_SIZE: #Checks if valid placement
            if all(grid[start_row + i][start_col] == 0 for i in range(ship_len)): #checks if ship is already there
                for i in range(ship_len): #replaces values in grid with 1 to mark player ship
                    grid[start_row + i][start_col] = 1
                    ship_coordinates.append((start_row + i, start_col)) #Coordinates of length of ship
                ship_list.append({'coordinates': ship_coordinates, 'hits': []}) #Appends shiplist with info on ship
                return True
    return False

def get_ghost_positions(grid, start_row, start_col, ship_len, orientation):
    """Calculate the ghost ship positions based on mouse hover."""
    ghost_positions = []
    if orientation == "H": #If player is in horizontal placement mode
        if start_col + ship_len <= GRID_SIZE:
            ghost_positions = [(start_row, start_col + i) for i in range(ship_len)]#Marks positions where ghost cell should be present
    else: #If player is in vertical placement mode
        if start_row + ship_len <= GRID_SIZE:
            ghost_positions = [(start_row + i, start_col) for i in range(ship_len)]#Marks position where ghost cell should be present
    return ghost_positions

def ship_placement_menu(player_grid, player_number, ship_list, ships_to_place):
    """Allow player to place ships manually with a ghost version of the ship."""
    placing_ships = True #Process still ongoing
    ship_idx = 0 #Counting variable 
    orientation = "H" #Default placement orientation is horizontal
    ghost_positions = []

    while placing_ships: #While player is still in the process of placing ships
        win.fill(BLACK) 
        draw_text(f"Player {player_number}: Place your ships", WIDTH // 2 - 100, 50) #WHich player is placing ships
        draw_text(f"Current ship length: {ships_to_place[ship_idx]}", WIDTH // 2 - 100, 100) #Displays current ship length
        draw_text("Press 'H' for Horizontal, 'V' for Vertical", WIDTH // 2 - 100, 150) #Displays info for player so they know what to press to change orientation

        mouse_x, mouse_y = pygame.mouse.get_pos() #Get position of player mouse
        if MARGIN < mouse_x < MARGIN + GRID_SIZE * CELL_SIZE and MARGIN < mouse_y < MARGIN + GRID_SIZE * CELL_SIZE: #Basically just means "if player is hoveirng over the placement grid"
            row = (mouse_y - MARGIN) // CELL_SIZE #Finds which row player is hovering over
            col = (mouse_x - MARGIN) // CELL_SIZE #Finds which col player is hovering over
            ghost_positions = get_ghost_positions(player_grid, row, col, ships_to_place[ship_idx], orientation) #Feeds those to ghost position function so it can draw those on the grid

        draw_grid(player_grid, MARGIN, MARGIN, ghost_positions=ghost_positions) #Draw the placement grid

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #If player quits game
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: #If player touches any key
                if event.key == pygame.K_h: #If that key is an H
                    orientation = "H"
                if event.key == pygame.K_v:#If that key is a V
                    orientation = "V"
            if event.type == pygame.MOUSEBUTTONDOWN: #If player places
                if ghost_positions: #If player is hovering over grid
                    start_row, start_col = ghost_positions[0] #Coordinates to place based on player mouse position
                    if place_ship(player_grid, start_row, start_col, ships_to_place[ship_idx], orientation, ship_list): #if player places a ship and it was valid and went through
                        ship_idx += 1 #Increments every time player places a ship to track number of ships placed
                        if ship_idx == len(ships_to_place): #If player has placed the number of ships for the game
                            placing_ships = False #Stop process
                            break

def check_hit(ship_grid, missile_board, row, col, ship_list):
    """Check if a ship is hit and update both the missile board and the player's ship grid.
       If a ship is sunk, mark it differently."""
    if missile_board[row][col] != 0:  # If the cell has already been targeted, return False
        return False

    if ship_grid[row][col] == 1:  # A ship is hit
        missile_board[row][col] = 2  # Mark hit on the missile board
        hit_sound.play()
        ship_grid[row][col] = 2  # Mark hit on the player's ship grid

        for ship in ship_list:
            if (row, col) in ship['coordinates']:
                ship['hits'].append((row, col))  # Record the hit
                
                # Check if the ship is sunk
                if len(ship['hits']) == len(ship['coordinates']):
                    for (r, c) in ship['coordinates']:
                        missile_board[r][c] = 3  # Mark the ship as sunk on the missile board
                        ship_grid[r][c] = 3  # Mark the ship as sunk on the player's ship grid
                        sunk_sound.play()

        return True  # A valid shot was made
    else:
        missile_board[row][col] = 1  # Mark miss on the missile board
        miss_sound.play()
    return True  # Return True since it was a valid shot


def main_menu():
    """Main menu to select the number of ships."""
    selected_ships = 3 #Default value
    menu_running = True

    while menu_running:
        win.fill(BLACK)
        draw_text("Welcome to 2-Player Battleship", WIDTH // 2 - 150, HEIGHT // 2 - 100) #Just info for users so they know how to use the 
        draw_text(f"Number of Ships: {selected_ships}", WIDTH // 2 - 100, HEIGHT // 2)
        draw_text("Use UP and DOWN arrow keys to select the number of ships.", WIDTH // 2 - 300, HEIGHT // 2 + 50)
        draw_text("Press ENTER to start", WIDTH // 2 - 100, HEIGHT // 2 + 200)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: #If a keyboard stroke is detected
                if event.key == pygame.K_UP and selected_ships < len(default_ships): #If up arrow key is pressed and we aren't at maximum of 5 ships
                    selected_ships += 1 #Increment 1
                elif event.key == pygame.K_DOWN and selected_ships > 1: #if down arrow up is pressed and we aren't at minimum of 1 ships yet
                    selected_ships -= 1 #increment down 1
                elif event.key == pygame.K_RETURN: #If enter, close this menu
                    menu_running = False
                    break

    return selected_ships #Return number of ships to use in game

def display_winner(winner):
    """Display the winner and wait for user input to close the game."""
    win.fill(BLACK)
    draw_text(f"Player {winner} Wins!", WIDTH // 2 - 100, HEIGHT // 2 - 50) #Displays which player won
    draw_text("Press ENTER to exit", WIDTH // 2 - 100, HEIGHT // 2 + 50) #Enter to quit game
    pygame.display.flip()

    waiting_for_input = True #waiting for user input
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: #If player presses enter, quit the game
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    quit()
def display_turn_screen(player_number):
    """Screen in between turns to hide board info from other player."""
    win.fill(BLACK)
    draw_text(f"Player {player_number}'s Turn", WIDTH // 2 - 150, HEIGHT // 2 - 50) #Current players turn, suppose to hand off laptop to them when they get to this screen
    draw_text("Please wait for the other player to finish their turn.", WIDTH // 2 - 300, HEIGHT // 2 + 10)
    draw_text("Press any key to continue...", WIDTH // 2 - 150, HEIGHT // 2 + 70)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: #any key is pressed
                waiting = False #Stop waiting, go onto next turn
                break
def draw_text(text, x, y):
    """Utility function to draw text on the screen."""
    text_surface = font.render(text, True, WHITE) #White text
    win.blit(text_surface, (x, y))#Draws on window the text, with coordinates

def all_ships_sunk(ship_list):
    """Check if all ships in the list are sunk."""
    return all(len(ship['hits']) == len(ship['coordinates']) for ship in ship_list)#checks if all ships have the same number of hits as they have length, which would mean they are all sunk

def display_winner(winner):
    """Display the winner and wait for user input to close the game."""
    win.fill(BLACK)
    draw_text(f"Player {winner} Wins!", WIDTH // 2 - 100, HEIGHT // 2 - 50) #Winning player 
    draw_text("Press ENTER to exit", WIDTH // 2 - 100, HEIGHT // 2 + 50) 
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input: #While waiting for keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: #Quit game if they press enter
                    pygame.quit()
                    quit()
def instructions_page():
    """Display the game instructions to the player."""
    instructions_running = True
    while instructions_running:#While player hasn't moved on from instructions by pressing enter
        win.fill(BLACK)

        # Display the instructions, just explains game mechanics and what colors mean
        draw_text("Instructions", WIDTH // 2 - 100, 50)
        draw_text("1. Place your ships on the grid.", WIDTH // 2 - 300, 150)
        draw_text("2. On your turn, try to hit the enemy's ships by clicking on the missile board.", WIDTH // 2 - 300, 200)
        draw_text("3. Colors:", WIDTH // 2 - 300, 250)
        draw_text("- Purple: Your ship", WIDTH // 2 - 300, 300)
        draw_text("- Grey: Missed shot", WIDTH // 2 - 300, 350)
        draw_text("- Red: Hit", WIDTH // 2 - 300, 400)
        draw_text("- Green: Sunk enemy ship", WIDTH // 2 - 300, 450)
        draw_text("- Blue: Sunk friendly ship", WIDTH // 2 - 300, 500)
        draw_text("Press ENTER to continue...", WIDTH // 2 - 100, HEIGHT - 50)

        pygame.display.flip()

        # Wait for the player to press a key to proceed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: #If player presses enter to move on 
                    instructions_running = False  # Exit the instruction page
                    break

def game_loop():
    """Main game loop where players place ships and play the game."""
    # Main menu to select the number of ships
    instructions_page()#Start instructions page
    num_ships = main_menu()#start main menu, which also grabs our number of ships for the game

    # Initialize ship lists for both players
    player1_ships = []
    player2_ships = []

    # Ships to place based on the selection
    ships_to_place = default_ships[:num_ships]

    # Player 1 places ships
    ship_placement_menu(grid1, 1, player1_ships, ships_to_place)

    # Player 2 places ships
    ship_placement_menu(grid2, 2, player2_ships, ships_to_place)

    # Main game loop after ship placement
    running = True
    turn = 1  # Player 1 starts
    while running:
        win.fill(BLACK)
        
        if turn == 1:
            # Display Player 1's missile board (targeting Player 2's ships)

            draw_text("Your Ships", MARGIN + 100, MARGIN - 40)  # Above Player 1's ship grid
            draw_text("Missile Board", WIDTH // 2 + MARGIN + 100, MARGIN - 40)  # Above Player 1's missile board
            draw_text("Player 1's Turn", WIDTH // 2 - 130, 20)
            draw_grid(missile_board1, WIDTH // 2 + MARGIN, MARGIN, player_grid=False)
            # Display Player 1's own ship grid with hits and sunk ships
            draw_grid(grid1, MARGIN, MARGIN, player_grid=True)
        else:
            # Display Player 2's missile board (targeting Player 1's ships)
            draw_text("Your Ships", MARGIN + 100, MARGIN - 40)  # Above Player 2's ship grid
            draw_text("Missile Board", WIDTH // 2 + MARGIN + 100, MARGIN - 40)  # Above Player 2's missile board
            draw_text("Player 2's Turn", WIDTH // 2 - 130, 20)
            draw_grid(missile_board2, WIDTH // 2 + MARGIN, MARGIN, player_grid=False)
            # Display Player 2's own ship grid with hits and sunk ships
            draw_grid(grid2, MARGIN, MARGIN, player_grid=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:#If they click the mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()#Gets mouse position
                if turn == 1: 
                    # Check if Player 1 clicks on the missile board area
                    if (WIDTH // 2 + MARGIN < mouse_x < WIDTH // 2 + MARGIN + GRID_SIZE * CELL_SIZE and 
                        MARGIN < mouse_y < MARGIN + GRID_SIZE * CELL_SIZE): #Checks if where they clicked was on the misisle board area
                        row = (mouse_y - MARGIN) // CELL_SIZE #Finds row where they clicked
                        col = (mouse_x - (WIDTH // 2 + MARGIN)) // CELL_SIZE #Finds col where they clicked
                        if check_hit(grid2, missile_board1, row, col, player2_ships):#If they fired at a valid position
                            # Check if Player 1 has won
                            if all_ships_sunk(player2_ships): #If all player 2 ships sunk after player 1 fires
                                win_sound.play()
                                display_winner(1)  # Player 1 wins
                                running = False
                            else:
                                # Show screen to switch turns and switch to Player 2
                                display_turn_screen(2)
                                turn = 2  # Switch to Player 2
                elif turn == 2:
                    # Check if Player 2 clicks on the missile board area
                    if (WIDTH // 2 + MARGIN < mouse_x < WIDTH // 2 + MARGIN + GRID_SIZE * CELL_SIZE and 
                        MARGIN < mouse_y < MARGIN + GRID_SIZE * CELL_SIZE): #Checks if where they clicked was in the missile board area
                        row = (mouse_y - MARGIN) // CELL_SIZE #Finds row where they clicked
                        col = (mouse_x - (WIDTH // 2 + MARGIN)) // CELL_SIZE #Finds col where they clicked
                        if check_hit(grid1, missile_board2, row, col, player1_ships): #If they fired at a valid position
                            # Check if Player 2 has won
                            if all_ships_sunk(player1_ships):
                                win_sound.play()
                                display_winner(2)  # Player 2 wins
                                running = False
                            else:
                                # Show screen to switch turns and switch to Player 1
                                display_turn_screen(1)
                                turn = 1  # Switch to Player 1

    pygame.quit()



if __name__ == "__main__":
    game_loop()

