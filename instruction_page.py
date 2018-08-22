import pygame
import sys
from pygame.locals import *

pygame.init()

#background = pygame.image.load("instruction_background.jpg")

def run():
    background = pygame.image.load("instruction_background.jpg")
    screen = pygame.display.set_mode((1000,600))
    screen.blit(background, (0,0))
    pygame.display.set_caption("Instructions")
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # press esc to return home
                if event.key == pygame.K_ESCAPE:
                    import home
                    home.run()
            
            pygame.display.update()
    
