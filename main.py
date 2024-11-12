# 1. Gör så att racketen är lila istället för grå.
# 2. Gör så att 2 cirklar spawnar istället för 1.
# 3. Gör så att racketen också kan röra sig upp och ner.
# 
# (Utmaning)
# Döp om Score till Dryness.
# Gör så att Dryness börjar på 5, och räknar ner istället för upp.
# Om Dryness når 0, ska spelet pausa och visa "Game Over".

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tearcatcher")

# Colors
TEXT_COLOR = (255, 255, 255)
PAPER_COLOR = (255, 255, 255)
PADDLE_COLOR = (128, 128, 128)
TEARS_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (0, 0, 0)

# Clock to control frame rate
clock = pygame.time.Clock()

# Paddle properties
paddle_width = 100
paddle_height = 20
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - paddle_height - 75
paddle_speed = 7

# Circle properties
circle_radius = 15
circle_speed = 5
circle_spawn_time = 0
circles = []

# White rectangle at the bottom
white_rect = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

# Score counter
score = 0
font = pygame.font.SysFont(None, 36)  # Font for displaying score

# Game loop
running = True
while running:
    dt = clock.tick(60)  # Time since last tick in milliseconds
    circle_spawn_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn circles
    if circle_spawn_time >= 1500:
        x_pos = random.randint(circle_radius, WIDTH - circle_radius)
        circles.append([x_pos, -circle_radius])  # Start above the screen
        circle_spawn_time = 0

    # Get pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # Move circles down and check for collisions
    for circle in circles[:]:
        circle[1] += circle_speed

        # Create rect for circle for collision detection
        circle_rect = pygame.Rect(circle[0] - circle_radius, circle[1] - circle_radius, circle_radius * 2, circle_radius * 2)
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

        # Check for collision with paddle
        if circle_rect.colliderect(paddle_rect):
            circles.remove(circle)
            score += 1  # Increment score
        # Check for collision with white rectangle at bottom
        elif circle_rect.colliderect(white_rect):
            circles.remove(circle)
        # Remove circles that have fallen off the screen (in case they slip past the rectangle)
        elif circle[1] - circle_radius > HEIGHT:
            circles.remove(circle)

    # Drawing
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(screen, PAPER_COLOR, white_rect)
    pygame.draw.rect(screen, PADDLE_COLOR, (paddle_x, paddle_y, paddle_width, paddle_height))
    for circle in circles:
        pygame.draw.circle(screen, TEARS_COLOR, (int(circle[0]), int(circle[1])), circle_radius)

    # Display score
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
