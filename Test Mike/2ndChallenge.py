import pygame
import sys
import os
import time
import pygame.mixer


def reset_game():
    global showing_first_frame, all_images_clicked, clicked_images, last_click_time, start_time, game_lost
    showing_first_frame = True
    all_images_clicked = False
    clicked_images = []
    last_click_time = None
    start_time = time.time()
    game_lost = False

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1400, 788
FPS = 60
GRAVITY = 1
PLAYER_SPEED = 5
JUMP_HEIGHT = -22
NUM_HEARTS = 5
NUM_FLAGS = 3
GAME_TIME = 30

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

# Load background music and sounds
pygame.mixer.music.load("background.mp3")
background_sound = pygame.mixer.Sound("background.mp3")
catch_flag_sound = pygame.mixer.Sound("flag.mp3")
lose_heart_sound = pygame.mixer.Sound("heart.mp3")

# Play the background music continuously
pygame.mixer.music.play(loops=-1)


# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

# Load images
current_dir = os.path.dirname(os.path.abspath(__file__))
background_image = pygame.image.load(os.path.join(current_dir, 'background.jpg')).convert()
player_right_image = pygame.image.load(os.path.join(current_dir, 'mikeRight.png')).convert_alpha()
player_left_image = pygame.image.load(os.path.join(current_dir, 'mikeLeft.png')).convert_alpha()
flag_image = pygame.image.load(os.path.join(current_dir, 'flag.png')).convert_alpha()
chair_image = pygame.image.load(os.path.join(current_dir, 'chair.png')).convert_alpha()
plant_image = pygame.image.load(os.path.join(current_dir, 'plant.png')).convert_alpha()
library_image = pygame.image.load(os.path.join(current_dir, 'library.png')).convert_alpha()
heart_image = pygame.image.load(os.path.join(current_dir, 'heart.png')).convert_alpha()
timer_font = pygame.font.Font(None, 36)
info_font = pygame.font.Font(None, 24)

# Resize images
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
player_right_image = pygame.transform.scale(player_right_image, (100,100))
player_left_image = pygame.transform.scale(player_left_image, (100,100))
flag_image = pygame.transform.scale(flag_image, (100,100))
chair_image = pygame.transform.scale(chair_image, (100,100))
plant_image = pygame.transform.scale(plant_image, (100,100))
library_image = pygame.transform.scale(library_image, (120,120))
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Load additional images
start_image = pygame.image.load(os.path.join(current_dir, 'start.png')).convert_alpha()
button_image = pygame.image.load(os.path.join(current_dir, 'button.png')).convert_alpha()
lost_image = pygame.image.load(os.path.join(current_dir, 'lost.jpg')).convert_alpha()
win_image = pygame.image.load(os.path.join(current_dir, 'level3Win.png')).convert_alpha()

# Resize images
start_image = pygame.transform.scale(start_image, (WIDTH, HEIGHT))
button_image = pygame.transform.scale(button_image, (270, 80))
lost_image = pygame.transform.scale(lost_image, (WIDTH, HEIGHT))
win_image = pygame.transform.scale(win_image, (WIDTH, HEIGHT))

# Load additional images
level3_image = pygame.image.load(os.path.join(current_dir, 'level3.png')).convert_alpha()

# Resize images
level3_image = pygame.transform.scale(level3_image, (460, 200))
# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((197, 135, 74))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, *args):
        pass  # Do nothing, keeping the platform fixed

# Heart class
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = heart_image
        self.rect = self.image.get_rect()

