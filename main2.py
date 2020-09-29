from pygame.locals import *
from random import randint # lets us give random position to fruits
import time
import pygame

# declaring main var's; main booleans
playing = True
moveUp = moveDown = moveRight = moveLeft = move_init = False

# other int variables
step = 23
score = 0
length = 2
speed = 75

# lists to store coordinates of snake
# each item of lists will store coordinates of one body part of snake
x_snake_position = [0]
y_snake_position = [0]

# increasing size of list to potentially have 1000 sections for snake
# when snake gets bigger, list will have 1,000 items already created to store new body part's coordinates
for i in range(0,1000):
    x_snake_position.append(-100)
    y_snake_position.append(-100)

# function to check if snake hits something like fruits or itself
# enter x and y coordinates of two objects, will return true if they collide
def collision(x_coordinates_1, y_coordinates_1, x_coordinates_2, y_coordinates_2, size_snake, size_fruit):
    if ((x_coordinates_1 + size_snake >= x_coordinates_2) or (x_coordinates_1 >= x_coordinates_2)) and x_coordinates_1 <= x_coordinates_2 + size_fruit:
        if ((y_coordinates_1 >= y_coordinates_2) or (y_coordinates_1 + size_snake >= y_coordinates_2)) and y_coordinates_1 <= y_coordinates_2 + size_fruit:
            return True
        return False

# function to display player's score
def disp_score(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(score), True, (0,0,0))
    window.blit(text, (400,0))

# create board game/ initialize pygame
pygame.init()

# create main window
window = pygame.display.set_mode((500, 500))
window_rect = window.get_rect()
pygame.display.set_caption("Cat's Snake Game")

# blit image on main window
cover = pygame.Surface(window.get_size())
cover = cover.convert()
cover.fill((152, 251, 152)) #fill entire board game with chosen color
window.blit(cover, (0, 0)) # blit allows you to stick something on board game

# refreshing screen to display everything
pygame.display.flip() # flip refreshes screen, must use every time you "blit" something

# loading main images on game window
head = pygame.image.load("head.png").convert_alpha() 
head = pygame.transform.scale(head, (35, 35))

body_part_1 = pygame.image.load("body.png").convert_alpha()
body_part_1 = pygame.transform.scale(body_part_1, (25, 25))

fruit = pygame.image.load("fruit.png").convert_alpha()
fruit = pygame.transform.scale(fruit, (35,35))

# store head and fruit's coordinates in var's
position_1 = head.get_rect() #get_rect allows you to get coordinates of given obj
position_fruit = fruit.get_rect()

# store var's in list variables created before
x_snake_position[0] = position_1.x
y_snake_position[0] = position_1.y

# give random coordinates to first fruit of game
position_fruit.x = randint(2,10)*step
position_fruit.y = randint(2,10)*step

# main loop for game
while (playing == True):
    # collecting all events
    for event in pygame.event.get():

        #checking if user quits game
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            playing = False

        #checking if user presses key
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                if moveUp == False and move_init == True:
                    # if moving down, can't move up
                    if moveDown == True:
                        moveUp == False

                    else:
                        # otherwise, change values to other directions to false
                        # and cchange moveUp to true
                        moveDown = moveRight = moveLeft = False
                        moveUp = move_init = True

            if event.key == pygame.K_DOWN:

                if moveDown == False:
                    # if moving up, can't move down
                    if moveUp == True:
                        moveDown == False
                        
                    else:
                        
                        moveRight = moveLeft = moveUp = False 
                        moveDown = move_init = True

            if event.key == pygame.K_RIGHT:

                if moveRight == False: 
                    # if moving left, can't move right
                    if moveLeft == True:
                        moveRight == False
                        
                    else:
                        # otherwise, moves right; all other directions set to false
                        moveLeft = moveUp = moveDown = False 
                        moveRight = move_init = True

            if event.key == pygame.K_LEFT:
       
                if moveLeft == False:
                    if moveRight == True:
                        moveLeft == False
                        
                    else:
                        
                        moveRight = moveDown = moveUp = False 
                        moveLeft = move_init = True

    #blit head and first part of body
    window.blit(body_part_1, (-5, 5))
    window.blit(head, (0,0))

    # move each body part of body by giving them new coordinates
    # each part of the snake will take positions of the part before it
    # give updated coordinates to entire snake by doing this on entire list
    for i in range(length-1, 0, -1):
        x_snake_position[i] = x_snake_position[(i-1)]
        y_snake_position[i] = y_snake_position[(i-1)]

    # fill window with color to erase diff parts of snake
    cover.fill((152, 251, 152))

    #blit parts of snake on screen using updated coordinates
    for i in range(1, length):
        cover.blit(body_part_1, (x_snake_position[i], y_snake_position[i]))

    # moving snake in certain direction if user presses key
    if moveUp:

        y_snake_position[0] = y_snake_position[0] - step 
        window.blit(cover, (0,0)) 
        window.blit(head, (x_snake_position[0], y_snake_position[0]))

    if moveDown:

        y_snake_position[0] = y_snake_position[0] + step
        window.blit(cover, (0,0))
        window.blit(head, (x_snake_position[0], y_snake_position[0]))

    if moveRight:

        x_snake_position[0] = x_snake_position[0] + step
        window.blit(cover, (0,0))
        window.blit(head, (x_snake_position[0], y_snake_position[0]))

    if moveLeft:

        x_snake_position[0] = x_snake_position[0] - step
        window.blit(cover, (0,0))
        window.blit(head, (x_snake_position[0], y_snake_position[0]))

    # Calling the collision function to check if the snake hits the edges of the window

    if x_snake_position[0] < window_rect.left:

        playing = False

    if x_snake_position[0] + 35 > window_rect.right:

        playing = False

    if y_snake_position[0] < window_rect.top:

        playing = False
    
    if y_snake_position[0] + 35 > window_rect.bottom:

        playing = False
            
    # Calling the collision function to check if the snake hits itself
    if collision(x_snake_position[0], y_snake_position[0], x_snake_position[i], y_snake_position[i],0,0) and (move_init == True):
        
        playing = False

    # Blitting the fruit
    window.blit(fruit, position_fruit)

    # Calling the collision function to check if the snake hits the fruit
    if collision(x_snake_position[0], y_snake_position[0], position_fruit.x, position_fruit.y,35,25):
        
        # Giving new coordinates to the fruit when the snake eats it
        position_fruit.x = randint(1,20)*step   
        position_fruit.y = randint(1,20)*step
    
        # Giving new coordinates to the fruit if the ones given above are the same as the snake's ones
        for j in range(0,length):

            while collision(position_fruit.x, position_fruit.y, x_snake_position[j], y_snake_position[j],35,25):
                position_fruit.x = randint(1,20)*step   
                position_fruit.y = randint(1,20)*step
        
        # Increasing the size of the snake and the score
        length = length + 1
        score = score + 1

    # Displaying the score
    disp_score(score)
    
    # Flipping to add everything on the board
    pygame.display.flip()

    # Delaying the game to make the snake move fluidly
    time.sleep (speed / 1000)

    
# Exiting the game
pygame.quit()
exit()
