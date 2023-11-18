import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
DEFAULT_PADDLE_SPEED = 6  # Default paddle speed
PADDLE_SPEED = DEFAULT_PADDLE_SPEED
DEFAULT_BALL_SPEED = 6  # Default ball speed
BALL_SPEED = DEFAULT_BALL_SPEED
MAX_SPEED = 20
DEFAULT_ACCELERATION_FACTOR = 1.15  # Default acceleration factor
ACCELERATION_FACTOR = DEFAULT_ACCELERATION_FACTOR
MAX_ACCELERATION_FACTOR = 2.5
SLOWMO_DURATION = 5 * 60  # 5 seconds in frames

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PO(G)NG")  # Change the game caption

# Paddle objects
player1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball object
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed = [BALL_SPEED, BALL_SPEED]  # Ball speed in x and y direction
ball_angle = random.uniform(-math.pi / 4, math.pi / 4)  # Random angle for initial direction
ball_speed[0] *= math.cos(ball_angle)
ball_speed[1] *= math.sin(ball_angle)

# Slow-motion ability variables
slowmo_active = False
slowmo_duration = 0
slowmo_cooldown = 0

# Strike counter
streak_counter = 1
font = pygame.font.Font(None, 36)  # Font for streak counter

clock = pygame.time.Clock()
TICK_RATE_NORMAL = 60  # Normal tick rate (60 frames per second)
TICK_RATE_SLOW = 30  # Slow tick rate (30 frames per second)
current_tick_rate = TICK_RATE_NORMAL  # Set initial tick rate to normal

running = True

# Main game loop
while running:
    clock.tick(current_tick_rate)  # Set the clock tick based on current_tick_rate
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Activate slow-motion ability
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            current_tick_rate = TICK_RATE_SLOW  # Change tick rate to slow (30 FPS)

        # Deactivate slow-motion ability
        if event.type == pygame.KEYUP and event.key == pygame.K_e:
            current_tick_rate = TICK_RATE_NORMAL  # Restore tick rate to normal (60 FPS)

    keys = pygame.key.get_pressed()

    # Player movement
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += PADDLE_SPEED

    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += PADDLE_SPEED

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with walls (top, bottom, left, right)
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] *= -1
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1

    # Ball collision with paddles
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed[0] *= -1
        ball_speed[1] *= random.uniform(0.9, 1.1)  # Randomize bounce off angle slightly
        streak_counter += 1
        ball_speed[0] *= ACCELERATION_FACTOR ** streak_counter
        ball_speed[1] *= ACCELERATION_FACTOR ** streak_counter

        # Limit the maximum ball speed and acceleration factor
        BALL_SPEED = min(MAX_SPEED, BALL_SPEED)
        ACCELERATION_FACTOR = min(MAX_ACCELERATION_FACTOR, ACCELERATION_FACTOR)

    # Slow-motion ability logic
    if slowmo_active:
        if slowmo_duration > 0:
            slowmo_duration -= 1
        else:
            slowmo_active = False
            BALL_SPEED = DEFAULT_BALL_SPEED  # Restore default ball speed
            PADDLE_SPEED = DEFAULT_PADDLE_SPEED  # Restore default paddle speed

    # Reduce slow-motion ability cooldown
    if slowmo_cooldown > 0:
        slowmo_cooldown -= 1

    # Render streak counter text
    streak_text = font.render(f"Streak: {streak_counter}", True, WHITE)
    win.blit(streak_text, (WIDTH // 2 - 70, 20))  # Display streak counter on the screen

    # Drawing objects
    pygame.draw.rect(win, WHITE, player1)
    pygame.draw.rect(win, WHITE, player2)
    pygame.draw.ellipse(win, WHITE, ball)

    # Update the display
    pygame.display.flip()

pygame.quit()
