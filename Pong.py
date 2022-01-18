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

    # Draw the (left) paddle
    pygame.draw.rect(screen, WHITE, [30, 50, 30, 70])

    # Update screen
    pygame.display.flip()

    # Set framerate
    clock.tick(60)

pygame.quit()