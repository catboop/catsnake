import pygame
import random
import time

# main variable
PLAYING = True
MOVE_UP = MOVE_DOWN = MOVE_RIGHT = MOVE_LEFT = MOVE_INIT = False

# other int variables
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
STEP = 23 # used for random coordinate calc
SPEED = 75

class Snake(object):
    def __init__(self):
        # loading snake images
        self.head = pygame.image.load("kitcat.png").convert_alpha() 
        self.head = pygame.transform.scale(self.head, (50, 50))
        self.body_part = pygame.image.load("body.png").convert_alpha()
        self.body_part = pygame.transform.scale(self.body_part, (25, 25))
       
        # each item of lists will store coordinates of one body part of snake
        self.x_position = [0]
        self.y_position = [0]
        
        self.length = 1
        self.increase_size()        
        
        self.score = 0
        
    def get_head_position(self):
        # position of head of snake
        position_1 = self.head.get_rect()
        self.x_position[0] = position_1.x
        self.y_position[0] = position_1.y
        return (self.x_position[0], self.y_position[0])

    # increasing size of list to potentially have 1000 sections for snake
    # when snake gets bigger, list will have 1,000 items already created to store new body part's coordinates
    def increase_size(self):
        for i in range(0,1000):
            self.x_position.append(-100)
            self.y_position.append(-100)
 
    @staticmethod # part of class def but not part of objects it creates
    def collision(x_1, y_1, x_2, y_2, size_snake, size_food):
        if ((x_1 + size_snake >= x_2) or (x_1 >= x_2)) and x_1 <= x_2 + size_food:
            if ((y_1 >= y_2) or (y_1 + size_snake >= y_2)) and y_1 <= y_2 + size_food:
                return True
            return False

    def move(self):
        # move each body part of body by giving them new coordinates
        # each part of the snake will take positions of the part before it
        # give updated coordinates to entire snake by doing this on entire list
        for i in range(self.length-1, 0, -1):
            self.x_position[i] = self.x_position[i - 1]
            self.y_position[i] = self.y_position[i - 1]

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
        self.food = pygame.image.load("wine.png").convert_alpha()
        self.food = pygame.transform.scale(self.food, (50,50))
        self.position_food = (0, 0)
        self.randomize_position()
    
    def randomize_food(self):
        images = [
            pygame.image.load("wine.png").convert_alpha(),
            pygame.image.load("icecream.png").convert_alpha(),
            pygame.image.load("taco.png").convert_alpha(),
            pygame.image.load("pizza.png").convert_alpha()
        ]
        self.food = images[random.randint(0,len(images) - 1)]
        self.food = pygame.transform.scale(self.food, (50,50))


    def randomize_position(self):
        # give random coordinates
        self.position_food = self.food.get_rect()
        self.position_food.x = random.randint(1,20) * STEP
        self.position_food.y = random.randint(1,20) * STEP

def main(): 
    global PLAYING
    pygame.mixer.init()
    noms = pygame.mixer.Sound("nom.wav")
    death = pygame.mixer.Sound("death2.wav")
    music = pygame.mixer.Sound("80s.wav")
    noms.set_volume(0.8)
    music.set_volume(0.3)
    music.play(-1) # -1 will repeat indefinitely

    # initialize game => will initialize display module
    pygame.init()

    # create single display Surface
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    window_rect = window.get_rect()

    # load background image
    bg = pygame.image.load("background.jpg")

    # blit bg to window
    window.blit(bg, (0, 0))

    # create window caption
    pygame.display.set_caption("Cat's Snake Game")

    # create Snake and food instances
    snake = Snake()
    food = Food()

    # blit head
    window.blit(snake.head, (snake.x_position[0], snake.y_position[0]))

    # blit food
    window.blit(food.food, food.position_food)

    # update contents of entire display
    pygame.display.flip()

    # create continuous loop to keep screen visible
    while (PLAYING == True):
        snake.handle_keys() #invoke keystroke handler
        snake.move() # move snake

        # moving snake in certain direction if user presses key
        if MOVE_UP:
            snake.y_position[0] -= STEP 

        if MOVE_DOWN:
            snake.y_position[0] += STEP

        if MOVE_RIGHT:
            snake.x_position[0] += STEP

        if MOVE_LEFT:
            snake.x_position[0] -= STEP
            
        window.blit(bg, (0,0))
        window.blit(snake.head, (snake.x_position[0], snake.y_position[0]))

        #blit parts of snake on screen using updated coordinates
        for i in range(1, snake.length):
            window.blit(snake.body_part, (snake.x_position[i], snake.y_position[i]))

        # calling the collision function to check if the snake hits the edges of the window
        if snake.x_position[0] < window_rect.left:
            PLAYING = False

        if snake.x_position[0] + 50 > window_rect.right:
            PLAYING = False

        if snake.y_position[0] < window_rect.top:
            PLAYING = False
        
        if snake.y_position[0] + 50 > window_rect.bottom:
            PLAYING = False
        
        # calling the collision function to check if the snake hits itself
        for i in range(snake.length - 1, 0, -1):
            if snake.collision(snake.x_position[0], snake.y_position[0], snake.x_position[i], snake.y_position[i], 0, 0) and (MOVE_INIT == True):
                PLAYING = False
        
        # calling the collision function to check if the snake hits the food
        if snake.collision(snake.x_position[0], snake.y_position[0], food.position_food.x, food.position_food.y,50,25):
    
            # Giving new coordinates to the food when the snake eats it
            food.randomize_position()  

            # change food
            food.randomize_food()
    
            # Giving new coordinates to the food if the ones given above are the same as the snake's ones
            for j in range(0, snake.length):
                while snake.collision(food.position_food.x, food.position_food.y, snake.x_position[j], snake.y_position[j], 50, 25):
                    food.randomize_position()  
            
            # Increasing the size of the snake and the score
            noms.play()
            snake.length += 1
            snake.score += 1
        
        # blit score
        font = pygame.font.SysFont('Arial', 25)
        text = font.render("Score: {0}".format(snake.score), 1, (250, 250, 250))
        window.blit(text, (400, 10))
  
        # blit food
        window.blit(food.food, food.position_food)

        # Flipping to add everything on the board
        pygame.display.flip()

        # Delaying the game to make the snake move fluidly
        time.sleep (SPEED / 1000)

    # when loop is over (i.e. no longer playing), create gameover screen
    # create black screen
    music.stop()
    death.play()
    cover = pygame.Surface(window.get_size())
    cover = cover.convert()
    cover.fill((0, 0, 0))
    window.blit(cover, (0,0))

    # add gameover text + score
    font = pygame.font.SysFont(None, 60)
    text = font.render('GO TO SLEEP!', True, (250,250,250))
    text_score = font.render("Score: {0}".format(snake.score), 1, (250, 250, 250))
    window.blit(text, (100, 200))
    window.blit(text_score, (100, 250))
    
    # update display
    pygame.display.flip()

    #suspend execution for given num of secs
    time.sleep(3) 

main()
