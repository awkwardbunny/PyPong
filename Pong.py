import math
import random
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

    def normalize(self, max):
        magnitude = math.sqrt(self.x ** 2 + self.y ** 2)
        self.x *= max / magnitude
        self.y *= max / magnitude


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def get_tuple(self):
        return self.r, self.g, self.b


class Ball:
    def __init__(self,
                 color: Color,
                 position: Coord,
                 screen_size: Coord,
                 size: Coord = Coord(10, 10)
                 ):
        self.color = color
        self.position = position
        self.size = size
        self.max_speed = 5
        self.screen_size = screen_size

        self.speed = Coord(random.randint(-100, 100), random.randint(-100, 100))
        self.speed.normalize(self.max_speed)

    def bounce_x(self):
        self.speed.x = -1 * self.speed.x

    def bounce_y(self):
        self.speed.y = -1 * self.speed.y

    def move_relative(self, offset: Coord):
        self.position.add(offset)
        if self.position.y <= 0 or self.position.y + self.size.y >= self.screen_size.y:
            self.bounce_y()
        elif self.position.x <= 0 or self.position.x + self.size.x >= self.screen_size.x:
            self.bounce_x()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color.get_tuple(), [self.position.x, self.position.y, self.size.x, self.size.y])

    def update(self):
        self.move_relative(self.speed)


class Paddle:
    def __init__(self,
                 color: Color,
                 position: Coord,
                 max_y: int,
                 size: Coord = Coord(20, 90)
                 ):
        self.color = color
        self.position = position
        self.size = size
        self.speed = 0
        self.max_y = max_y

    def move_relative(self, offset: Coord):
        self.position.add(offset)
        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y + self.size.y > self.max_y:
            self.position.y = self.max_y - self.size.y

    def move_absolute(self, new_position: Coord):
        self.position = new_position

    def draw(self, screen):
        pygame.draw.rect(screen, self.color.get_tuple(), [self.position.x, self.position.y, self.size.x, self.size.y])

    def set_speed(self, speed: int):
        self.speed = speed

    def update(self):
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

        self.paddle_speed = 5
        self.pong_speed = 5

        # Create our paddles
        self.l_paddle = Paddle(self.foreground_color, Coord(30, 50), self.dimension.y)
        self.r_paddle = Paddle(self.foreground_color, Coord(750, 50), self.dimension.y)

        # Calculate middle of screen
        middle = self.dimension.y / 2
        half_height = self.l_paddle.size.y / 2 # Assuming both paddles are same size
        self.l_paddle.position.y = middle - half_height
        self.r_paddle.position.y = middle - half_height

        middle_y = self.dimension.y / 2
        middle_x = self.dimension.x / 2
        ball_size = Coord(20, 20)
        ball_position = Coord(middle_x - 10, middle_y - 10)

        # Create our pong (Ball)
        self.pong = Ball(self.foreground_color, ball_position, self.dimension, ball_size)

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

        self.pong.draw(self.screen)

        # TODO: Draw center line
        # TODO: Draw score
        pygame.display.flip()

    def update(self):
        self.l_paddle.update()  # Update left paddle position
        self.r_paddle.update()  # Update right paddle position
        self.pong.update()

        # TODO: Check pong/paddle collisions
        # ppos = self.pong.position
        # lpos = self.l_paddle.position
        # rpos = self.r_paddle.position
        #
        # if lpos.x + self.l_paddle.size.x <= ppos.x and (ppos.y > lpos.y and ppos.y + self.pong.size.y < self.l_paddle.size.y + lpos.y):
        #     self.pong.bounce_y()

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
                    self.r_paddle.set_speed(-1 * self.paddle_speed)
                elif event.key == pygame.K_DOWN:
                    self.r_paddle.set_speed(self.paddle_speed)
                elif event.key == pygame.K_w:
                    self.l_paddle.set_speed(-1 * self.paddle_speed)
                elif event.key == pygame.K_s:
                    self.l_paddle.set_speed(self.paddle_speed)
                elif event.key == pygame.K_q:
                    self.running = False
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
