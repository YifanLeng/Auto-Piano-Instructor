import pygame
import sys
import time
import pygame.midi
import visualize_the_record
from pygame.locals import *

# initialize modules
pygame.init()
pygame.midi.init()
# get the output event
port = pygame.midi.get_default_output_id()
midi_out = visualize_the_record.getmidi()
# set up colors
white = (255, 255, 255)
black = (0,0,0)
blue = (53, 148, 242)
grey = (112, 112, 112)
# use sprite group to store key instances
all_notes = pygame.sprite.Group()
all_whitekeys = pygame.sprite.Group()
all_blackkeys = pygame.sprite.Group()
notes = [48, 50, 52, 53, 55, 57, 59,60, 62, 64, 65, 67, 69, 71, 72]
class Struct: pass
data = Struct()

# load image
def load_image(name):
    image = pygame.image.load(name)
    return image, image.get_rect()

class Notes(pygame.sprite.Sprite):
    counter = -1
    # initialize position and image
    def __init__(self, centerX, centerY, name):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(name)
        self.centerX, self.centerY = centerX, centerY
        self.rect.center = (centerX, centerY)
        # set every note an index to identify
        Notes.counter += 1
        self.index = Notes.counter

    def Index(self):
        return self.index
         
class Staff(pygame.sprite.Sprite):
    # initialize start and end points
    def __init__(self, startX, startY, endX, endY,screen):
        self.startX, self.startY = startX, startY
        self.endX, self.endY = endX, endY
        self.screen = screen
        
    def drawLine(self):
        # draw lines of the staff
        numLines = 5
        space = 25
        for i in xrange (numLines):
            startX = self.startX
            startY = self.startY + i*space
            endX = self.endX
            endY = self.endY + i*space
            pygame.draw.line(self.screen, black,[startX,startY],[endX,endY],2)
       
class Keyboard(pygame.sprite.Sprite):
    counter = -1
    #initialize the starting point of the keyboard
    def __init__(self, startX, startY,name):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(name)
        self.rect.topleft = (startX, startY)
        Keyboard.counter += 1
        # set every key an index to relate to the note
        self.index = Keyboard.counter

    def Index(self):
        return self.index  

def placeNotes():
    # place notes on the staff
    numNotes = 15
    for i in xrange (numNotes):
        startX = 20
        startY = 220
        space = 60
        length = 960
        width = (length - space)/numNotes
        height = 25
        centerX = startX+space+width/2+i*width
        centerY = startY - i*height/2
        # put all the notes into a list
        note = Notes(centerX, centerY, "note.png")
        all_notes.add(note)

def makeStaff(screen):
    # draw the empty staff
    highStaff = Staff(20, 6, 980, 6,screen)
    highStaff.drawLine()
    lowStaff = Staff(20, 158, 980, 158,screen)
    lowStaff.drawLine()
    
def makeWhiteKeys():
    # set instances of whitekeys
    numkeys = 28
    startX = 60
    startY = 500
    width = 30
    for i in xrange (numkeys):
        tpX = startX + i*width
        key = Keyboard(tpX, startY, "white_key.png")
        all_whitekeys.add(key)
    
def makeBlackKeys():
    # set instances of blackkeys
    startY = 500
    startX = 60
    interval = 7
    whiteWidth = 30
    blackWidth = 20
    blacks = [1,2,4,5,6]
    # magic number!
    for i in xrange (0, 28, interval):
        for j in blacks:
            j = j+i
            centerX = startX + j*whiteWidth
            tpX = centerX - blackWidth/2
            key = Keyboard(tpX, startY, "black_key.png")
            all_blackkeys.add(key)

def drawReset(screen):
    # draw reset icon
    icon = pygame.image.load("icon_reset.png")
    screen.blit(icon, (20, 300))
    data.resetrect = icon.get_rect()
    data.resetrect.topleft = (20, 300)

def drawNames(screen):
    noteNames = pygame.image.load("noteNames.png")
    screen.blit(noteNames, (46, 450))

def reset():
    # reset all notes and keys to original images
    for note in all_notes:
        note.image = pygame.image.load("note.png")
    for whitekey in all_whitekeys:
        whitekey.image = pygame.image.load("white_key.png")
    for blackkey in all_blackkeys:
        blackkey.image = pygame.image.load("black_key.png")
    
def run():
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Staff")
    screen.fill(blue)
    placeNotes()
    makeStaff(screen)
    makeWhiteKeys()
    makeBlackKeys()
    drawReset(screen)
    drawNames(screen)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # press esc to return to the home page
                if event.key == pygame.K_ESCAPE:
                    import home
                    home.run()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                interval = 7
                if data.resetrect.collidepoint(pos):
                    reset()
                for note in all_notes:
                    if note.rect.collidepoint(pos):
                        index = note.Index()
                        # change image of selected notes
                        note.image = pygame.image.load("orange_note.png")
                        for whitekey in all_whitekeys:
                            if whitekey.Index() == index + interval:
                                # change key images
                                whitekey.image = pygame.image.load("orange_key.png")
                                # use output event to make sound of the note
                                midi_out.set_instrument(0)
                                midi_out.note_on(notes[index], 127)
                                time.sleep(0.5)
                                midi_out.note_off(notes[index], 127)        
        # draw all the notes
        all_notes.draw(screen)
        all_whitekeys.draw(screen)
        all_blackkeys.draw(screen)
        pygame.display.update()
            

