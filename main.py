"""

Authors: Abhishek Bhatt [3086901], Samuel Buehler [3031928], Collins Gatimi [2791182], Mikaela Navarro [2998217], Andrew Vanderwerf [3075534]

Updated by: Matthew McManness [2210261], Manvir Kaur [], Magaly Comacho [], Mariam Oraby [], Shravya Matta []
Date Created: 09/09/24
Date Last Modified: 09/19/24

Program Tile: Battleship
Program Description: Create a game where two players can place their ships on their grid and try to hit each other's ships by guessing the ships' location on the grid. The first player to sink all the opponent's ships wins.
Update Description: Added 3 AI difficulties and a persistant scoreboard.

Sources: YouTube, ChatGPT
Inputs:User mouse/key inputs
Output:Game screen

"""
# Import modules
import pygame
import random

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

# New Functions:

def select_game_mode():

    # present a menu to select between pass and play mode or AI mode.
    # Returns a string (either "pass_and_play" or "AI")
    game_mode = "pass_and_play" # Default
    menu_running = True

    while menu_running:
        win.fill(BLACK)

        # Display menu options:
        draw_text("Select Game Mode", WIDTH // 2 - 150, HEIGHT // 2 - 100)
        draw_text(f"Current selection: {game_mode}", WIDTH // 2 - 100, HEIGHT // 2)
        draw_text("Use LEFT/RIGHT arrows to change mode", WIDTH // 2 - 200, HEIGHT // 2 + 50)
        draw_text("Press ENTER to confirm", WIDTH // 2 - 100, HEIGHT // 2 + 100)

        pygame.display.flip()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        # Toggle between 'pass_and_play' and 'AI'
                        if game_mode == "pass_and_play":
                            game_mode = "AI"
                        else:
                            game_mode = "pass_and_play"

                    if event.key == pygame.K_RETURN:
                        # Confirm selection and exit menu
                        menu_running = False

    return game_mode

def select_ai_difficulty():

    # Presents a menu to select the AI Level
    # Returns: A string indicating the AI difficulty ("easy", "medium", "hard")

    ai_difficulty = "easy"  # Default
    menu_running = True

    while menu_running:
        win.fill(BLACK)

        # Display the difficulty selection menu
        draw_text("Select AI Difficulty", WIDTH // 2 - 150, HEIGHT // 2 - 100)
        draw_text(f"Current selection: {ai_difficulty}", WIDTH // 2 - 100, HEIGHT // 2)
        draw_text("Use LEFT/RIGHT arrows to change difficulty", WIDTH // 2 - 200, HEIGHT // 2 + 50)
        draw_text("Press ENTER to confirm", WIDTH // 2 - 100, HEIGHT // 2 + 100)

        pygame.display.flip()

        # Event handling to change the AI difficulty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    # Cycle through difficulties: easy -> medium -> hard -> easy
                    if ai_difficulty == "easy":
                        ai_difficulty = "medium"
                    elif ai_difficulty == "medium":
                        ai_difficulty = "hard"
                    else:
                        ai_difficulty = "easy"

                if event.key == pygame.K_RETURN:
                    # Confirm selection and exit menu
                    menu_running = False

    return ai_difficulty

def place_ai_ships(grid, ships_to_place, player2_ships):
    
    # Automatically places the AI's ships on the grid.
    # Arguments:
    #     - grid: The AI's grid where ships will be placed.
    
    # Define ship lengths (same as player ships)
    for ship_len in ships_to_place:
        placed = False  # Track if the ship was successfully placed
        while not placed:
            # Randomly choose orientation ('H' for horizontal, 'V' for vertical)
            orientation = random.choice(["H", "V"])

            if orientation == "H":
                # Pick random start position where the ship fits horizontally
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - ship_len)
            else:
                # Pick random start position where the ship fits vertically
                row = random.randint(0, GRID_SIZE - ship_len)
                col = random.randint(0, GRID_SIZE - 1)

            # Check if the selected area is free to place the ship
            if check_area_is_free(grid, row, col, ship_len, orientation):
                # Place the ship on the grid and track it in player2_ships (AI's ships)
                ship_coordinates = []  # To store the coordinates of the ship
                place_ship(grid, row, col, ship_len, orientation, player2_ships)

                # After placing, add the ship's coordinates to player2_ships for tracking
                if orientation == "H":
                    ship_coordinates = [(row, col + i) for i in range(ship_len)]
                else:
                    ship_coordinates = [(row + i, col) for i in range(ship_len)]

                player2_ships.append({
                    'coordinates': ship_coordinates,
                    'hits': []  # Initialize an empty hits list for tracking
                })
                placed = True

def check_area_is_free(grid, start_row, start_col, ship_len, orientation):
    
    # Helper function to check if the area is free to place a ship.
    # Returns True if the ship can be placed, False if there's an overlap or out of bounds.
    
    if orientation == "H":
        # Check if any of the cells are already occupied
        for i in range(ship_len):
            if grid[start_row][start_col + i] != 0:
                return False
    else:
        # Check if any of the cells are already occupied
        for i in range(ship_len):
            if grid[start_row + i][start_col] != 0:
                return False

    return True

# Shravya Matta
def update_scoreboard(player_hits, player_misses, player, hit):
     # Add code here
    return #don't have to return anything just diplay info based on player hits, and player misses arrary

# Shravya Matta
def display_scoreboard(player_hits, player_misses):
     # Add code here
    return #don't have to return anything just diplay info based on player hits, and player misses arrary

# Manvir Kaur  
def ai_easy_turn(player_grid, missile_board):
      # Add code here
      # return row, col #(uncomment this the other return is so that people can test without correct code here)
    return
# Magaly Comacho
def ai_medium_turn(player_grid, missile_board):
      # Add code here
      # return row, col #(uncomment this the other return is so that people can test without correct code here)
    return

# Mariam Oraby
def ai_hard_turn(player_grid, missile_board):
      # Add code here
      # return row, col #(uncomment this the other return is so that people can test without correct code here)
    return


def draw_grid(grid, x_offset, y_offset, player_grid=True, ghost_positions=None):
    """Draw the game grid, including ships, hits, misses, and ghost ship if present."""
    
    for row in range(GRID_SIZE):
        draw_text(str(row), x_offset-20, y_offset + row * CELL_SIZE + (CELL_SIZE / 4)) # Draws row label
        for col in range(GRID_SIZE):
            draw_text(chr(65+col), x_offset + col * CELL_SIZE + (CELL_SIZE / 3), y_offset-25) # Draws col label
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

        # Check if the hit was on a specific ship and append the hit to the ship's 'hits' list
        for ship in ship_list:
            if (row, col) in ship['coordinates']:
                if (row, col) not in ship['hits']:  # Avoid double-counting hits
                    ship['hits'].append((row, col))
                    print(f"AI hit registered on Player's ship at {row}, {col}")  # Debug: AI hit

                # Check if the ship is sunk
                if len(ship['hits']) == len(ship['coordinates']):
                    print(f"AI sunk Player's ship at {ship['coordinates']}!")  # Debug: AI ship sunk
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
        draw_text("Welcome to Battleship", WIDTH // 2 - 150, HEIGHT // 2 - 100) #Just info for users so they know how to use the 
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

def display_turn_screen(player_number, game_mode=None):
    """Screen in between turns to hide board info from other player."""
    
    if game_mode == "AI" and player_number == 2:
        turn_text = "AI's Turn"
    else:
        turn_text = f"Player {player_number}'s Turn"
    
    win.fill(BLACK)
    draw_text(turn_text, WIDTH // 2 - 150, HEIGHT // 2 - 50)  # Display the appropriate turn text
    draw_text("Please wait for the other player to finish their turn.", WIDTH // 2 - 300, HEIGHT // 2 + 10)
    draw_text("Press any key to continue...", WIDTH // 2 - 150, HEIGHT // 2 + 70)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # any key is pressed
                waiting = False  # Stop waiting, go on to next turn
                break

def draw_text(text, x, y):
    """Utility function to draw text on the screen."""
    text_surface = font.render(text, True, WHITE) #White text
    win.blit(text_surface, (x, y))#Draws on window the text, with coordinates

def all_ships_sunk(ship_list):
    """Check if all ships in the list are sunk."""
    result = all(len(ship['hits']) == len(ship['coordinates']) for ship in ship_list)
    print(f"All ships sunk check: {result}")  # Debug: Win condition check
    return result

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
    instructions_page()  # Start instructions page
    game_mode = select_game_mode()  # Select game mode (AI or pass-and-play)
    if game_mode == "AI":
        ai_difficulty = select_ai_difficulty()  # Select AI difficulty

    num_ships = main_menu()  # Select number of ships
    player1_ships = []
    player2_ships = []
    ships_to_place = default_ships[:num_ships]

    # Player 1 places ships
    ship_placement_menu(grid1, 1, player1_ships, ships_to_place)

    if game_mode == "pass_and_play":
        # Player 2 places ships manually
        ship_placement_menu(grid2, 2, player2_ships, ships_to_place)
    elif game_mode == "AI":
        # AI places ships automatically
        place_ai_ships(grid2, ships_to_place, player2_ships)

    # Initialize hit/miss counters
    player_hits = {1: 0, 2: 0}
    player_misses = {1: 0, 2: 0}

    running = True
    turn = 1  # Player 1 starts

    while running:
        win.fill(BLACK)
        
        # Handle Player 1's turn
        if turn == 1:
            draw_text("Player 1's Turn", WIDTH // 2 - 130, 20)
            draw_grid(missile_board1, WIDTH // 2 + MARGIN, MARGIN, player_grid=False)
            draw_grid(grid1, MARGIN, MARGIN, player_grid=True)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # Player 1 fires
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (WIDTH // 2 + MARGIN < mouse_x < WIDTH // 2 + MARGIN + GRID_SIZE * CELL_SIZE and
                            MARGIN < mouse_y < MARGIN + GRID_SIZE * CELL_SIZE):
                        row = (mouse_y - MARGIN) // CELL_SIZE
                        col = (mouse_x - (WIDTH // 2 + MARGIN)) // CELL_SIZE
                        if check_hit(grid2, missile_board1, row, col, player2_ships):
                            update_scoreboard(player_hits, player_misses, 1, True)  # Hit
                        else:
                            update_scoreboard(player_hits, player_misses, 1, False)  # Miss
                        if all_ships_sunk(player2_ships):  # Player 1 wins
                            win_sound.play()
                            display_winner(1)
                            running = False
                        else:
                            display_turn_screen(2, game_mode)  # Switch to Player 2
                            turn = 2

        # Handle Player 2's turn (pass-and-play mode)
        elif turn == 2 and game_mode == "pass_and_play":
            draw_text("Player 2's Turn", WIDTH // 2 - 130, 20)
            draw_grid(missile_board2, WIDTH // 2 + MARGIN, MARGIN, player_grid=False)
            draw_grid(grid2, MARGIN, MARGIN, player_grid=True)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # Player 2 fires
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (WIDTH // 2 + MARGIN < mouse_x < WIDTH // 2 + MARGIN + GRID_SIZE * CELL_SIZE and
                            MARGIN < mouse_y < MARGIN + GRID_SIZE * CELL_SIZE):
                        row = (mouse_y - MARGIN) // CELL_SIZE
                        col = (mouse_x - (WIDTH // 2 + MARGIN)) // CELL_SIZE
                        if check_hit(grid1, missile_board2, row, col, player1_ships):
                            update_scoreboard(player_hits, player_misses, 2, True)  # AI Hit
                        else:
                            update_scoreboard(player_hits, player_misses, 2, False)  # AI Miss
                        if all_ships_sunk(player1_ships):  # Player 2 wins
                            win_sound.play()
                            display_winner(2)
                            running = False
                        else:
                            display_turn_screen(1, game_mode)  # Switch back to Player 1
                            turn = 1

        # Handle AI's turn
        elif turn == 2 and game_mode == "AI":
            # AI chooses a move based on difficulty
            if ai_difficulty == "easy":
                row, col = ai_easy_turn(grid1, missile_board2)
            elif ai_difficulty == "medium":
                row, col = ai_medium_turn(grid1, missile_board2)
            elif ai_difficulty == "hard":
                row, col = ai_hard_turn(grid1, missile_board2, player1_ships)

            # AI fires at Player 1's ships
            if check_hit(grid1, missile_board2, row, col, player1_ships):
                update_scoreboard(player_hits, player_misses, 2, True)  # AI Hit
            else:
                update_scoreboard(player_hits, player_misses, 2, False)  # AI Miss
            if all_ships_sunk(player1_ships):  # AI wins
                win_sound.play()
                print("AI wins!")  # Debug: AI wins
                display_winner(2)
                running = False
            else:
                display_turn_screen(1)  # Switch back to Player 1
                turn = 1

        # display scoreboard
        display_scoreboard(player_hits, player_misses)

    pygame.quit()


if __name__ == "__main__":
    game_loop()

