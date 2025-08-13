import pygame
import sys
import random

# Initialize the game
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Game window setup
frame_size_x = 720
frame_size_y = 480
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255) # Changed to pure white for better contrast
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# FPS controller
fps_controller = pygame.time.Clock()
difficulty = 50

# Snake variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
score = 0

# Apple variables
apple_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
apple_spawn = True

# --- Main Game Loop ---
while True:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    direction = change_to

    # --- Snake Movement ---
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # --- Snake Growth & Apple Collision ---
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == apple_pos[0] and snake_pos[1] == apple_pos[1]:
        score += 1
        apple_spawn = False  # Set to False to trigger new apple generation
    else:
        snake_body.pop() # Remove the tail if no apple was eaten

    # --- Apple Spawning ---
    if not apple_spawn:
        apple_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    apple_spawn = True

    # --- Drawing ---
    game_window.fill(black) # Use black for a more classic feel

    # Draw Snake
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw Apple - THIS IS THE KEY FIX
    pygame.draw.rect(game_window, red, pygame.Rect(apple_pos[0], apple_pos[1], 10, 10))

    # --- Game Over Conditions ---
    # Wall collision
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        pygame.quit()
        sys.exit()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        pygame.quit()
        sys.exit()
    # Body collision
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            pygame.quit()
            sys.exit()

    # --- Update Screen and Control Speed ---
    pygame.display.update()
    fps_controller.tick(difficulty)