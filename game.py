import pygame
import sys
import pygame.midi
import time
import visualize_the_record
import record
import scores
from pygame.locals import *

# store the list to store the instances
all_whitekeys = []
all_blackkeys = []
fallingPieces = []
# set up colors
black = (0,0,0)
red = (255, 0 ,0)
orange = (255, 201, 14)
grey = (112, 112, 112)
# use Struct to store variables used across functions
class Struct: pass
data = Struct()
data.counter = 0
data.notes = []
data.collision = 0
data.fallingNote = None
data.score = 0
data.fallingPieces = []
data.FPS = 30
# use set to avoid make the note on twice
collisionSet = set()
# init modules
pygame.init()
pygame.midi.init()
# get the input event
i = record.getInput()
# get the output event
port = pygame.midi.get_default_output_id()
data.midi_out = visualize_the_record.getmidi()
# use clock to adjust speed
clock = pygame.time.Clock()
#screen size
screenHeight = 685
screenWidth = 1000
# values of notes
whiteNotes = [36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60,62,
              64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83]
blackNotes = [37, 39, 42, 44, 46, 49, 51, 54, 56, 58, 61, 63, 66, 68, 70, 73,
              75, 78, 80, 82]
# set up font
font = pygame.font.SysFont(None, 48)

def noteToImgx(note):
    # get the top left x of a key given its note
    keys = all_whitekeys + all_blackkeys
    for key in keys:
        if key.note == note:
            return key.startX
    
def generateNotes(information,screen):
    data.fallingPieces = []
    # make fallingPiece instances
    for info in information:
        # set fallingPieces based on the information given by the midi keyboard
        timePoint = info[0]
        noteLength = info[1]
        note = info[2]
        height = noteLength
        imgx = noteToImgx(note)
        # lessen the waiting time
        offset = 1600
        distance = timePoint - offset
        # width for white and black keys
        if note in whiteNotes:
            width = 30
        else:
            width = 20
        fallingPiece = FallingPieces(note, height,width,
                                     imgx, 20, distance,screen)
        data.fallingPieces.append(fallingPiece)

# load image
def load_image(name):
    image = pygame.image.load(name)
    return image, image.get_rect()

class FallingPieces(object):
    counter = 0
    def __init__(self, note, height, width,imgx, speed, distance,screen):
        # initialize all the data
        self.speed = speed
        self.height = height
        self.width = width
        self.imgy = screenHeight-distance-height
        self.imgx = imgx
        self.distance = distance
        self.note = note
        self.Grand_piano = 0
        self.instrument = self.Grand_piano
        FallingPieces.counter += 1
        # set every fallingPiece an index to hash
        self.index = FallingPieces.counter
        self.screen = screen

    def draw(self):
        # draw the fallingPieces
        pygame.draw.rect(self.screen, orange,
                         (self.imgx, self.imgy,self.width, self.height))

    def move(self):
        # cover the previous fallingPiece
        pygame.draw.rect(self.screen, black,
                         (self.imgx, self.imgy,self.width, self.height))
        # move the fallingPiece
        self.imgy += self.speed
        
    def sound(self):
        try:
            if data.collision == 1:
                # set an input instance
                data.midi_out.set_instrument(self.instrument)
                data.midi_out.note_on(self.note, 127)
        except:
            print "error when playing note"

    def __hash__(self):
        # hash based on every fallingPiece's unique index
        hashable = self.index
        return hash(hashable)



class Keyboard(pygame.sprite.Sprite):
    counter = -1
    #initialize the starting point of the keyboard
    def __init__(self, startX, startY,name,note,chosenTimes):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(name)
        self.rect.topleft = (startX, startY)
        Keyboard.counter += 1
        self.index = Keyboard.counter
        self.startX = startX
        self.note = note
        self.chosenTimes = chosenTimes
                
    def Index(self):
        return self.index


def makeWhiteKeys():
    #generate white key instances
    numkeys = 28
    startX = 60
    startY = 500
    width = 30
    for i in xrange (numkeys):
        tpX = startX + i*width
        key = Keyboard(tpX, startY, "white_key.png", whiteNotes[i],0)
        all_whitekeys.append(key)

def makeBlackKeys():
    #generate black key instances
    noteIndex = -1
    startY = 500
    startX = 60
    interval = 7
    whiteWidth = 30
    blackWidth = 20
    blacks = [1,2,4,5,6]
    for i in xrange (0, 4*interval, interval):
        for j in blacks:
            j = j+i
            noteIndex += 1
            centerX = startX + j*whiteWidth
            tpX = centerX - blackWidth/2
            key = Keyboard(tpX, startY, "black_key.png", blackNotes[noteIndex],0)
            all_blackkeys.append(key)


