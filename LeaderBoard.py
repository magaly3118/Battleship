import json

def add_score_to_leaderboard(player_score):
    player_name = ""  # To store the player's name input
    name_entered = False
    input_active = True

    while input_active:
        win.fill(BLACK)

        # Display instructions and current input
        draw_text("Enter your name: " + player_name, WIDTH // 2 - 150, HEIGHT // 2 - 50)
        draw_text("Press ENTER to submit", WIDTH // 2 - 150, HEIGHT // 2 + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key   
 == pygame.K_RETURN:
                    name_entered = True  # Finish name input
                    input_active = False

                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character from the name
                    player_name = player_name[:-1]
                else:
                    # Add the pressed key to the player_name string
                    player_name += event.unicode

    # Once name is entered, proceed to save the score
    if name_entered:
        # Assuming leaderboard is stored as a list of dictionaries in a file or a global list
        leaderboard = []  # Load existing leaderboard data from a file or global variable

        try:
            # Open the leaderboard file and load the existing scores (JSON format for simplicity)
            with open("leaderboard.json", "r") as f:
                leaderboard = json.load(f)
        except FileNotFoundError:
            # If no leaderboard exists, start with an empty list
            leaderboard = []

        # Add the new score to the leaderboard
        new_entry = {"name": player_name, "score": player_score}
        leaderboard.append(new_entry)

        # Sort the leaderboard by score in descending order (highest scores first)
        leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

        # Save the updated leaderboard back to the file
        with open("leaderboard.json",   
 "w") as f:
            json.dump(leaderboard, f)

        print(f"Added {player_name}'s score of {player_score} to the leaderboard!")

def display_leaderboard():
    # Display the leaderboard, or show a blank menu if no file exists
    leaderboard = []
    leaderboard_file = "leaderboard.json"

    # Check if the leaderboard file exists
    if os.path.exists(leaderboard_file):
        # Load the leaderboard data from the file
        try:
            with open(leaderboard_file, "r") as f:
                leaderboard = json.load(f)
        except json.JSONDecodeError:
            # If the file exists but is corrupted or empty, set an empty leaderboard
            leaderboard = []
    else:
        # No file exists, so start with an empty leaderboard
        leaderboard = []

    # Display the leaderboard on the screen
    win.fill(BLACK)

    if leaderboard:
        # Sort the leaderboard in descending order by score
        leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

        draw_text("Leaderboard", WIDTH // 2 - 100, HEIGHT // 2 - 150)

        # Display the top 5 players (or fewer if there aren't that many)
        for index, entry in enumerate(leaderboard[:5]):
            name = entry["name"]
            score = entry["score"]
            draw_text(f"{index + 1}. {name}: {score}", WIDTH // 2 - 100, HEIGHT // 2 - 50 + index * 30)

    else:
        # If no leaderboard data exists, display a blank message
        draw_text("Leaderboard is empty", WIDTH // 2 - 100, HEIGHT // 2)

    draw_text("Press ENTER to return to the main menu", WIDTH // 2 - 100, HEIGHT // 2 + 150)
    pygame.display.flip()

    # Wait for the user to press ENTER to go back to the menu
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:   

                if event.key == pygame.K_RETURN:   
  # Return to main menu on ENTER
                    waiting_for_input = False