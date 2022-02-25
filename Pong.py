import pygame


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self):
        return self.x, self.y

    def add(self, other: "Coord"):
        self.x += other.x
        self.y += other.y


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def get_tuple(self):
        return self.r, self.g, self.b


class Paddle:
    def __init__(self,
                 color: Color,
                 position: Coord,
                 size: Coord = Coord(20, 90)
                 ):
        self.color = color
        self.position = position
        self.size = size
        self.speed = 0

    def move_relative(self, offset: Coord):
        self.position.add(offset)

    def move_absolute(self, new_position: Coord):
        self.position = new_position

    def draw(self, screen):
        pygame.draw.rect(screen, self.color.get_tuple(), [self.position.x, self.position.y, self.size.x, self.size.y])

    def set_speed(self, speed: int):
        self.speed = speed

    def update(self):
        # TODO: Limit check y
        self.move_relative(Coord(0, self.speed))


class Pong:
    def __init__(self,
                 dimension: Coord = Coord(800, 500),
                 title: str = "Pong v2",
                 ):
        self.dimension: Coord = dimension
        self.foreground_color = Color(180, 180, 180)
        self.background_color = Color(0, 0, 0)
        self.title = title

        self.paddle_speed = 10
        self.pong_speed = 5

        # Create our paddles
        self.l_paddle = Paddle(self.foreground_color, Coord(30, 50))
        self.r_paddle = Paddle(self.foreground_color, Coord(750, 50))

        # TODO: Create our pong
        # TODO: Keep track of score

        self.screen = None
        self.clock = None
        self.running = False

    # Initialize pygame and start game loop
    def start(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode(self.dimension.get_tuple())
        self.clock = pygame.time.Clock()

        self.running = True
        while self.running:
            self.loop()

    # Our main game loop
    def loop(self):
        self.process_inputs()
        self.update()
        self.draw()
        self.clock.tick(60)

    def draw(self):
        self.screen.fill(self.background_color.get_tuple())

        self.l_paddle.draw(self.screen)  # Draw left paddle
        self.r_paddle.draw(self.screen)  # Draw right paddle

        # TODO: Draw center line
        # TODO: Draw pong
        # TODO: Draw score
        pygame.display.flip()

    def update(self):
        self.l_paddle.update()  # Update left paddle position
        self.r_paddle.update()  # Update right paddle position

        # TODO: Update pong
        # TODO: Update score

    def process_inputs(self):
        # Check events
        for event in pygame.event.get():
            # Check if the 'X' button was pressed to quit
            if event.type == pygame.QUIT:
                self.running = False
            # Check user inputs
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.r_paddle.set_speed(-5)
                elif event.key == pygame.K_DOWN:
                    self.r_paddle.set_speed(5)
                elif event.key == pygame.K_w:
                    self.l_paddle.set_speed(-5)
                elif event.key == pygame.K_s:
                    self.l_paddle.set_speed(5)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    self.r_paddle.set_speed(0)
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    self.l_paddle.set_speed(0)


# Beginning of our program
if __name__ == "__main__":

    '''
    Create our game.
    Default parameters such as 'dimension' and 'title' can be overriden like so:
    'game = Pong(title = "Not Pong")'
    or
    'game = Pong(dimension = Coords(400, 400))'
    or both combined:
    'game = Pong(title = "Definitely not Pong", dimension = Coords(500, 500))'
    '''
    game = Pong()

    # Start our game
    game.start()
