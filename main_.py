"""

Authors: Abhishek Bhatt [3086901], Samuel Buehler [3031928], Collins Gatimi [2791182], Mikaela Navarro [2998217], Andrew Vanderwerf [3075534]

Date Created: 09/09/24
Date Last Modified: 09/09/24

Program Tile: Battleship
Program Description: Create a game where two players can place their ships on their grid and try to hit each other's ships by guessing the ships' location on the grid. The first player to sink all the opponent's ships wins.

Sources: YouTube
Inputs: User mouse/key inputs
Output: Game screen

"""
# Import modules
import pygame

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1260, 960
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Player Battleship")
font = pygame.font.SysFont('Stencil', 25)

# Load sounds
hit_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
miss_sound = pygame.mixer.Sound("assets/sounds/splash.wav")
shot = pygame.mixer.Sound("assets/sounds/gunshot.wav")
win_sound = pygame.mixer.Sound("assets/sounds/win.wav")

# Load the battleship image
battleship_image = pygame.image.load("assets/images/battleship.png") 
battleship_image = pygame.transform.scale(battleship_image, (WIDTH//2.2, HEIGHT))  

menu_ship = pygame.image.load("assets/images/battleship-logo.png") 
menu_ship = pygame.transform.scale(menu_ship, (WIDTH//1.5, HEIGHT//2.7)) 

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (169, 169, 169)
GHOST_COLOR = (200, 200, 200)
BLUE = (0, 0, 255)  # Color for sunk ships on the ship grids

# Grid settings
CELL_SIZE = 40
GRID_SIZE = 10
MARGIN = 50

# Load ship images
ship_images = {
    1: pygame.image.load("assets/ships/ship_1.png"),
    2: pygame.image.load("assets/ships/ship_2.png"),
    3: pygame.image.load("assets/ships/ship_3.png"),
    4: pygame.image.load("assets/ships/ship_4.png"),
    5: pygame.image.load("assets/ships/ship_5.png")
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

font = pygame.font.Font(None, 36)

def draw_grid(grid, x_offset, y_offset, player_grid=True, ghost_positions=None):
    """Draw the game grid, including ships, hits, misses, and ghost ship if present."""

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE
            if player_grid:  # For the player's own grid
                if grid[row][col] == 1:  # Ship part
                    color = BLACK
                elif grid[row][col] == 2:  # Hit
                    color = RED
                elif grid[row][col] == 3:  # Sunk
                    color = BLUE
            else:  # For the missile board
                if grid[row][col] == 1:  # Miss
                    color = GREY
                elif grid[row][col] == 2:  # Hit
                    color = RED
                elif grid[row][col] == 3:  # Sunk
                    color = GREEN

            if ghost_positions and (row, col) in ghost_positions:
                color = GHOST_COLOR

            pygame.draw.rect(win, color, (x_offset + col * CELL_SIZE, y_offset + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
            pygame.draw.rect(win, BLACK, (x_offset + col * CELL_SIZE, y_offset + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            if player_grid and grid[row][col] == 1:  # Draw ship images only on player's own grid
                ship_len = get_ship_length_from_position(grid, row, col)
                if ship_len and ship_len in ship_images:
                    win.blit(ship_images[ship_len], (x_offset + col * CELL_SIZE, y_offset + row * CELL_SIZE))

def get_ship_length_from_position(grid, row, col):
    """Return the length of the ship at the given grid position, if any."""
    if grid[row][col] == 1:
        for ship_len in default_ships:
            if all(
                (col + i < GRID_SIZE and grid[row][col + i] == 1) or
                (row + i < GRID_SIZE and grid[row + i][col] == 1)
                for i in range(ship_len)
            ):
                return ship_len
    return None

def place_ship(grid, start_row, start_col, ship_len, orientation, ship_list):
    """Place a ship manually based on the start position and orientation and track the ship coordinates."""
    ship_coordinates = []
    if orientation == "H":
        if start_col + ship_len <= GRID_SIZE:
            if all(grid[start_row][start_col + i] == 0 for i in range(ship_len)):
                for i in range(ship_len):
                    grid[start_row][start_col + i] = 1
                    ship_coordinates.append((start_row, start_col + i))
                ship_list.append({'coordinates': ship_coordinates, 'hits': []})
                return True
    else:
        if start_row + ship_len <= GRID_SIZE:
            if all(grid[start_row + i][start_col] == 0 for i in range(ship_len)):
                for i in range(ship_len):
                    grid[start_row + i][start_col] = 1
                    ship_coordinates.append((start_row + i, start_col))
                ship_list.append({'coordinates': ship_coordinates, 'hits': []})
                return True
    return False

def get_ghost_positions(grid, start_row, start_col, ship_len, orientation):
    """Calculate the ghost ship positions based on mouse hover."""
    ghost_positions = []
    if orientation == "H":
        if start_col + ship_len <= GRID_SIZE:
            ghost_positions = [(start_row, start_col + i) for i in range(ship_len)]
    else:
        if start_row + ship_len <= GRID_SIZE:
            ghost_positions = [(start_row + i, start_col) for i in range(ship_len)]
    return ghost_positions

def ship_placement_menu(player_grid, player_number, ship_list, ships_to_place):
    """Allow player to place ships manually with a ghost version of the ship."""
    placing_ships = True
    ship_idx = 0
    orientation = "H"
    ghost_positions = []

    while placing_ships:
        win.fill(BLACK)
        draw_text(f"Player {player_number}: Place your ships", WIDTH // 2 + 20, 50) == pygame.font.SysFont('Stencil', 42)
        draw_text(f"Current ship length: {ships_to_place[ship_idx]}", WIDTH // 2 , 100)
        draw_text("Press 'H' for Horizontal, 'V' for Vertical", WIDTH // 2 + 95, 150)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if MARGIN < mouse_x < MARGIN + GRID_SIZE * CELL_SIZE and MARGIN < mouse_y < MARGIN + GRID_SIZE * CELL_SIZE:
            row = (mouse_y - MARGIN) // CELL_SIZE
            col = (mouse_x - MARGIN) // CELL_SIZE
            ghost_positions = get_ghost_positions(player_grid, row, col, ships_to_place[ship_idx], orientation)

        draw_grid(player_grid, MARGIN, MARGIN, ghost_positions=ghost_positions)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    orientation = "H"
                if event.key == pygame.K_v:
                    orientation = "V"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ghost_positions:
                    start_row, start_col = ghost_positions[0]
                    if place_ship(player_grid, start_row, start_col, ships_to_place[ship_idx], orientation, ship_list):
                        ship_idx += 1
                        if ship_idx == len(ships_to_place):
                            placing_ships = False
                            break

def check_hit(ship_grid, missile_board, row, col, ship_list):
    """Check if a ship is hit and update both the missile board and the player's ship grid.
       If a ship is sunk, mark it differently."""
    if missile_board[row][col] != 0:  # If the cell has already been targeted, return False
        return False

    if ship_grid[row][col] == 1:  # A ship is hit
        missile_board[row][col] = 2  # Mark hit on the missile board
        ship_grid[row][col] = 2  # Mark hit on the player's ship grid

        for ship in ship_list:
            if (row, col) in ship['coordinates']:
                ship['hits'].append((row, col))  # Record the hit

                # Check if the ship is sunk
                if len(ship['hits']) == len(ship['coordinates']):
                    for (r, c) in ship['coordinates']:
                        missile_board[r][c] = 3  # Mark the ship as sunk on the missile board
                        ship_grid[r][c] = 3  # Mark the ship as sunk on the player's ship grid
        pygame.time.wait(500) 
        hit_sound.play()
        pygame.time.wait(1000)
        return True  # A valid shot was made
    else:
        missile_board[row][col] = 1  # Mark miss on the missile board
        pygame.time.wait(500) 
        miss_sound.play()
        pygame.time.wait(1000)
    return True  # Return True since it was a valid shot


def main_menu():
    """Main menu to select the number of ships."""
    selected_ships = 3
    menu_running = True

    while menu_running:
        win.fill(BLACK)

        win.blit(menu_ship, (200, 0)) 

        draw_text("Welcome to 2-Player Battleship", WIDTH // 2 , HEIGHT // 2 - 100)
        draw_text(f"Number of Ships: {selected_ships}", WIDTH // 2 , HEIGHT // 2)
        draw_text("Use UP and DOWN arrow keys to select the number of ships.", WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("Press ENTER to start", WIDTH // 2 , HEIGHT // 2 + 100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_ships < len(default_ships):
                    selected_ships += 1
                elif event.key == pygame.K_DOWN and selected_ships > 1:
                    selected_ships -= 1
                elif event.key == pygame.K_RETURN:
                    menu_running = False
                    break

    return selected_ships

def all_ships_sunk(ship_list):
    """Check if all ships in the list are sunk."""
    return all(len(ship['hits']) == len(ship['coordinates']) for ship in ship_list)

def display_winner(winner):
    """Display the winner and wait for user input to close the game."""
    win.fill(BLACK)
    draw_text(f"Player {winner} Wins!", WIDTH // 2 , HEIGHT // 2 - 50)
    draw_text("Press ENTER to exit", WIDTH // 2 , HEIGHT // 2 + 50)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    quit()

def display_turn_screen(player_number):
    """Display a screen that informs the player that it is the other player's turn."""
    win.fill(BLACK)
    draw_text(f"Player {player_number}'s Turn", WIDTH // 2 , HEIGHT // 2 - 50)
    draw_text("Please wait for the other player to finish their turn.", WIDTH // 2 , HEIGHT // 2 + 10)
    draw_text("Press any key to continue...", WIDTH // 2 , HEIGHT // 2 + 70)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                break
def draw_text(text, x, y):
    """Utility function to draw text on the screen."""
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    win.blit(text_surface, text_rect)

def all_ships_sunk(ship_list):
    """Check if all ships in the list are sunk."""
    return all(len(ship['hits']) == len(ship['coordinates']) for ship in ship_list)

def display_winner(winner):
    """Display the winner and wait for user input to close the game."""
    win.fill(BLACK)
    win_sound.play()
    draw_text(f"Player {winner} Wins!", WIDTH // 2 , HEIGHT // 2 - 50)
    draw_text("Press ENTER to exit", WIDTH // 2 , HEIGHT // 2 + 50)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    quit()
def instructions_page():
    """Display the game instructions to the player."""
    instructions_running = True
    while instructions_running:
        win.fill(BLACK)

        # Display the instructions
        win.blit(battleship_image, (0, 0)) 

        draw_text("Instructions", WIDTH // 1.5 +70, 50)
        draw_text("1. Place your ships on the grid.", WIDTH // 1.5 +70 , 150)
        draw_text("2. On your turn, try to hit the enemy's ships by ", WIDTH // 1.5 +70 , 200)
        draw_text(" clicking on the missile board.", WIDTH // 1.5 +70 , 250)
        draw_text("3. Colors:", WIDTH // 1.5 +70 , 350)
        draw_text("- Purple: Your ship", WIDTH // 1.5 +70, 400)
        draw_text("- Grey: Missed shot", WIDTH // 1.5 +70, 450)
        draw_text("- Red: Hit", WIDTH // 1.5 +70, 500)
        draw_text("- Green: Sunk enemy ship", WIDTH // 1.5 +70, 550)
        draw_text("- Blue: Sunk friendly ship", WIDTH // 1.5 +70, 600)


        draw_text("Press ENTER to continue...", WIDTH // 1.5 +70, HEIGHT - 100)

        pygame.display.flip()

        # Wait for the player to press a key to proceed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    instructions_running = False  # Exit the instruction page
                    break

def game_loop():
    """Main game loop where players place ships and play the game."""
    # Main menu to select the number of ships
    instructions_page()
    num_ships = main_menu()

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
            draw_text("Your Ships", MARGIN + 200, MARGIN - 20)  # Above Player 1's ship grid
            draw_text("Missile Board", WIDTH // 2 + MARGIN + 200, MARGIN - 20)  # Above Player 1's missile board
            draw_text("Player 1's Turn", WIDTH // 2 - 65, 50)
            draw_grid(missile_board1, WIDTH // 2 + MARGIN, MARGIN, player_grid=False)
            # Display Player 1's own ship grid with hits and sunk ships
            draw_grid(grid1, MARGIN, MARGIN, player_grid=True)
        else:
            # Display Player 2's missile board (targeting Player 1's ships)
            draw_text("Your Ships", MARGIN + 200, MARGIN - 20)  # Above Player 1's ship grid
            draw_text("Missile Board", WIDTH // 2 + MARGIN + 200, MARGIN - 20)  # Above Player 1's missile board
            draw_text("Player 2's Turn", WIDTH // 2 -65, 50)
            draw_grid(missile_board2, WIDTH // 2 + MARGIN, MARGIN, player_grid=False)
            # Display Player 2's own ship grid with hits and sunk ships
            draw_grid(grid2, MARGIN, MARGIN, player_grid=True)
 
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if turn == 1:
                    # Check if Player 1 clicks on the missile board area
                    if (WIDTH // 2 + MARGIN < mouse_x < WIDTH // 2 + MARGIN + GRID_SIZE * CELL_SIZE and 
                        MARGIN < mouse_y < MARGIN + GRID_SIZE * CELL_SIZE):
                        row = (mouse_y - MARGIN) // CELL_SIZE
                        col = (mouse_x - (WIDTH // 2 + MARGIN)) // CELL_SIZE
                        shot.play()
                        if check_hit(grid2, missile_board1, row, col, player2_ships):
                            # Check if Player 1 has won
                            if all_ships_sunk(player2_ships):
                                display_winner(1)  # Player 1 wins
                                running = False
                            else:
                                # Show screen to switch turns and switch to Player 2
                                display_turn_screen(2)
                                turn = 2  # Switch to Player 2
                elif turn == 2:
                    # Check if Player 2 clicks on the missile board area
                    if (WIDTH // 2 + MARGIN < mouse_x < WIDTH // 2 + MARGIN + GRID_SIZE * CELL_SIZE and 
                        MARGIN < mouse_y < MARGIN + GRID_SIZE * CELL_SIZE):
                        row = (mouse_y - MARGIN) // CELL_SIZE
                        col = (mouse_x - (WIDTH // 2 + MARGIN)) // CELL_SIZE
                        shot.play()
                        if check_hit(grid1, missile_board2, row, col, player1_ships):
                            # Check if Player 2 has won
                            if all_ships_sunk(player1_ships):
                                display_winner(2)  # Player 2 wins
                                running = False
                            else:
                                # Show screen to switch turns and switch to Player 1
                                display_turn_screen(1)
                                turn = 1  # Switch to Player 1

    pygame.quit()

if __name__ == "__main__":
    game_loop()
