# reference: lagusan.com/button-drawer-python-2-6/
import pygame, Buttons
import sys
import pygame.midi
import time
from pygame.locals import *

pygame.init()
pygame.midi.init()

grey = (112, 112, 112)
black = (0,0,0)

screenHeight = 600
screenWidth = 1000
background = pygame.image.load("home_background.jpg")

class selectButtons:
    def __init__(self, buttonColor,x,y,length,
                 height, textColor,text,text2,text3,text4, text5):
        self.color = buttonColor
        self.x = x
        self.y = y
        self.width = length
        self.height = height
        self.text = text
        self.text2 = text2
        self.text3 = text3
        self.text4 = text4
        self.text5 = text5
        self.textColor = textColor
        self.main()
        
    def display(self):
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption("home")

    def update_display(self):
        self.screen.blit(background, (0,0))
        self.Button1.create_button(self.screen, self.color,self.x, self.y,
                                    self.width, self.height, 0,
                                   self.text, self.textColor)
        self.Button2.create_button(self.screen, self.color,self.x,self.y+100,
                                   self.width, self.height,0,
                                   self.text2, self.textColor)
        self.Button3.create_button(self.screen, self.color,self.x,self.y+200,
                                   self.width, self.height,0,
                                   self.text3, self.textColor)
        self.Button4.create_button(self.screen, self.color,self.x,self.y+300,
                                   self.width, self.height,0,
                                   self.text4, self.textColor)
        self.Button5.create_button(self.screen, self.color,self.x,self.y+400,
                                   self.width, self.height,0,
                                   self.text5, self.textColor)
    
        pygame.display.flip()

    def main(self):
        self.Button1 = Buttons.Button()
        self.Button2 = Buttons.Button()
        self.Button3 = Buttons.Button()
        self.Button4 = Buttons.Button()
        self.Button5 = Buttons.Button()
        self.display()
        ###############################################################
        # Yifan Leng wrote the following part
        while True:
            self.update_display()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        import tp_staff
                        tp_staff.run()
                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        import record
                        record.run()
                    elif self.Button3.pressed(pygame.mouse.get_pos()):
                        import visualize_the_record
                        visualize_the_record.run()
                    elif self.Button4.pressed(pygame.mouse.get_pos()):
                        import game
                        import choose_music
                        song = choose_music.run()
                        game.run(song)
                    elif self.Button5.pressed(pygame.mouse.get_pos()):
                        import instruction_page
                        instruction_page.run()
        ################################################################


def run():
    obj = selectButtons(grey, 333,50, 333, 50, black,
                        "learn to recognize staff","record your playing",
                        "visualize the record",
                        "start playing music pieces", "instructions")
                





















                    

    
