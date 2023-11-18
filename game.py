import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
DEFAULT_PADDLE_SPEED = 6
PADDLE_SPEED = DEFAULT_PADDLE_SPEED
DEFAULT_BALL_SPEED = 6
BALL_SPEED = DEFAULT_BALL_SPEED
MAX_SPEED = 20
DEFAULT_ACCELERATION_FACTOR = 1.15
ACCELERATION_FACTOR = DEFAULT_ACCELERATION_FACTOR
MAX_ACCELERATION_FACTOR = 2.5
SLOWMO_DURATION = 5 * 60
RESET_DELAY = 3 * 60  # 3 seconds in frames before ball reset

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Paddle objects
player1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball object
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed = [BALL_SPEED, BALL_SPEED]
reset_delay = 0  # Countdown before ball reset

# Score variables
score_player1 = 0
score_player2 = 0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
TICK_RATE_NORMAL = 60
TICK_RATE_SLOW = 30
current_tick_rate = TICK_RATE_NORMAL

running = True

def reset_ball():
    global reset_delay
    ball.center = (WIDTH // 2, HEIGHT // 2)
    reset_delay = RESET_DELAY

# Main game loop
while running:
    clock.tick(current_tick_rate)
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            current_tick_rate = TICK_RATE_SLOW
        if event.type == pygame.KEYUP and event.key == pygame.K_e:
            current_tick_rate = TICK_RATE_NORMAL

        # Check for spacebar to start a new round
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and reset_delay == 0:
            score_player1 = 0
            score_player2 = 0
            reset_ball()

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
    if reset_delay == 0:
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Ball collision with walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] *= -1

        # Ball collision with paddles
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed[0] *= -1
            ball_speed[1] *= random.uniform(0.9, 1.1)
            ball_speed[0] *= ACCELERATION_FACTOR
            ball_speed[1] *= ACCELERATION_FACTOR

            # Limit the maximum ball speed and acceleration factor
            BALL_SPEED = min(MAX_SPEED, BALL_SPEED)
            ACCELERATION_FACTOR = min(MAX_ACCELERATION_FACTOR, ACCELERATION_FACTOR)

    else:
        reset_delay -= 1
        if reset_delay == 0:
            reset_ball()

    # Ball out of bounds - scoring
    if ball.left <= 0:
        score_player2 += 1
        reset_ball()

    elif ball.right >= WIDTH:
        score_player1 += 1
        reset_ball()

    # Drawing objects
    pygame.draw.rect(win, WHITE, player1)
    pygame.draw.rect(win, WHITE, player2)
    pygame.draw.ellipse(win, WHITE, ball)

    # Render scores
    score_text = font.render(f"{score_player1} - {score_player2}", True, WHITE)
    win.blit(score_text, (WIDTH // 2 - 50, 20))

    # Update the display
    pygame.display.flip()

pygame.quit()
