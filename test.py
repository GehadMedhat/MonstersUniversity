import pygame
import sys

pygame.init()

# Set up the display
screen = pygame.display.set_mode((1400, 788))

# Caption and Icon
pygame.display.set_caption("Monsters University: Mike's Journey")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Load frames
frames = [
    pygame.image.load("frame1.jpg"),
    pygame.image.load("frame2.jpg"),
    pygame.image.load("frame3.jpg"),
    pygame.image.load("frame4.jpg"),
    pygame.image.load("frame5.jpg"),
    pygame.image.load("frame6.jpg"),
    pygame.image.load("frame7.jpg"),
    pygame.image.load("frame8.jpg"),
    pygame.image.load("frame9.jpg"),
]

# Load additional image for frame 9
yes_image = pygame.image.load("yes.png")
yes_image = pygame.transform.scale(yes_image, (240, 120))

# Load welcome frame
welcome_frame = pygame.image.load("WelcomeFrame.jpg")

# Load buttons and resize them
story_button = pygame.image.load("StoryModeButton.png")
start_button = pygame.image.load("StartGameButton.png")
skip_button = pygame.image.load("SkipButton.png")

# Resize the buttons
button_width, button_height = 240, 120  # Adjust the width and height as needed
story_button = pygame.transform.scale(story_button, (button_width, button_height))
start_button = pygame.transform.scale(start_button, (button_width, button_height))
skip_button = pygame.transform.scale(skip_button, (100, 100))  # Keep the skip button size

# Set button positions
story_button_rect = story_button.get_rect(topright=(850, 450))
start_button_rect = start_button.get_rect(topleft=(610, 340))
skip_button_rect = skip_button.get_rect(topleft=(1250, 660))  # Adjusted the y-coordinate

current_frame_index = 0

clock = pygame.time.Clock()

show_welcome_frame = True
show_frames_flag = False

while show_welcome_frame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if story_button_rect.collidepoint(event.pos):
                show_frames_flag = True
                show_welcome_frame = False
            elif start_button_rect.collidepoint(event.pos):
                # Add logic to start the game
                print("Start Game button clicked")
                # You can add your game starting logic here

    screen.fill((255, 255, 255))  # Fill the screen with a white background

    # Display the welcome frame
    screen.blit(welcome_frame, (0, 0))

    # Draw buttons on the welcome frame
    screen.blit(story_button, story_button_rect)
    screen.blit(start_button, start_button_rect)

    pygame.display.flip()

    clock.tick(30)  # Adjust the frame rate as needed

# Now, the loop to show frames when Story Mode is clicked
while show_frames_flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_frame_index = (current_frame_index + 1) % len(frames)
            elif event.key == pygame.K_LEFT:
                current_frame_index = (current_frame_index - 1) % len(frames)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if skip_button_rect.collidepoint(event.pos):
                # Clicking the skip button exits the loop and displays a black frame
                show_frames_flag = False

    screen.fill((255, 255, 255))  # Fill the screen with a white background

    if current_frame_index == 8:
        # Display the yes.png image on top of frame 9
        screen.blit(frames[current_frame_index], (0, 0))
        screen.blit(yes_image, (800, 400))
    elif current_frame_index < len(frames):
        # Display the current frame
        screen.blit(frames[current_frame_index], (0, 0))
    else:
        # Display a blank black frame.
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 1400, 788))

    # Draw the smaller skip button on frames
    screen.blit(skip_button, skip_button_rect)

    pygame.display.flip()

    clock.tick(30)  # Adjust the frame rate as neededzzz