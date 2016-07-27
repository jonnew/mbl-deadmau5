#!/usr/bin/python

'''
Deadmau5 to train some mice

'''

from .deadmau5globals import *
from .recorder import Recorder
from .tracker import Tracker
from .maze import Maze
from .mouse import Mouse
#import vidcap #Records pygame to video
import math
import pygame
import signal
import sys
import zmq

def main():

    # Install exit routine
    def signal_handler(signal, frame):
        #recorder.close_file()
        print('Exiting')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # Recorder
    #recorder = Recorder('/home/jon/Desktop/20160725/mouse-4/','maze')

    # Tracker
    ctx = zmq.Context()
    tracker = Tracker()
    tracker.connect(ctx, 'tcp://localhost:5555')
    
    # Maze and mouse
    maze = Maze(SCREEN, 10, 3)
    mouse = Mouse(SCREEN, (9.5, 9.5))
    maze.addMouse(mouse)

    while True:

        # Get latest position
        pos = tracker.get_position()

        # Catch pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()

        # Update display
        SCREEN.fill(BGCOLOR)
        maze.draw(pos)
        pygame.display.flip()
        pygame.display.update()

        # Record maze state
        #maze.record()

if __name__ == '__main__':
    main()
