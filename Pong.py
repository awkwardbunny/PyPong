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
GRAY = (200, 200, 200)

paddle_size = [20, 90]
left_paddle = [30, 50]
right_paddle = [750, 50]

pong = [400, 250]
pong_size = [24, 24]

going_up = False
going_down = False

running = True
while running:

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if user clicked the quit button
            running = False  # end loop
        elif event.type == pygame.KEYDOWN:  # this will run when a key is pressed
            # Check WHICH key was pressed
            if event.key == pygame.K_UP:  # if the UP key was pressed
                going_up = True
                going_down = False
            elif event.key == pygame.K_DOWN:  # if the DOWN key was pressed
                going_up = False
                going_down = True
        elif event.type == pygame.KEYUP:  # this will run when a key is released
            if event.key == pygame.K_UP:  # if the UP key was released
                going_up = False  # stop moving up
            if event.key == pygame.K_DOWN:  # if the DOWN key was released
                going_down = False  # stop moving down

    if going_up:
        if right_paddle[1] > 0:  # check if at the top of screen
            right_paddle[1] -= 4
        if left_paddle[1] > 0:  # check if at the top of screen
            left_paddle[1] -= 4
    elif going_down:
        if right_paddle[1] + paddle_size[1] < 500:  # check if (the bottom left corner) is at bottom of screen
            right_paddle[1] += 4
        if left_paddle[1] + paddle_size[1] < 500:  # check if (the bottom left corner) is at bottom of screen
            left_paddle[1] += 4

    '''
    # Draw things onto the screen
    ## pygram.draw.rect takes 3 arguments:
    ## -> screen: on WHAT to draw the rectangle on
    ## -> color: what color to draw in
    ## -> [x, y, width, height]
    '''
    # Clear screen to black
    screen.fill(BLACK)
    # Draw the (right) paddle
    pygame.draw.rect(screen, GRAY, [right_paddle[0], right_paddle[1], paddle_size[0], paddle_size[1]])
    # Draw the (left) paddle
    pygame.draw.rect(screen, GRAY, [left_paddle[0], left_paddle[1], paddle_size[0], paddle_size[1]])
    # Draw dotted line down the middle
    for y in range(0, screen_size[1], 40):
        pygame.draw.rect(screen, GRAY, [395, y, 10, 20])
    # Draw pong
    pygame.draw.rect(screen, GRAY, [pong[0], pong[1], pong_size[0], pong_size[1]])

    # Update screen
    pygame.display.flip()

    # Set framerate
    clock.tick(60)

pygame.quit()