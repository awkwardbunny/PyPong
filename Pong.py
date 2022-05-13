import math
import random
import pygame


class Rect:
    def __init__(self, sx, sy, ex, ey):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey


def is_colling(first: Rect, second: Rect) -> bool:
    dx1 = first.sx - second.ex  # + if first box is to the right of second box
    dx2 = second.sx - first.ex  # + if first box is to the left of second box
    dy1 = first.sy - second.ey  # + if first box is to the below of second box
    dy2 = second.sy - first.ey  # + if first box is to the above of second box

    # print(dx1, dx2, dy1, dy2)

    if dx1 > 0 or dx2 > 0:
        return False

    if dy1 > 0 or dy2 > 0:
        return False
    return True


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


def add_coords(a: Coord, b: Coord):
    sum = Coord(a.x, a.y)
    sum.add(b)
    return sum


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
                 size: Coord = Coord(10, 10)
                 ):
        self.color = color
        self.position = position
        self.starting_pos = Coord(position.x, position.y)
        self.size = size
        self.max_speed = 5

        self.speed = Coord(random.randint(-100, 100), random.randint(-100, 100))
        self.speed.normalize(self.max_speed)

    def bounce_x(self):
        self.speed.x = -1 * self.speed.x

    def bounce_y(self):
        self.speed.y = -1 * self.speed.y

    def move_relative(self, offset: Coord):
        self.position.add(offset)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color.get_tuple(), [self.position.x, self.position.y, self.size.x, self.size.y])

    def get_bounds(self) -> Rect:
        end = add_coords(self.position, self.size)
        return Rect(self.position.x, self.position.y, end.x, end.y)

    def update(self):
        self.move_relative(self.speed)

    def reset(self):
        self.position = Coord(self.starting_pos.x, self.starting_pos.y)


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

    def get_bounds(self) -> Rect:
        end = add_coords(self.position, self.size)
        return Rect(self.position.x, self.position.y, end.x, end.y)

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
        self.pong = Ball(self.foreground_color, ball_position, ball_size)

        # Keep track of score
        self.l_score = 0
        self.r_score = 0

        self.screen = None
        self.clock = None
        self.running = False
        self.font = None

    # Initialize pygame and start game loop
    def start(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode(self.dimension.get_tuple())
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40)

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

        # Draw center line
        for y in range(0, self.dimension.y, 40):
            pygame.draw.rect(self.screen, self.foreground_color.get_tuple(), [self.dimension.x/2 - 2, y, 4, 20])

        # Draw score
        left_score = self.font.render(str(self.l_score), False, self.foreground_color.get_tuple())
        right_score = self.font.render(str(self.r_score), False, self.foreground_color.get_tuple())
        self.screen.blit(left_score, (340, 40))
        self.screen.blit(right_score, (440, 40))

        pygame.display.flip()

    def update(self):
        self.l_paddle.update()  # Update left paddle position
        self.r_paddle.update()  # Update right paddle position
        self.pong.update()

        # Check pong/paddle collisions
        if is_colling(self.pong.get_bounds(), self.l_paddle.get_bounds()) and self.pong.speed.x < 0:
            print("Collided with left paddle")
            self.pong.bounce_x()
        if is_colling(self.pong.get_bounds(), self.r_paddle.get_bounds()) and self.pong.speed.x > 0:
            print("Collided with right paddle")
            self.pong.bounce_x()

        # Check pong/window collisions (up and down)
        top_bound = Rect(-10, -10, self.dimension.x + 10, 0)
        bottom_bound = Rect(-10, self.dimension.y + 10, self.dimension.x + 10, self.dimension.y + 10)
        if is_colling(self.pong.get_bounds(), top_bound) and self.pong.speed.y < 0:
            print("Collided with top")
            self.pong.bounce_y()
        if is_colling(self.pong.get_bounds(), bottom_bound) and self.pong.speed.y > 0:
            print("Collided with bottom")
            self.pong.bounce_y()

        # Check pong/window collisions (left and right)
        left_bound = Rect(-10, -10, 0, self.dimension.y + 10)
        right_bound = Rect(self.dimension.x, -10, self.dimension.x + 10, self.dimension.y + 10)
        if is_colling(self.pong.get_bounds(), left_bound) and self.pong.speed.x < 0:
            print("Collided with left")
            self.r_score += 1
            print(f"Score is {self.l_score}:{self.r_score}")
            self.pong.reset()

        if is_colling(self.pong.get_bounds(), right_bound) and self.pong.speed.x > 0:
            print("Collided with right")
            self.l_score += 1
            print(f"Score is {self.l_score}:{self.r_score}")
            self.pong.reset()

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
