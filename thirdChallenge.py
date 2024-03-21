import pygame
import sys
import time
from theEnd import TheEnd
import tkinter as tk
from tkinter import messagebox

def reset_game():
    global showing_first_frame, all_images_clicked, clicked_images, last_click_time, start_time, game_lost
    showing_first_frame = True
    all_images_clicked = False
    clicked_images = []
    last_click_time = None
    start_time = time.time()
    game_lost = False


def initialize_game():
    # Initialize Pygame
    pygame.init()

# Set up display
width, height = 1400, 788
initialize_game()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame with Images")

# Load background image for the first frame
first_frame_image = pygame.image.load("first.png")
first_frame_rect = first_frame_image.get_rect(center=(width // 2, height // 2))

# Load start button image
button_image = pygame.image.load("button.png")
button_rect = button_image.get_rect(center=(width // 2, height - 240))

# Load background image for the game
background_image = pygame.image.load("room.jpg")
background_rect = background_image.get_rect()

# Load RedCircle image with a larger size
red_circle_size = (200, 200)  # Adjust the size as needed
red_circle = pygame.transform.scale(pygame.image.load("RedCircle.png"), red_circle_size)

# Load indicator image
indicator_size = (150, 300)  # Adjust the size as needed
indicator = pygame.transform.scale(pygame.image.load("indicator.png"), indicator_size)

# Load six images and scale them
image1 = pygame.transform.scale(pygame.image.load("door.jpg"), (250, 500))
image2 = pygame.transform.scale(pygame.image.load("toys.jpg"), (205, 100))
image3 = pygame.transform.scale(pygame.image.load("bed.jpg"), (300, 200))
image4 = pygame.transform.scale(pygame.image.load("cup.jpg"), (100, 80))
image5 = pygame.transform.scale(pygame.image.load("chair.jpg"), (180, 190))
image6 = pygame.transform.scale(pygame.image.load("window.jpg"), (100, 400))

# Set dimensions and positions for the six images
image1_rect = image1.get_rect(topleft=(380, 25))
image2_rect = image2.get_rect(topleft=(410, 536))
image3_rect = image3.get_rect(topright=(width - 440, 450))
image4_rect = image4.get_rect(bottomleft=(218, height - 148))
image5_rect = image5.get_rect(bottomright=(width - 230, height - 203))
image6_rect = image6.get_rect(topleft=(120, 110))

# Load MP3 sounds and set volume for each
sound1 = pygame.mixer.Sound("squeaky door open.mp3")
sound1.set_volume(0.5)

sound2 = pygame.mixer.Sound("dog toy.mp3")
sound2.set_volume(0.5)

sound3 = pygame.mixer.Sound("Nails Scratching Wall.mp3")
sound3.set_volume(0.5)

sound4 = pygame.mixer.Sound("glass smash.mp3")
sound4.set_volume(0.5)

sound5 = pygame.mixer.Sound("chair squeaking.mp3")
sound5.set_volume(0.5)

sound6 = pygame.mixer.Sound("rain on window.mp3")
sound6.set_volume(0.5)

# List to store image and sound pairs
image_sound_mapping = [
    (image1_rect, sound1),
    (image2_rect, sound2),
    (image3_rect, sound3),
    (image4_rect, sound4),
    (image5_rect, sound5),
    (image6_rect, sound6),
]

# List to store clicked images
clicked_images = []

# Define properties for the indicator
indicator_margin = 20
indicator_spacing = 10
indicator_width = 20
indicator_height = height - 2 * indicator_margin - 620

# Initialize the green indicator position
green_indicator_x = width - indicator_margin - indicator_width - 50
green_indicator_y = indicator_margin + 180

# Flag to indicate if the first frame is being shown
showing_first_frame = True

# Flag to indicate if all images have been clicked
all_images_clicked = False

# Time when the last image is clicked
last_click_time = None

# Load replay and exit buttons
replay_button = pygame.image.load("replay.png")
exit_button = pygame.image.load("exit.png")

# Time variables
total_time = 120 # 1 minute
start_time = time.time()

# Load the "Lost" image
lost_image = pygame.image.load("lost.jpg")

# Load question mark, exit, and replay images
question_mark_image = pygame.image.load("questionMark.png")
replay_button = pygame.image.load("replay.png")
exit_button = pygame.image.load("exit.png")

# Resize the buttons
button_width, button_height = 200, 100  # Adjust the width and height as needed
replay_button = pygame.transform.scale(replay_button, (button_width, button_height))
exit_button = pygame.transform.scale(exit_button, (button_width, button_height))

# Set button positions
replay_button_rect = replay_button.get_rect(center=(width // 4, height - 200))
exit_button_rect = exit_button.get_rect(center=(3 * width // 4, height - 200))

# Resize the question mark icon
question_mark_size = (50, 50)  # Adjust the size as needed
question_mark_image = pygame.transform.scale(question_mark_image, question_mark_size)

# Set the position of the question mark icon
question_mark_rect = question_mark_image.get_rect(topright=(width - 20, 20))

# Flag to indicate if the small frame is being shown
show_small_frame = False
small_frame_timer = 0

# Load replay and exit buttons for the small frame
small_frame_replay_button = pygame.image.load("replay.png")
small_frame_exit_button = pygame.image.load("exit.png")

# Resize the buttons for the small frame
small_frame_button_width, small_frame_button_height = 100, 50  # Adjust the width and height as needed
small_frame_replay_button = pygame.transform.scale(small_frame_replay_button, (small_frame_button_width, small_frame_button_height))
small_frame_exit_button = pygame.transform.scale(small_frame_exit_button, (small_frame_button_width, small_frame_button_height))

# Set positions for the buttons in the small frame
small_frame_replay_button_rect = small_frame_replay_button.get_rect(center=(width // 2 - 50, height // 2 + 50))
small_frame_exit_button_rect = small_frame_exit_button.get_rect(center=(width // 2 + 50, height // 2 + 50))

# Game state variables
game_lost = False
show_exit_replay_buttons = False 

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if question_mark_rect.collidepoint(event.pos):
                # Show exit and replay buttons
                show_exit_replay_buttons = True
                small_frame_timer = pygame.time.get_ticks()
            elif showing_first_frame and button_rect.collidepoint(event.pos):
                showing_first_frame = False
            else:
                for rect, sound in image_sound_mapping:
                    if rect.collidepoint(event.pos):
                        sound.play()
                        clicked_images.append(rect)
                        last_click_time = time.time()
     # Inside the main game loop, handle the event when the question mark is clicked
        elif showing_first_frame and question_mark_rect.collidepoint(pygame.mouse.get_pos()):
          # Show a pop-up window with exit and replay buttons
         root = tk.Tk()
         root.title("Options")

         def replay_game():
          # Close the pop-up window
          root.destroy()

          # Restart the game by resetting game state and initializing a new game window
          reset_game()
          showing_first_frame = True

         def exit_game():
          # Display a confirmation dialog before exiting
          result = messagebox.askyesno("Exit Game", "Are you sure you want to exit?")
          if result:
             pygame.quit()
             sys.exit()

         replay_button = tk.Button(root, text="Replay", command=replay_game)
         replay_button.pack()

         exit_button = tk.Button(root, text="Exit", command=exit_game)
         exit_button.pack()

         root.mainloop()

    # Draw to the screen
    if showing_first_frame:
        screen.blit(background_image, background_rect)  # Draw the background
        screen.blit(first_frame_image, first_frame_rect)
        screen.blit(button_image, button_rect)
        screen.blit(question_mark_image, question_mark_rect)
    else:
        screen.blit(background_image, background_rect)  # Draw the background
        # Draw the six images on top of the background
        screen.blit(image1, image1_rect)
        screen.blit(image2, image2_rect)
        screen.blit(image3, image3_rect)
        screen.blit(image4, image4_rect)
        screen.blit(image5, image5_rect)
        screen.blit(image6, image6_rect)
        screen.blit(question_mark_image, question_mark_rect)

        # Draw exit and replay buttons when needed
        if show_exit_replay_buttons:
            screen.blit(exit_button, exit_button_rect)
            screen.blit(replay_button, replay_button_rect)

        # Draw RedCircle on top of clicked images
        for rect in clicked_images:
            center_x = rect.x + rect.width // 2
            center_y = rect.y + rect.height // 2
            red_circle_rect = red_circle.get_rect(center=(center_x, center_y))
            screen.blit(red_circle, red_circle_rect)

        # Draw the indicator image
        indicator_x = green_indicator_x - 80
        indicator_y = green_indicator_y - 90
        screen.blit(indicator, (indicator_x, indicator_y))

        # Draw rectangles inside the indicator based on the number of clicked images
        for i in range(min(len(clicked_images), 6)):
            rect_height = indicator_height / 6
            rect_y = green_indicator_y + i * rect_height
            pygame.draw.rect(screen, (255, 0, 0), (green_indicator_x, rect_y, indicator_width, rect_height))

        # Check if all images are clicked
        if not all_images_clicked and len(clicked_images) == len(image_sound_mapping):
            if last_click_time is not None and time.time() - last_click_time > 7:
                # Execute theEnd class or any other desired action
               all_images_clicked = True
               print("All images clicked, waiting for 7 seconds. Executing theEnd class...")

               pygame.quit()  # Close the Pygame display

             # Assuming theEnd class has a method is_playing() to check if the video is still playing
               the_end_instance = TheEnd()  # Use the correct case for the class name
               the_end_instance.play_video()

# Handle Pygame events until the video is closed
               while the_end_instance.is_playing():  # Adjust the method based on your video player
                for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    initialize_game()
                    screen = pygame.display.set_mode((width, height))
                    # Reset the game state
                    reset_game()

        # Timer logic
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(total_time - elapsed_time, 0)

        # Display the timer at the top left
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {remaining_time} seconds", True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))

        # Check if time is up
        if remaining_time == 0 and not all_images_clicked:
            game_lost = True

         # Draw small frame when needed
        if show_small_frame:
            current_time = pygame.time.get_ticks()
            if current_time - small_frame_timer < 2000:  # Display the small frame for 2 seconds
                # Create a small frame with the question mark and buttons
                small_frame_width, small_frame_height = 200, 150
                small_frame_surface = pygame.Surface((small_frame_width, small_frame_height))
                small_frame_rect = small_frame_surface.get_rect(center=(width // 2, height // 2))
                small_frame_surface.blit(question_mark_image, (50, 20))  # Draw the question mark

                # Draw exit and replay buttons
                small_frame_surface.blit(small_frame_replay_button, small_frame_replay_button_rect)
                small_frame_surface.blit(small_frame_exit_button, small_frame_exit_button_rect)

                # Draw the small frame on the main screen
                screen.blit(small_frame_surface, small_frame_rect)

            else:
                show_small_frame = False    

    pygame.display.flip()  # Update the display

    # Cap the frame rate
    pygame.time.Clock().tick(60)
    # Game over logic
    if game_lost:
      screen.blit(lost_image, (0, 0))

    # Load replay and exit buttons
      replay_button = pygame.image.load("replay.png")
      exit_button = pygame.image.load("exit.png")

    # Resize the buttons
      button_width, button_height = 200, 100  # Adjust the width and height as needed
      replay_button = pygame.transform.scale(replay_button, (button_width, button_height))
      exit_button = pygame.transform.scale(exit_button, (button_width, button_height))

    # Set button positions
      replay_button_rect = replay_button.get_rect(center=(width // 4, height - 200))
      exit_button_rect = exit_button.get_rect(center=(3 * width // 4, height - 200))

    # Draw buttons on the game over screen
      screen.blit(replay_button, replay_button_rect)
      screen.blit(exit_button, exit_button_rect)

      pygame.display.flip()

    # Wait for user input on the game over screen
      game_over = True
      while game_over:
        for event in pygame.event.get():
         if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
         elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
          if question_mark_rect.collidepoint(event.pos):
             # Show exit and replay buttons
            show_exit_replay_buttons = True
            small_frame_timer = pygame.time.get_ticks()
            


        pygame.time.Clock().tick(60)