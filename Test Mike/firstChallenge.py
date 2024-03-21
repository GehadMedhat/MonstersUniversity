import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Initialize the mixer module
pygame.mixer.init()

# Load sounds
game_over_sound = pygame.mixer.Sound('game over.wav')
lose_life_sound = pygame.mixer.Sound('lose_live.wav')
game_sound = pygame.mixer.Sound('level1.mp3')


# Initialize the game width and height
screen_width = 1400
screen_height = 788


# Create a screen
screen = pygame.display.set_mode((screen_width, screen_height))


# Background
background_image = pygame.image.load('background1.jpg')


# Add Mike
mike_To_right = pygame.image.load('mike_right.png')
mike_To_left = pygame.image.load('mike_left.png')


mike_width, mike_height = mike_To_right.get_size()
mike_x = (screen_width - mike_width) // 2
mike_y = screen_height - mike_height - 10
mike_x_change = 5


# Add Enemy 1
enemyImg1 = pygame.image.load('enemy1.png')
enemy_width1, enemy_height1 = enemyImg1.get_size()


# Add Enemy 2
enemyImg2 = pygame.image.load('enemy2.png')
enemy_width2, enemy_height2 = enemyImg2.get_size()


# Add Enemy 3
enemyImg3 = pygame.image.load('enemy3.png')
enemy_width3, enemy_height3 = enemyImg3.get_size()


num_of_enemies = 30
enemies = []


# Set up timer
initial_game_time = 50  # Initial game time in seconds
current_time = initial_game_time * 1000  # Convert seconds to milliseconds
clock = pygame.time.Clock()


# Define mike class
class Mike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.mike_To_right = pygame.image.load('mike_right.png')
        self.mike_To_left = pygame.image.load('mike_left.png')
        self.image = pygame.image.load('mike.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.Vector2(0, 0)

    def set_direction(self, direction):
        if direction == 'right':
            self.image = self.mike_To_right
        elif direction == 'left':
            self.image = self.mike_To_left


# Create mike
mike = Mike(mike_x, mike_y)
all_sprites = pygame.sprite.Group(mike)

# Add a variable to control enemy spawn rate
enemy_spawn_rate = 1000  # Spawn a new enemy every 1000 milliseconds (1 second)
last_enemy_spawn_time = pygame.time.get_ticks()


def game_over():
    game_over_img = pygame.image.load('game_over.jpg')
    screen.blit(game_over_img, (screen_width, screen_height))
    screen.blit(game_over_img, (0, 0))

    pygame.display.flip()
    pygame.time.wait(7000)
    pygame.quit()
    sys.exit()


# To display an enemy
def show_Enemy(enemy_img, x, y):
    screen.blit(enemy_img, (x, y))


# To display lives
font = pygame.font.Font(None, 36)

# set up lives
initial_lives = 5
lives = initial_lives


# Life bar settings
life_icon_width = 30
life_icon_height = 30
life_icon_spacing = 10


# sound settings
sound_icon_width = 1200
sound_icon_height = 1200
sound_icon_spacing = 10


sound_on = pygame.image.load('soundOn.png')
sound_off = pygame.image.load('soundOff.png')
sound_icon_x = screen_width - (sound_icon_width + sound_icon_spacing)
sound_icon_y = 10

# variable to set sound state
sound_state = 'on'

# Function to toggle sound state
def toggle_sound(sound_state):
    return 'off' if sound_state == 'on' else 'on'

# Function to show lives
def show_Lives():
    liveIcon = pygame.image.load('live.png')
    for i in range(lives):
        life_icon_x = screen_width - (i + 1) * (life_icon_width + life_icon_spacing)
        life_icon_y = 10
        screen.blit(liveIcon, (life_icon_x, life_icon_y, life_icon_width, life_icon_height))


# To display time
def show_Time(time):
    font_time = pygame.font.Font(None, 36)
    seconds = max(time // 1000, 0)
    time_text = font_time.render("Time: {}s".format(seconds), True, (255, 255, 255))
    screen.blit(time_text, (10, 10))



# The main game loop
running = True
while running:
    game_sound.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if sound_icon_x <= mouse_x <= sound_icon_x + sound_icon_width and \
                    sound_icon_y <= mouse_y <= sound_icon_y + sound_icon_height:
                sound_state = toggle_sound(sound_state)
                if sound_state == 'on':
                    pygame.mixer.unpause()
                else:
                    pygame.mixer.pause()

    screen.blit(background_image, (0, 0))

    # Handle key presses outside the event loop for better responsiveness
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mike.set_direction('left')
        mike.velocity.x = -mike_x_change
    elif keys[pygame.K_RIGHT]:
        mike.set_direction('right')
        mike.velocity.x = mike_x_change
    else:
        mike.velocity.x = 0

    # Update Mike's position
    mike.rect.x += mike.velocity.x

    # Boundary check for the left edge
    if mike.rect.left < 0:
        mike.rect.left = 0

    # Boundary check for the right edge
    if mike.rect.right > screen_width:
        mike.rect.right = screen_width


    # Draw sprites
    all_sprites.draw(screen)

    # Update existing enemy positions
    for enemy in enemies:
        enemy[1] += enemy[3]  # Update x position
        enemy[2] += enemy[4]  # Update y position

        # Check for collision with Mike
        if mike.rect.colliderect(pygame.Rect(enemy[1], enemy[2], enemy[0].get_width(), enemy[0].get_height())):
            # Reduce lives and reset enemy position
            lose_life_sound.play()
            lives -= 1
            enemy[2] = random.randint(-300, -50)
            enemy[1] = random.randint(0, screen_width - enemy[0].get_width())

    # Add new enemies at a regular interval
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > enemy_spawn_rate:
        # Randomize the enemy type
        enemy_type = random.randint(1, 3)

        if enemy_type == 1:
            enemy_x = random.randint(0, screen_width - enemy_width1)
            enemy_y = random.randint(-300, -50)
            enemy_x_change = 0
            enemy_y_change = 3.7
            enemies.append([enemyImg1, enemy_x, enemy_y, enemy_x_change, enemy_y_change])
        elif enemy_type == 2:
            enemy_x = random.randint(0, screen_width - enemy_width2)
            enemy_y = random.randint(-300, -50)
            enemy_x_change = 0
            enemy_y_change = 3.7
            enemies.append([enemyImg2, enemy_x, enemy_y, enemy_x_change, enemy_y_change])
        elif enemy_type == 3:
            enemy_x = random.randint(0, screen_width - enemy_width3)
            enemy_y = random.randint(-300, -50)
            enemy_x_change = 0
            enemy_y_change = 3.7
            enemies.append([enemyImg3, enemy_x, enemy_y, enemy_x_change, enemy_y_change])

        last_enemy_spawn_time = current_time


    # Draw enemies
    for enemy in enemies:
        show_Enemy(enemy[0], enemy[1], enemy[2])


    # Draw time
    show_Time(current_time)

    # Draw lives
    show_Lives()

    if sound_state == 'on':
        screen.blit(sound_on, (sound_icon_x, sound_icon_y, sound_icon_width, sound_icon_height))
    elif sound_state == 'off':
        screen.blit(sound_off, (sound_icon_x, sound_icon_y, sound_icon_width, sound_icon_height))

    pygame.display.flip()

    # Update the timer
    elapsed_time = clock.tick(60)  # Get elapsed time since the last frame
    current_time -= elapsed_time

    if lives <= 0:
        game_over_sound.play()
        game_over()
        running = False
    elif current_time == 50:
        game_over_sound.play()
        game_over()
        running = False


# Quit pygame
pygame.quit()
sys.exit()