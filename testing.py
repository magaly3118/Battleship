"""
Testing

Date Created: 09/13/24
Date Last Modified: 09/13/34

Description: Testing the ship placement, ship length, hits, misses, and if all ships have sunk.
"""

# Define constants for grid size and ship lengths
GRID_SIZE = 10
default_ships = [1, 2, 3, 4, 5]

# Create ship and missile grids for Player 1
grid1 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
missile_board1 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Create ship and missile grids for Player 2
grid2 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
missile_board2 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Use the place_ship function from main for testing
def place_ship(grid, start_row, start_col, ship_len, orientation, ship_list):
    ship_coordinates = []
    if orientation == "H":
        if start_col + ship_len <= GRID_SIZE:
            if all(grid[start_row][start_col + i] == 0 for i in range(ship_len)):
                for i in range(ship_len):
                    grid[start_row][start_col + i] = 1
                    ship_coordinates.append((start_row, start_col + i))
                ship_list.append({'coordinates': ship_coordinates, 'hits': []})
                # Show where the ship's coordinates
                print(f"Ship is placed at {ship_coordinates}")
                return ship_coordinates
            # Let user know ship is overlapping another ship
            else:
                print("Ship is overlapping another ship")
                return None
        # Let user know ship is outside the grid
        else:
            print("Ship is outside the grid")
            return None
    elif orientation == "V":
        if start_row + ship_len <= GRID_SIZE:
            if all(grid[start_row + i][start_col] == 0 for i in range(ship_len)):
                for i in range(ship_len):
                    grid[start_row + i][start_col] = 1
                    ship_coordinates.append((start_row + i, start_col))
                ship_list.append({'coordinates': ship_coordinates, 'hits': []})
                # Show where the ship's coordinates
                print(f"Ship is placed at {ship_coordinates}")
                return ship_coordinates
            # Let user know ship is overlapping another ship
            else:
                print("Ship is overlapping another ship")
                return None
        # Let user know ship is outside the grid
        else:
            print("Ship is outside the grid")
            return None
    else:
        return None

# Check if ship length
def ship_length(ship_coordinates, expected_len):
    if len(ship_coordinates) == expected_len:
        print(f"Ship length passed. Expected: {expected_len}")
    else:
        print(f"Ship length failed. Expected: {expected_len}, got {len(ship_coordinates)}")

# Check if a ship is hit or not
def check_hit(ship_grid, missile_board, row, col,ship_list):
    # Hitting the same spot
    if missile_board[row][col] != 0:
        print(f"({row}, {col}) has already been targeted")
        return False
    
    # A ship got hit
    if ship_grid[row][col] == 1:
        # Mark hit on missile board
        missile_board[row][col] = 2
        # Mark hit on ship grid
        ship_grid[row][col] = 2
        print(f"Hit at ({row}, {col})")

        for ship in ship_list:
            if (row, col) in ship['coordinates']:
                # Mark down hit
                ship['hits'].append((row, col))
                print(f"Ship hit at ({row}, {col}), Total hits on this ship: {len(ship['hits'])}")

                # Check if ship sunk
                if len(ship['hits']) == len(ship['coordinates']):
                    print(f"Ship at {ship['coordinates']} sunk")
                    for (r, c) in ship['coordinates']:
                        # Mark sunk on missile board
                        missile_board[r][c] = 3
                        # Mark sunk on ship grid
                        ship_grid[r][c] = 3
        return True
    # Ship did not get hit
    else:
        # Mark miss on missile board
        missile_board[row][col] = 1
        print(f"Miss at ({row}, {col})")
        return False

# Check if all ships sunk
def all_ships_sunk(grid):
    for row in grid:
        # Ship hasn't sunk yet, but has been hit
        if 1 in row:
            return False
    return True