def drawKeys(screen):
    # draw the keyboard on the screen
    for whiteKey in all_whitekeys:
        screen.blit(whiteKey.image, whiteKey.rect.topleft)
    for blackKey in all_blackkeys:
        screen.blit(blackKey.image, blackKey.rect.topleft)


def makePieceFall(screen, all_keys, fallingPieces):
    keyHeight = 175
    for fallingPiece in fallingPieces:
        # pieces fall until leave the screen
        if fallingPiece.imgy <= screenHeight+20:
            fallingPiece.move()
            fallingPiece.draw()
            # if fallingPiece hits the key
            if fallingPiece.imgy >= screenHeight-keyHeight-fallingPiece.height-20:
                data.fallingNote = fallingPiece.note
            if fallingPiece.imgy >= screenHeight-keyHeight-fallingPiece.height:
                # the collision set checks if new fallingpiece hits the key
                # to avoid call note_on multiple times
                num = len(collisionSet)
                collisionSet.add(fallingPiece)
                if len(collisionSet) != num:
                    data.collision = 0
                data.collision += 1
                # make the sound
                fallingPiece.sound()
                for key in all_keys: #@ change it later
                    if key.note == fallingPiece.note:
                        # change the color of the white key
                        if key.note in whiteNotes:
                            key.image = pygame.image.load("orange_key.png")
                        else:
                            key.image = pygame.image.load("orange_small_key.png")
                        if fallingPiece.imgy >= screenHeight:
                            # if fallingpiece leaves the key
                            # change back the color
                            data.midi_out.note_off(fallingPiece.note, 127)
                            #fallingPieces.remove(fallingPiece)
                            if key.note in whiteNotes:
                                key.image = pygame.image.load("white_key.png")
                            else:
                                key.image = pygame.image.load("black_key.png")
    drawKeys(screen)

def drawFast(screen):
    # draw fast-speed icon
    fastIcon = pygame.image.load("fastIcon.png")
    screen.blit(fastIcon, (150, 20))
    # get the rect of the icon
    data.fastRect = fastIcon.get_rect()
    data.fastRect.topleft = (150,20)

def drawSlow(screen):
    # draw slow-speed icon
    slowIcon = pygame.image.load("slowIcon.png")
    screen.blit(slowIcon, (20, 20))
    # get the rect of the icon
    data.slowRect = slowIcon.get_rect()
    data.slowRect.topleft = (20, 20)

def run(song):
    # set up the screen
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Game")
    makeWhiteKeys()
    makeBlackKeys()
    # set up fallingPieces
    generateNotes(song,screen)
    all_keys = all_whitekeys + all_blackkeys
    while True:
        makePieceFall(screen, all_keys, data.fallingPieces)
        drawFast(screen)
        drawSlow(screen)
        drawKeys(screen)
        clock.tick(data.FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # press esc to return home
                if event.key == pygame.K_ESCAPE:
                    import home
                    home.run()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if data.fastRect.collidepoint(pos):
                    # fast FPS is 120
                    data.FPS = 120
                elif data.slowRect.collidepoint(pos):
                    # set slow FPS to 10
                    data.FPS = 10
        if i.poll():
            midi_events = i.read(10)
            note = midi_events[0][0][1]
            noteStatus = midi_events[0][0][2]
            #midi_events[0][0][2] is zero when the key is realeased
            for key in all_keys:
                if key.note == note:
                    if noteStatus != 0:
                        if key.note == data.fallingNote:
                            # score increases as user hits the right key
                            data.score += 1
                            # switch key images
                            if key.note in whiteNotes:
                                key.image = pygame.image.load("orange_key.png")
                            else:
                                key.image = pygame.image.load("orange_small_key.png")
                        # red the keys if user hits the wrong key
                        else:
                            if key.note in blackNotes:
                                key.image = pygame.image.load("red_key.png")
                            else:
                                key.image = pygame.image.load("red_big_key.png")
                    # switch back the original keys
                    else:
                        for key in all_keys:
                            if key.note in whiteNotes:
                                key.image = pygame.image.load("white_key.png")
                            else:
                                key.image = pygame.image.load("black_key.png")
            # render scores on the screen
            text = font.render(str(data.score), True, red, black)
            textrect = text.get_rect()
            textrect.centerx, textrect.centery = 20, 100
            screen.blit(text, textrect)
        pygame.display.update()
    
