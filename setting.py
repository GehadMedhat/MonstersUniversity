import pygame
import sys

class GameControls:
    def __init__(self):
        self.exit_button = pygame.image.load('exit.jpg')
        self.replay_button = pygame.image.load('replay.jpg')
        self.stop_button = pygame.image.load('stop.jpg')
        self.pause_button = pygame.image.load('pause.jpg')

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def replay_game(self):
        # Add your replay logic here
        pass

    def stop_music(self):
        # Add your stop music logic here
        pass

    def pause_game(self):
        # Add your pause game logic here
        pass

    def run_settings():
      # Your settings logic goes here
      print("Opening settings...")
      # Add your settings functionality

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.exit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.exit_button.get_rect(topleft=(0, 0)).collidepoint(pygame.mouse.get_pos()):
                self.exit_game()
            elif self.replay_button.get_rect(topleft=(100, 0)).collidepoint(pygame.mouse.get_pos()):
                self.replay_game()
            elif self.stop_button.get_rect(topleft=(200, 0)).collidepoint(pygame.mouse.get_pos()):
                self.stop_music()
            elif self.pause_button.get_rect(topleft=(300, 0)).collidepoint(pygame.mouse.get_pos()):
                self.pause_game()

# Example usage:
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
controls = GameControls()

# Load background image
background = pygame.image.load('background.jpg')  # Replace 'background.jpg' with your image file

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            controls.exit_game()
        else:
            controls.handle_event(event)

    # Render the background
    screen.blit(background, (0, 0))

    # Render the buttons
    screen.blit(controls.exit_button, (0, 0))
    screen.blit(controls.replay_button, (100, 0))
    screen.blit(controls.stop_button, (200, 0))
    screen.blit(controls.pause_button, (300, 0))

    pygame.display.flip()
    clock.tick(60)
