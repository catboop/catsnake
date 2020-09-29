import pygame
import random


def main():
    running = True

    # initialize game => will initialize display module
    pygame.init()

    # create single display Surface
    window = pygame.display.set_mode((500, 500))

    # load background image
    bg = pygame.image.load("background.jpg")

    # blit bg to window
    window.blit(bg, (0, 0))

    # create window caption
    pygame.display.set_caption("Cat's Snake Game")

    # update contents of entire display
    pygame.display.flip()
    
    # create continuous loop to keep screen visible
    while (running == True):
        # monitor user inputs (aka events)
        for event in pygame.event.get():
            # if event is type QUIT, close game
            # otherwise, loop will keep going and keep window open
            if event.type == pygame.QUIT:
                running = False

# initialize function
main()