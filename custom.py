import pygame
import random
import time

# main variable
PLAYING = True
MOVE_UP = MOVE_DOWN = MOVE_RIGHT = MOVE_LEFT = MOVE_INIT = False

# other int variables
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
STEP = 23 # used for random num generation
SPEED = 75

class Snake(object):
    def __init__(self):
        # loading snake images
        self.head = pygame.image.load("head.png").convert_alpha() 
        self.head = pygame.transform.scale(self.head, (35, 35))
        self.body_part_1 = pygame.image.load("body.png").convert_alpha()
        self.body_part_1 = pygame.transform.scale(self.body_part_1, (25, 25))
       
        # each item of lists will store coordinates of one body part of snake
        self.x_position = [0]
        self.y_position = [0]
        
        self.length = 2
        self.increase_size()        
        
        self.score = 0
        
    def get_head_position(self):
        # position of head of snake, first square in 
        # positions property
        return (self.x_position[0], self.y_position[0])

    # increasing size of list to potentially have 1000 sections for snake
    # when snake gets bigger, list will have 1,000 items already created to store new body part's coordinates
    def increase_size(self):
        for i in range(0,1000):
            self.x_position.append(-100)
            self.y_position.append(-100)
 
    def collision(x_1, y_1, x_2, y_2, size_snake, size_fruit):
        if ((x_1 + size_snake >= x_2) or (x_1 >= x_2) and x_1 <= x_2 + size_fruit):
            if ((y_1 >= y_2) or (y_1 + size_snake >= y_2) and y_1 <= y_2 + size_fruit):
                return True
            return False

    def move(self):
        # move each body part of body by giving them new coordinates
        # each part of the snake will take positions of the part before it
        # give updated coordinates to entire snake by doing this on entire list
        for i in range(self.length - 1, 0, -1):
            self.x_position[i] = self.x_position[(i-1)]
            self.y_position[i] = self.y_position[(i-1)]

    # # reset length, positions, direction, and score
    # def reset(self):
    #     self.length = 1
    #     self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT /2))]
    #     self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    #     self.score = 0

    def handle_keys(self):
        global MOVE_RIGHT
        global MOVE_LEFT
        global MOVE_UP
        global MOVE_DOWN
        global MOVE_INIT

        for event in pygame.event.get():

            #checking if user quits game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                PLAYING = False

            #checking if user presses key
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    if MOVE_UP == False and MOVE_INIT == True:
                        # if moving down, can't move up
                        if MOVE_DOWN == True:
                            MOVE_UP == False

                        else:
                            # otherwise, change values to other directions to false
                            # and change MOVE_UP to true
                            MOVE_DOWN = MOVE_RIGHT = MOVE_LEFT = False
                            MOVE_UP = MOVE_INIT = True

                if event.key == pygame.K_DOWN:
                    if MOVE_DOWN == False:
                        # if moving up, can't move down
                        if MOVE_UP == True:
                            MOVE_DOWN == False
                            
                        else:
                            
                            MOVE_RIGHT = MOVE_LEFT = MOVE_UP = False 
                            MOVE_DOWN = MOVE_INIT = True

                if event.key == pygame.K_RIGHT:
                    if MOVE_RIGHT == False: 
                        # if moving left, can't move right
                        if MOVE_LEFT == True:
                            MOVE_RIGHT == False
                            
                        else:
                            # otherwise, moves right; all other directions set to false
                            MOVE_LEFT = MOVE_UP = MOVE_DOWN = False 
                            MOVE_RIGHT = MOVE_INIT = True

                if event.key == pygame.K_LEFT:
                    if MOVE_LEFT == False:
                        if MOVE_RIGHT == True:
                            MOVE_LEFT == False
                            
                        else:   
                            MOVE_RIGHT = MOVE_DOWN = MOVE_UP = False 
                            MOVE_LEFT = MOVE_INIT = True

class Food(object):
    def __init__(self):
        # loading food image
        self.fruit = pygame.image.load("fruit.png").convert_alpha()
        self.fruit = pygame.transform.scale(self.fruit, (35,35))
        self.position_fruit = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        # give random coordinates
        self.position_fruit = self.fruit.get_rect()
        self.position_fruit.x = random.randint(2,10)*STEP
        self.position_fruit.y = random.randint(2,10)*STEP


def main(): 
    # initialize game => will initialize display module
    pygame.init()

    # create single display Surface
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # load background image
    bg = pygame.image.load("background.jpg")

    # blit bg to window
    window.blit(bg, (0, 0))

    # create window caption
    pygame.display.set_caption("Cat's Snake Game")

    # create Snake and Food instances
    snake = Snake()
    food = Food()

    # blit head and first part of body
    window.blit(snake.body_part_1, (-5, 5))
    window.blit(snake.head, (snake.x_position[0], snake.y_position[0]))

    # blit fruit
    window.blit(food.fruit, food.position_fruit)

    # update contents of entire display
    pygame.display.flip()

    # create continuous loop to keep screen visible
    while (PLAYING == True):
        snake.handle_keys() #invoke keystroke handler
        snake.move() # move snake

        # if snake collides with food
        if snake.get_head_position() == food.position_fruit:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        # blit score
        font = pygame.font.SysFont(None, 25)
        text = font.render("Score: {0}".format(snake.score), 1, (0, 0, 0))
        window.blit(text, (400, 10))

        # move each body part of body by giving them new coordinates
        # each part of the snake will take positions of the part before it
        # give updated coordinates to entire snake by doing this on entire list
        for i in range(snake.length - 1, 0, -1):
            snake.x_position[i] = snake.x_position[(i-1)]
            snake.y_position[i] = snake.y_position[(i-1)]

        #blit parts of snake on screen using updated coordinates
        for i in range(1, snake.length):
            window.blit(snake.body_part_1, (snake.x_position[i], snake.y_position[i]))
        
        # moving snake in certain direction if user presses key
        if MOVE_UP:
            snake.y_position[0] -= STEP 
            window.blit(bg, (0,0)) 
            window.blit(snake.head, (snake.x_position[0], snake.y_position[0]))

        if MOVE_DOWN:
            snake.y_position[0] += STEP
            window.blit(bg, (0,0))
            window.blit(snake.head, (snake.x_position[0], snake.y_position[0]))

        if MOVE_RIGHT:
            snake.x_position[0] += STEP
            window.blit(bg, (0,0))
            window.blit(snake.head, (snake.x_position[0], snake.y_position[0]))

        if MOVE_LEFT:
            snake.x_position[0] -= STEP
            window.blit(bg, (0,0))
            window.blit(snake.head, (snake.x_position[0], snake.y_position[0]))

        # Flipping to add everything on the board
        pygame.display.flip()

        # Delaying the game to make the snake move fluidly
        time.sleep (SPEED / 1000)

main()
