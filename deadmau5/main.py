#!/usr/bin/python

'''
Deadmau5 to kill some mice

'''

from tracker import Tracker
from maze import Maze
import math
import signal
import zmq


def main():

    # Install exit routine
    def signal_handler(signal, frame):
        print('Exiting')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # Tracker
    ctx = zmq.Context()
    tracker = Tracker()
    tracker.connect(ctx, 'tcp://localhost:5555')
    
    # Maze
    maze = Maze((8,8))

    while True:

        # Get latest position
        pos = tracker.get_position()

        # Update display
        maze.draw(pos)

if __name__ == '__main__':
    main()
