import pygame
pygame.init()

# Create screen
screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)

running = True
while running:

    # Check events
    for event in pygame.event.get():
        # If user clicked the quit button, end loop
        if event.type == pygame.QUIT:
            running = False

    # Draw things onto the screen
    # TODO

    # Update screen
    pygame.display.flip()

    # Set framerate
    # TODO

