import pygame

class MainMenu:
    """
    Class representing the main menu for Six Men's Morris.
    """

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)  # Font for menu text
        self.selected = 0  # Index of the currently selected menu option

        # Menu options
        self.options = ["Player vs. Player", "Player vs. AI"]

    def draw(self):
        """
        Draws the main menu on the screen.
        """

        # Background color
        self.screen.fill((255, 255, 255))  # Adjust if needed

        # Text rendering and positioning
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (0, 0, 0) if i == self.selected else (100, 100, 100))  # Text color based on selection
            text_rect = text.get_rect(center=self.screen.get_rect().center)
            text_rect.y += i * 100  # Vertical spacing between options
            self.screen.blit(text, text_rect)

    def handle_events(self, event):
        """
        Handles user input events for navigating the main menu.
        """

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)  # Handle wrapping for up key
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)  # Handle wrapping for down key
            elif event.key == pygame.K_RETURN:
                return self.selected  # Return the selected option index on Enter press

        return None  # Return None if no selection made

# Example usage (assuming you have a screen object)
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Adjust screen size
    clock = pygame.time.Clock()

    menu = MainMenu(screen)

    running = True
    selected_option = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            selected_option = menu.handle_events(event)

        menu.draw()
        pygame.display.flip()
        clock.tick(60)  # Limit framerate

    if selected_option is not None:
        # Start the game based on the selected option (0: Player vs. Player, 1: Player vs. AI)
        # ... your game logic here ...
        pass

    pygame.quit()

if __name__ == "__main__":
    main()
