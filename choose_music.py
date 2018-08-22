import pygame
import sys
import game
import scores
from pygame.locals import *

screenHeight = 600
screenWidth = 1000

class Struct: pass
data = Struct()
data.choice = None

pygame.init()

grey = (40,40,40)
white = (255,255,255)
black = (0,0,0)
blue = (0, 0, 255)
font = pygame.font.SysFont('segoeprint', 30)

class dropDowns(object):
    def __init__(self,song1, song2, color,textColor,
                 x, y, length, height,screen ):
        self.song1 = song1
        self.song2 = song2
        self.color = color
        self.textColor = textColor
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.screen = screen
        self.rect = (self.x, self.x+self.length, self.y, self.y+self.height)
        self.text1 = font.render(self.song1, True, self.textColor, self.color)
        self.text2 = font.render(self.song2, True, self.textColor, self.color)
        self.text1rect = self.text1.get_rect()
        self.text2rect = self.text2.get_rect()
        space = 50
        (self.text1rect.centerx,self.text1rect.centery) = (self.x+self.length/2.0,
                                                 self.y+self.height+space/2.0)
        (self.text2rect.centerx,self.text2rect.centery) = (self.x+self.length/2.0,
                                                self.y+self.height+space+space/2.0) 
    

        
    def drawChoices(self):
        space = 50
        self.screen.blit(self.text1, self.text1rect)
        self.screen.blit(self.text2, self.text2rect)


            
                  
musicPieces =  scores.returnMusic()
def run():
    while True:
        screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption("music choices")
        background = pygame.image.load("choose_music_background.jpg")
        screen.blit(background,(0,0))
        mode1 = dropDowns("castle in the sky","My heart will go on",
                  white,black,20, 100, 300, 100, screen)
        mode2 = dropDowns("A comme Amour", "Totoro",
                  grey,black, 350, 100, 300, 100,screen)
        mode3 = dropDowns("Canon in D","Mariage D'Amou",
                  black,white, 650, 100, 300, 100,screen)
        for mode in [mode1, mode2, mode3]:
            mode.drawChoices()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for mode in [mode1, mode2, mode3]:
                    index = -1
                    for rect in [mode.text1rect, mode.text2rect]:
                        index += 1
                        if rect.collidepoint(pos):
                            if index == 0:
                                 return musicPieces[mode.song1]
                            else:
                                 return musicPieces[mode.song2]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    import home
                    home.run()
                           
        pygame.display.update()



















                         
    
