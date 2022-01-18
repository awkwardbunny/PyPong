import pygame
pygame.init()

# Create screen
screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Pong")

# Get pygame clock
clock = pygame.time.Clock()

# Define some colors
BLUE = (25, 151, 224)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

paddle_size = [30, 70]
left_paddle = [30, 50]

running = True
while running:

    # Check events
    for event in pygame.event.get():
        # If user clicked the quit button, end loop
        if event.type == pygame.QUIT:
            running = False

    # Process user input
    # TODO

    # Draw things onto the screen
    # TODO
    screen.fill(BLACK)

    # Add 1 to Y coordinate
    left_paddle[1] += 1
    if left_paddle[1] > 100:
        left_paddle[1] = 50

    # Draw the (left) paddle
    pygame.draw.rect(screen, WHITE, [left_paddle[0], left_paddle[1], paddle_size[0], paddle_size[1]])

    # Update screen
    pygame.display.flip()

    # Set framerate
    clock.tick(60)

pygame.quit()