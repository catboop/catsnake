import sys
import random
import pygame

class Snake(object):
    def __init__(self):
        # start with length of one square
        self.length = 1
        # list of x, y positions for each square that makes up snake
        # start position at center of screen
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        # direction snake is headed
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        # color of snake
        self.color = (11, 102, 35)
        # starting score
        self.score = 0

    def get_head_position(self):
        # position of head of snake, first square in positions property
        return self.positions[0]

    def turn(self, point):
        # if one block, can move any of four directions; otherwise, can only move three ways
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    # need to calc new position given current position
    def move(self):
        # current position of snake's head
        cur = self.get_head_position()
        # current direction of snake
        x, y = self.direction
        # calc new position of head of snake using gridsize
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)

        # if snake runs into itself, reset
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()

        else:
            # add new head position and pop last position
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    # reset length, positions, direction, and score
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT /2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
    
    # ??
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)
    
    # ??
    def handle_keys(self):
        # collecting all events
        for event in pygame.event.get():

            # if user quits
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # key strokes corresponding with turning directions
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                # quits game
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (250, 128, 114)
        self.randomize_position()

    # randomize position of food
    def randomize_position(self):
        # use random module
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

    # ??
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)
        

# grid
def drawGrid(surface):
    # double for loop to iterate over each x,y coordinate on our grid
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (152, 251, 152), r)
            else:
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (144, 237, 144), rr)

# global variables to keep track of features of game
# screen size
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

# grid size
GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

# movements of snake
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# main game loop, will run continuously until game is exited
def main():
    # initialize game
    pygame.init()

    # initialize game clock to keep track of action at given time
    clock = pygame.time.Clock()

    # set display window name
    pygame.display.set_caption("Cat's Snake Game")

    # create display surface object
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    # re-draw screen whenever action is performed
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()


    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace",25)

    # continuous loop
    while (True):
        clock.tick(10)
        snake.handle_keys() #invoke keystroke handler
        drawGrid(surface) # re-draw grid
        snake.move() # move snake

        # if snake collides with food
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface,(0, 0))
        text = myfont.render("Score: {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()

main()