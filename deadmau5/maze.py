import numpy as np
import os
import sys
import pygame
import math

CM2PX = 25 
OFFSET = 300 

class Maze():

    def __init__(self, mouse_pos_cm):

        # pygame stuff
        width = 1000
        height = 1000
        self.bgcolor = 0, 0, 0

        self.screen = pygame.display.set_mode((width, height))
        pygame.init()

        self.world_mouse_pos_cm = mouse_pos_cm
        self.world_mouse_angle=math.radians(0)

        self.arena_diam_cm = 20

        home_pos_angle=math.radians(120)
        self.home_diam_cm = 3

        left_pos_angle=math.radians(0)
        self.left_diam_cm = 3

        right_pos_angle=math.radians(-120)
        self.right_diam_cm = 3

        self.home_pos = [ math.cos(float(home_pos_angle))*self.arena_diam_cm/2, math.sin(float(home_pos_angle))*self.arena_diam_cm/2 ]
        self.left_pos = [ math.cos(float(left_pos_angle))*self.arena_diam_cm/2, math.sin(float(left_pos_angle))*self.arena_diam_cm/2 ]
        self.right_pos= [ math.cos(float(right_pos_angle))*self.arena_diam_cm/2, math.sin(float(right_pos_angle))*self.arena_diam_cm/2 ]

        # load poop image
        #img_dir = os.path.dirname(os.path.abspath(__file__)) 
        img_dir = "/home/jon/public/mbl-deadmau5/images"
        self.poop_image = pygame.image.load(os.path.join(img_dir, "deadmau5.bmp"))

    def draw(self, pos):

        # Clear the screen
        self.screen.fill((self.bgcolor))

        # Extract xy, heading
        world_arena_pos_cm = pos['pos_xy']
        heading_unit_vec = pos['head_xy']
        world_arena_angle = math.atan2(heading_unit_vec[1], heading_unit_vec[0])
    
        # Catch pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # Correct position/heading
        mouse_from_arena_cm = tuple(
            -np.subtract(world_arena_pos_cm, self.world_mouse_pos_cm)) # calc pos relative to (rotated) arena
        arena_mouse_pos_cm = rotateVector(mouse_from_arena_cm, world_arena_angle) # and rotate to where it is relative to arena angle

	# draw stuff
	self.screen.blit(self.poop_image, (0,0));

        pygame.draw.circle(self.screen, (10,10,200), cm2px((0,0)), CM2PX * self.arena_diam_cm/2, 3)
        pygame.draw.circle(self.screen, (200,200,200), cm2px(self.home_pos), CM2PX * self.home_diam_cm, 2)
        pygame.draw.circle(self.screen, (0,200,0), cm2px(self.left_pos), CM2PX * self.left_diam_cm, 2)
        pygame.draw.circle(self.screen, (200,0,0), cm2px(self.right_pos), CM2PX * self.right_diam_cm, 2)

        pygame.draw.circle(self.screen, (255,255,255), cm2px(arena_mouse_pos_cm), 9, 2)
        mouse_angle_indicator = tuple(np.subtract(cm2px(arena_mouse_pos_cm), rotateVector((0,20), world_arena_angle)))
        pygame.draw.line(self.screen,(255,255,255), cm2px(arena_mouse_pos_cm), mouse_angle_indicator, 2)
            
        pygame.display.flip()
        pygame.display.update()

def rotateVector(v, theta):
    return ( v[0]*math.cos(theta)-v[1]*math.sin(theta) , v[0]*math.sin(theta)+v[1]*math.cos(theta)) 

def cm2px(pos_cm):
    
    pos_x = int(round(pos_cm[0] * CM2PX + OFFSET))
    pos_y= int(round(pos_cm[1] * CM2PX + OFFSET))
    return (pos_x, pos_y)