# Flag class
class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = flag_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Timer class
class Timer:
    def __init__(self, total_time):
        self.total_time = total_time
        self.remaining_time = total_time
        self.start_time = pygame.time.get_ticks()

    def get_elapsed_time(self):
        return (pygame.time.get_ticks() - self.start_time) // 1000

    def get_remaining_time(self):
        return max(0, self.total_time - self.get_elapsed_time())

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_right_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0

        if keys[pygame.K_LEFT]:
            self.image = player_left_image
            self.velocity.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.image = player_right_image
            self.velocity.x = PLAYER_SPEED

        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.y = JUMP_HEIGHT
            self.on_ground = False

        self.velocity.y += GRAVITY
        self.rect.x += self.velocity.x
        self.check_collision_x()

        self.rect.y += self.velocity.y
        self.on_ground = False
        self.check_collision_y()

    def check_collision_x(self):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.velocity.x > 0:
                self.rect.right = platform.rect.left
            elif self.velocity.x < 0:
                self.rect.left = platform.rect.right

    def check_collision_y(self):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.velocity.y > 0:
                self.rect.bottom = platform.rect.top
                self.on_ground = True
                self.velocity.y = 0
            elif self.velocity.y < 0:
                self.rect.top = platform.rect.bottom
                self.velocity.y = 0

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = chair_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Plant class
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = plant_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Library class
class Library(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = library_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Chair class
class Chair(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = chair_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Initialize flags_collected
flags_collected = 0

# Create sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
flags = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
hearts = pygame.sprite.Group()

# Create instances of Platform, Flag, Obstacle, Plant, Library, and Heart
# Make the platform wider and cover the entire screen
platform = Platform(0, HEIGHT - 80, WIDTH, 80, GREEN)
platforms.add(platform)
all_sprites.add(platform)

flag1 = Flag(1000, HEIGHT - 180)
flags.add(flag1)
all_sprites.add(flag1)

flag2 = Flag(2500, HEIGHT - 180)
flags.add(flag2)
all_sprites.add(flag2)

flag3 = Flag(4000, HEIGHT - 180)
flags.add(flag3)
all_sprites.add(flag3)

# Create instances of Library and Plant and add them to the obstacles group
library = Library(1400, HEIGHT - 195)
obstacles.add(library)
all_sprites.add(library)

library2 = Library(2600, HEIGHT - 195)
obstacles.add(library2)
all_sprites.add(library2)

library3 = Library(4600, HEIGHT - 195)
obstacles.add(library3)
all_sprites.add(library3)

library4 = Library(6600, HEIGHT - 195)
obstacles.add(library4)
all_sprites.add(library4)

library5 = Library(8600, HEIGHT - 195)
obstacles.add(library5)
all_sprites.add(library5)

plant = Plant(800, HEIGHT - 175)
obstacles.add(plant)
all_sprites.add(plant)

plant2 = Plant(3400, HEIGHT - 175)
obstacles.add(plant2)
all_sprites.add(plant2)

plant3 = Plant(5400, HEIGHT - 175)
obstacles.add(plant3)
all_sprites.add(plant3)

plant4 = Plant(7400, HEIGHT - 175)
obstacles.add(plant4)
all_sprites.add(plant4)

plant5 = Plant(9400, HEIGHT - 175)
obstacles.add(plant5)
all_sprites.add(plant5)

chair = Chair(2000, HEIGHT - 175)
obstacles.add(chair)
all_sprites.add(chair)

chair2 = Chair(4000, HEIGHT - 175)
obstacles.add(chair2)
all_sprites.add(chair2)

chair3 = Chair(6000, HEIGHT - 175)
obstacles.add(chair3)
all_sprites.add(chair3)

chair4 = Chair(8000, HEIGHT - 175)
obstacles.add(chair4)
all_sprites.add(chair4) 

chair5 = Chair(10000, HEIGHT - 175)
obstacles.add(chair5)
all_sprites.add(chair5) 

# Add the player sprite
player = Player()
all_sprites.add(player)

# Load replay and exit buttons
replay_button = pygame.image.load("replay.png")
exit_button = pygame.image.load("exit.png")

# Resize the buttons
button_width, button_height = 200, 100  # Adjust the width and height as needed
replay_button = pygame.transform.scale(replay_button, (button_width, button_height))
exit_button = pygame.transform.scale(exit_button, (button_width, button_height))

# Set button positions
replay_button_rect = replay_button.get_rect(center=(WIDTH // 4, HEIGHT - 200))
exit_button_rect = exit_button.get_rect(center=(3 * WIDTH // 4, HEIGHT - 200))

# Add hearts to follow the player
for i in range(NUM_HEARTS):
    heart = Heart(WIDTH // 2 - (NUM_HEARTS * 20) + (i * 40), 20)
    hearts.add(heart)
    all_sprites.add(heart)

# Initialize showing_first_frame
showing_first_frame = True
background_sound_playing = False
# Initialize replay_clicked flag outside the loop
replay_clicked = False

# Function to check if any sound is playing
def is_sound_playing():
    return pygame.mixer.get_busy()

# Game loop
clock = pygame.time.Clock()
background_x = 0
timer = Timer(GAME_TIME)
is_playing = False
is_won = False
is_lost = False
show_lost_screen = False  # Added flag to control lost screen display

# Initialize variables for heart loss sound
heart_loss_sound_playing = False
heart_loss_sound_timer = 0

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
             if replay_button_rect.collidepoint(event.pos):
                print("Replay button clicked")
                is_playing = True  # Start the game
                # Add logic to reset the game state
                print("Resetting the game...")
                reset_game()  # Reset the game state
             elif exit_button_rect.collidepoint(event.pos):
                    print("Exit button clicked")
                    pygame.quit()
                    sys.exit()

    # Check if the player collects flags
    collisions_flags = pygame.sprite.spritecollide(player, flags, True)
    for _ in collisions_flags:
        # If player collects a flag, update the counter
        flags_collected += 1

    # Check if the player collides with obstacles (chair, plant, library)
    collisions_obstacles = pygame.sprite.spritecollide(player, obstacles, True)
    if collisions_obstacles:
        if hearts:
            # If there are hearts left, remove one
            heart = hearts.sprites()[-1]
            hearts.remove(heart)
            all_sprites.remove(heart)
            if not heart_loss_sound_playing:
                lose_heart_sound.play()
                heart_loss_sound_playing = True
                # Set a timer to stop playing the heart loss sound after a short duration
                heart_loss_sound_timer = pygame.time.get_ticks() + 1000  # Adjust the duration as needed
        else:
            # If no hearts left, player loses
            is_lost = True

    all_sprites.update()

    # Camera follows the player
    camera_offset = player.rect.x - WIDTH // 2
    for sprite in all_sprites:
        sprite.rect.x -= camera_offset

    # Duplicate obstacles like the background
    for obstacle in obstacles.sprites():
        obstacle.rect.x -= player.velocity.x

    # Check if the player wins
    if flags_collected >= NUM_FLAGS:
        is_won = True

    if not (is_won or is_lost) and timer.get_remaining_time() <= 0:
        if flags_collected < NUM_FLAGS:
            is_lost = True
    
    if not is_playing:
        # Show the start screen
        screen.blit(start_image, (0, 0))
        screen.blit(button_image, (WIDTH // 2 - 140, HEIGHT // 2 + 100))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()

        if WIDTH // 2 - 140 < mouse_x < WIDTH // 2 + 140 and HEIGHT // 2 + 100 < mouse_y < HEIGHT // 2 + 300:
            if click:
                is_playing = True
                timer.start_time = pygame.time.get_ticks()

        pygame.display.flip()
        clock.tick_busy_loop(FPS)
        continue

    # Check if the player wins or loses
    if not (is_won or is_lost) and timer.get_remaining_time() <= 0:
        if flags_collected >= NUM_FLAGS:
            is_won = True
        else:
            is_lost = True

    if is_won:
        # Show win screen
        screen.blit(win_image, (0, 0))

        # Draw the button on the win screen
        button_rect = level3_image.get_rect(center=(WIDTH // 2 + 35, HEIGHT // 2 + 280))
        screen.blit(level3_image, button_rect)

        # Handle button click on the win screen
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()

        if button_rect.collidepoint(mouse_x, mouse_y):
            if click:
                print("Button on win screen clicked")
                # Add code to handle button click action

        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Reset the replay_clicked flag when the mouse is not over the replay button
    if not replay_button_rect.collidepoint(pygame.mouse.get_pos()):
        replay_clicked = False

    # Check if the player loses
    if is_lost and len(hearts) == 0 and not show_lost_screen:
        show_lost_screen = True   
        
    # Check if the game is lost
    elif is_lost:

        # Show lost screen
        screen.blit(lost_image, (0, 0))

        # Draw buttons on the game over screen
        screen.blit(replay_button, replay_button_rect)
        screen.blit(exit_button, exit_button_rect)

        # Handle button clicks on the game over screen
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()

        if replay_button_rect.collidepoint(mouse_x, mouse_y):
            if click:
                print("Replay button clicked")
                is_lost = False  # Reset the lost state
                reset_game()  # Reset the game state
                show_lost_screen = False
                continue
        elif exit_button_rect.collidepoint(mouse_x, mouse_y):
            if click:
                print("Exit button clicked")
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Play the heart loss sound for a short duration after each heart loss
    if heart_loss_sound_playing and pygame.time.get_ticks() > heart_loss_sound_timer:
        heart_loss_sound_playing = False
        
    # Create new obstacles as needed
    last_obstacle = obstacles.sprites()[-1]
    if last_obstacle.rect.right < WIDTH:
        new_library = Library(last_obstacle.rect.right + 200, HEIGHT - 200)
        obstacles.add(new_library)
        all_sprites.add(new_library)

        new_plant = Plant(last_obstacle.rect.right + 400, HEIGHT - 200)
        obstacles.add(new_plant)
        all_sprites.add(new_plant)

        new_chair = Chair(last_obstacle.rect.right + 600, HEIGHT - 200)
        obstacles.add(new_chair)
        all_sprites.add(new_chair)

    # Check if the first platform is partially out of the screen to the left
    first_platform = platforms.sprites()[0]
    if first_platform.rect.left > 0:
        # Create a new platform to the left of the first platform
        new_platform = Platform(first_platform.rect.left - WIDTH, HEIGHT - 80, WIDTH, 80, GREEN)
        platforms.add(new_platform)
        all_sprites.add(new_platform)

    # Check if the last platform is partially out of the screen to the right
    last_platform = platforms.sprites()[-1]
    if last_platform.rect.right < WIDTH:
        # Create a new platform to the right of the last platform
        new_platform = Platform(last_platform.rect.right, HEIGHT - 80, WIDTH, 80, GREEN)
        platforms.add(new_platform)
        all_sprites.add(new_platform)

    # Draw background
    screen.blit(background_image, (background_x % WIDTH - WIDTH, 0))
    screen.blit(background_image, (background_x % WIDTH, 0))

    # Move background with the player
    background_x -= player.velocity.x

    # Reset background position to create a looping effect
    if background_x >= WIDTH:
        background_x = 0
    elif background_x <= -WIDTH:
        background_x = 0

    # Draw sprites
    all_sprites.draw(screen)

    # Draw timer
    timer_text = timer_font.render(f"Time Left: {timer.get_remaining_time()}s", True, WHITE)
    screen.blit(timer_text, (10, 10))

    # Draw hearts
    for i, heart in enumerate(hearts.sprites()):
        screen.blit(heart_image, (WIDTH // 2 - (NUM_HEARTS * 20) + (i * 40), 20))

   # Function to check if any sound is playing
    def is_sound_playing():
       return pygame.mixer.get_busy()

   # Play background sound when the game starts
    if showing_first_frame:
       background_sound.play()
       showing_first_frame = False
       background_sound_playing = True

    if is_lost and len(hearts) < NUM_HEARTS:
        print("Player lost a heart")  # Add this line for debugging
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        print("Playing lose_heart_sound")  # Add this line for debugging
        lose_heart_sound.play()

    # Play background sound when the player catches the flag
    if collisions_flags:
      if not is_sound_playing() and background_sound_playing:
          background_sound_playing = False
          background_sound.play()
      catch_flag_sound.play()

    # Play background sound when the game is won
    if is_won and not background_sound_playing:
       background_sound.play()
       background_sound_playing = True

    # Play background sound when the game is lost
    if is_lost and not background_sound_playing:
      background_sound.play()
      background_sound_playing = True

    
    # Draw flags collected
    flags_collected_text = info_font.render(f"Flags Collected: {flags_collected}/{NUM_FLAGS}", True, WHITE)
    screen.blit(flags_collected_text, (WIDTH - 200, 10))

    pygame.display.flip()
    clock.tick(FPS)