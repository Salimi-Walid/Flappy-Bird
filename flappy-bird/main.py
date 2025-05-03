import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load assets
bg = pygame.image.load("flappy-bird/assets/images/background-day.png")
ground = pygame.image.load("flappy-bird/assets/images/base.png")
pipe_surface = pygame.image.load("flappy-bird/assets/images/pipe-green.png")
bird_surface = pygame.image.load("flappy-bird/assets/images/yellowbird-midflap.png")
game_over_surface = pygame.image.load("flappy-bird/assets/images/UI/gameover.png")

# Load sound effects
hit_sound = pygame.mixer.Sound("flappy-bird/assets/audio/hit.wav")

# Load number images for score
number_images = [pygame.image.load(f"flappy-bird/assets/images/UI/Numbers/{i}.png") for i in range(10)]

# Set the title of the window
pygame.display.set_caption("Flappy Bird")

# Bird variables
bird_x = 100
bird_y = SCREEN_HEIGHT // 2
bird_movement = 0
gravity = 0.25

# Pipe variables
pipe_list = []
PIPE_GAP = 150
pipe_speed = 3
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)  # Spawn pipes every 1.2 seconds

# Game state
game_active = True
hit_sound_played = False  # Flag to ensure hit sound plays only once

# Score variables
score = 0
high_score = 0

# Function to create pipes
def create_pipe():
    pipe_height = random.randint(150, SCREEN_HEIGHT - PIPE_GAP - 150)
    bottom_pipe = pipe_surface.get_rect(midtop=(SCREEN_WIDTH + 50, pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom=(SCREEN_WIDTH + 50, pipe_height - PIPE_GAP))
    return bottom_pipe, top_pipe

# Function to check collisions
def check_collision():
    global game_active, hit_sound_played
    # Check if bird hits the ground
    if bird_y + bird_surface.get_height() >= SCREEN_HEIGHT - ground.get_height():
        if not hit_sound_played:
            hit_sound.play()
            hit_sound_played = True
        return False
    # Check if bird hits pipes
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            if not hit_sound_played:
                hit_sound.play()
                hit_sound_played = True
            return False
    return True

# Function to restart the game
def restart_game():
    global bird_y, bird_movement, pipe_list, game_active, score, hit_sound_played
    bird_y = SCREEN_HEIGHT // 2
    bird_movement = 0
    pipe_list.clear()
    game_active = True
    score = 0  # Reset score
    hit_sound_played = False  # Reset sound flag

# Function to display score using images
def display_score(score, x, y):
    score_str = str(score)
    for i, digit in enumerate(score_str):
        digit_image = number_images[int(digit)]
        screen.blit(digit_image, (x + i * digit_image.get_width(), y))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:  # Move the bird up when SPACE is pressed
                bird_movement = -6
            if event.key == pygame.K_SPACE and not game_active:  # Restart the game
                restart_game()
        if event.type == SPAWN_PIPE and game_active:
            pipe_list.extend(create_pipe())

    # Draw the background
    for x in range(0, SCREEN_WIDTH, bg.get_width()):
        screen.blit(bg, (x, 0))

    if game_active:
        # Bird movement
        bird_movement += gravity
        bird_y += bird_movement
        bird_rect = bird_surface.get_rect(center=(bird_x, bird_y))

        # Draw pipes
        pipe_list = [pipe.move(-pipe_speed, 0) for pipe in pipe_list]
        for pipe in pipe_list:
            if pipe.bottom >= SCREEN_HEIGHT:  # Bottom pipe
                screen.blit(pipe_surface, pipe)
            else:  # Top pipe (flipped)
                flipped_pipe = pygame.transform.flip(pipe_surface, False, True)
                screen.blit(flipped_pipe, pipe)

        # Remove pipes that are off-screen
        pipe_list = [pipe for pipe in pipe_list if pipe.right > 0]

        # Check for collisions
        game_active = check_collision()

        for pipe in pipe_list:
            if pipe.centerx < bird_x and pipe.centerx > bird_x - pipe_speed:
                score += 1

        # Draw the bird
        screen.blit(bird_surface, bird_rect)
    else:
        # Display "Game Over" screen
        screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2,
                                        SCREEN_HEIGHT // 2 - game_over_surface.get_height() // 2))

    # Draw the ground
    ground_y = SCREEN_HEIGHT - ground.get_height()
    for x in range(0, SCREEN_WIDTH, ground.get_width()):
        screen.blit(ground, (x, ground_y))

    # Draw the score
    display_score(score, 10, 10)  # Top-left corner

    # Update the display
    pygame.display.update()
    clock.tick(60)