# Test if all player's ships sunk, if expected is 'False' it means that not all the player's ships sunk
def test_all_ships_sunk(grid, expected):
    result = all_ships_sunk(grid)
    if result == expected:
        print(f"All ships sunk test passed, result: {expected}")
    else:
        print(f"All ships sunk test failed, result: {expected}")


# Testing ships overlapping
def test1():
    print("\nShips Overlapping Test:")
    p1_ships=[]

    # Place first ship
    place_ship(grid1, 0, 0, 3, "H", p1_ships)
    # Place second ship, let user know there's overlapping
    place_ship(grid1, 0, 1, 3, "H", p1_ships)

# Testing ships outside grid
def test2():
    print("\nShips Outside Grid Test:")
    p1_ships=[]

    # Place ship outside grid
    place_ship(grid1, 10, 10, 3, "H", p1_ships)

# Testing repeated hit attempt
def test3():
    print("\nRepeated Hit Test:")
    p1_ships=[]

    # Place ship
    place_ship(grid1, 0, 0, 3, "H", p1_ships)

    # Hit ship once
    check_hit(grid1, missile_board1, 0, 0, p1_ships)
    # Hit ship at the same spot
    check_hit(grid1, missile_board1, 0, 0, p1_ships)

# Testing a game, 2 players, 1 ship each
def test4():
    print("\nGame Test:")
    # Ship lists for both players
    p1_ships = []
    p2_ships = []

    # Place a ship for both players
    p1_ship = place_ship(grid1,0, 0, 2, "H", p1_ships)
    p2_ship = place_ship(grid2, 5, 5, 3, "V", p2_ships)

    # Test if ship length matches expected
    ship_length(p1_ship, 2)
    ship_length(p2_ship, 3)

    # Player 1's turn
    print("\nPlayer 1's turn")
    # Player 1 hits Player 2's ship
    check_hit(grid2, missile_board1, 5, 5, p2_ships)

    # Check if both players' ships sunk
    print("\nShip Status")
    # Player 1's ships should not be sunk yet
    test_all_ships_sunk(grid1, False)
    # Player 2's ships should not be sunk yet
    test_all_ships_sunk(grid2, False)

    # Player 2's turn
    print("\nPlayer 2's turn")
    # Player 2 misses Player 1's ship
    check_hit(grid1, missile_board2, 1, 1, p1_ships)

    # Check if both players' ships sunk
    print("\nShip Status")
    # Player 1's ships should not be sunk yet
    test_all_ships_sunk(grid1, False)
    # Player 2's ships should not be sunk yet
    test_all_ships_sunk(grid2, False)

    # Player 1's turn
    print("\nPlayer 1's turn")
    # Player 1 hits Player 2's ship
    check_hit(grid2, missile_board1, 6, 5, p2_ships)

    # Check if both players' ships sunk
    print("\nShip Status")
    # Player 1's ships should not be sunk yet
    test_all_ships_sunk(grid1, False)
    # Player 2's ships should not be sunk yet
    test_all_ships_sunk(grid2, False)

    # Player 2's turn
    print("\nPlayer 2's turn")
    # Player 2 hits Player 1's ship
    check_hit(grid1, missile_board2, 0, 0, p1_ships)

    # Check if both players' ships sunk
    print("\nShip Status")
    # Player 1's ships should not be sunk yet
    test_all_ships_sunk(grid1, False)
    # Player 2's ships should not be sunk yet
    test_all_ships_sunk(grid2, False)

    # Player 1's turn
    print("\nPlayer 1's turn")
    # Player 1 hits Player 2's ship
    check_hit(grid2, missile_board1, 7, 5, p2_ships)

    # Check if both players' ships sunk
    print("\nShip Status")
    # Player 1's ships should not be sunk yet
    test_all_ships_sunk(grid1, False)
    # Player 2's ships should be sunk 
    test_all_ships_sunk(grid2, True)

# Test game logic and scenarios
def test():
    # test functions individually
    # test1() 
    # test2()
    # test3()  
    test4()
    

if __name__ == "__main__":
    test()



