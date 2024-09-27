class Scoreboard:
    def __init__(self):
        self.player1Hits = 0
        self.player2Hits = 0
        self.display = True

    def update(self, player, hit):
        if player == 1:
            self.player1Hits += 1
        else:
            self.player2Hits += 1

    def display_scoreboard(self):
        # Clear the screen if necessary
        win.fill(BLACK)

        # Draw the scoreboard elements with centered text
        draw_text("Player 1 Hits: " + str(self.player1Hits), WIDTH // 2 - 150, HEIGHT // 2 - 50, align="center")
        draw_text("Player 2 Hits: " + str(self.player2Hits), WIDTH // 2 - 150, HEIGHT // 2, align="center")

        # Display a message to instruct the player to click to continue
        draw_text("Press any key to continue...", WIDTH // 2 - 150, HEIGHT // 2 + 100, align="center")

        pygame.display.flip()

        # Wait for a key press to continue
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   

                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def toggle_display(self):
        self.display = not self.display

# Usage:
scoreboard = Scoreboard()
# Update the scoreboard as needed:
scoreboard.update(1, True)  # Player 1 hit
scoreboard.update(2, False)  # Player 2 miss

# Display the scoreboard:
if scoreboard.display:
    scoreboard.display_scoreboard()
