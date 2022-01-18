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

going_up = False
going_down = False

running = True
while running:

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if user clicked the quit button
            running = False # end loop
        elif event.type == pygame.KEYDOWN: # this will run when a key is pressed
            # Check WHICH key was pressed
            if event.key == pygame.K_UP: # if the UP key was pressed
                going_up = True
                going_down = False
            elif event.key == pygame.K_DOWN: # if the DOWN key was pressed
                going_up = False
                going_down = True

    if going_up:
        left_paddle[1] -= 4
    elif going_down:
        left_paddle[1] += 4

    # Draw things onto the screen
    ## Clear screen to black
    screen.fill(BLACK)
    ## Draw the (left) paddle
    pygame.draw.rect(screen, WHITE, [left_paddle[0], left_paddle[1], paddle_size[0], paddle_size[1]])

    # Update screen
    pygame.display.flip()

    # Set framerate
    clock.tick(60)

pygame.quit()