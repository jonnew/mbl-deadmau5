import math
import pygame

# Global constants
CM2PX = 15
SCREEN_PX_X= 500
SCREEN_PX_Y= 600
OFFSET = min(SCREEN_PX_X, SCREEN_PX_Y) / 2
ANGLE_OFFSET = 150
BGCOLOR = 0, 0, 0

# Initialize pygame
SCREEN = pygame.display.set_mode((SCREEN_PX_X, SCREEN_PX_Y), pygame.RESIZABLE)
pygame.init()
pygame.font.init()

# Must be done after pygame.init()
FONT = pygame.font.SysFont("monospace", 30)

def globalAngleOffset(theta):
    return theta + ANGLE_OFFSET

def rotateVector(v, theta):
    return (v[0]*math.cos(theta)-v[1]*math.sin(theta),
            v[0]*math.sin(theta)+v[1]*math.cos(theta))

def cm2px(pos_cm):
    pos_x = int(round(pos_cm[0] * CM2PX + OFFSET))
    pos_y= int(round(pos_cm[1] * CM2PX + OFFSET))
    return (pos_x, pos_y)
