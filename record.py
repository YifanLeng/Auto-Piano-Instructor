# reference: http://comments.gmane.org/gmane.comp.python.pygame/21856
import pygame
import sys
import pygame.midi
import write_file
from pygame.locals import *

pygame.init()
pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
i = pygame.midi.Input( input_id )
startTime = int(pygame.midi.time())

timePoints = []
notes = []
class Struct: pass
data = Struct()
data.counter = 0
data.information = []

going = True

def getInput():
        return i

def run():
        pygame.init()
        pygame.midi.init()
        print "starting"
        pygame.display.set_caption("midi test")
        screen = pygame.display.set_mode((400, 300), RESIZABLE, 32)
        ##########################################################
        # Yifan Leng wrote the follwing part
        while True:             
                if i.poll():
                    midi_events = i.read(10)
                    if midi_events[0][0][2] != 0:
                        timePoints.append(int(pygame.midi.time())-startTime)
                        notes.append(int(midi_events[0][0][1]))
                        # convert them into pygame events.
                    if midi_events[0][0][2] == 0:
                        # append the length of the note
                        timePoints.append(int(pygame.midi.time())-startTime)
                        noteLength = timePoints[-1]-timePoints[-2]
                        # append the note value
                        note = notes[-1]
                        info = [timePoints[-2], noteLength, note]
                        data.information.append(info)

                for event in pygame.event.get():
                        if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                        elif event.type == pygame.KEYDOWN:
                                # press esc to return home
                                if event.key == pygame.K_ESCAPE:
                                    import home
                                    home.run()
                                else:
                                    # write a text file to store information
                                    content = str(data.information)
                                    write_file.writeFile("my_play.txt", content)
                                    if write_file.writeFile("my_play.txt", content):
                                        print "done recording"
        #################################################################

        print "exit button clicked."
        i.close()
