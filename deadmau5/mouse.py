from deadmau5globals import *
import numpy as np
import os
import sys
import pygame
import math
import random
from collections import deque


class Mouse():

    def __init__(self, screen, pos_cm):

        self.screen = screen
        self.pos_cm = pos_cm
        self.angle=math.radians(0)

        # load poop image
        #img_dir = os.path.dirname(os.path.abspath(__file__)) 
        img_dir = "/home/jon/public/mbl-deadmau5/images"
        self.image = pygame.image.load(os.path.join(img_dir, "mouse-emoji.bmp"))
        self.poop_img = pygame.image.load(os.path.join(img_dir, "poop.bmp"))
       
        self.hist_col = 100.0
        self.history = deque(maxlen = 1000)
        self.poops = deque(maxlen = 10)

    def draw(self, pos, screen):
       
        if pos['pos_ok'] and pos['head_ok']: 

            # Extract xy, heading
            world_arena_pos_cm = pos['pos_xy']
            heading_unit_vec = pos['head_xy']
            world_arena_angle = math.atan2(heading_unit_vec[1], heading_unit_vec[0])
            world_arena_angle += math.radians(ANGLE_OFFSET)        

            #world_arena_angle = math.atan2(heading_unit_vec[1], heading_unit_vec[0])

            # Correct position/heading
            mouse_from_arena_cm = tuple(
                -np.subtract(world_arena_pos_cm, self.pos_cm)) # calc pos relative to (rotated) arena
            arena_mouse_pos_cm = rotateVector(mouse_from_arena_cm, world_arena_angle) # and rotate to where it is relative to arena angle

            mouse_px = cm2px(arena_mouse_pos_cm)

            self.history.appendleft(mouse_px)
            col = self.hist_col 

            #rot_mouse = pygame.transform.rotate(self.image, -world_arena_angle * 57)
            #rot_mouse.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)  
            #img_px = (mouse_px[0] - self.image.get_width()/2, mouse_px[1] - self.image.get_height()/2)
            #self.screen.blit(rot_mouse, img_px);

            self.poop(mouse_px)
            for i in range(len(self.poops)):
               self.screen.blit(self.poop_img, self.poops[i])

            if len(self.history) > 1:
                for i in reversed(range(len(self.history)-1)):
                    col = self.hist_col * ((float(self.history.maxlen) - i) / float(self.history.maxlen))
                    pygame.draw.line(self.screen,(col, col, col), self.history[i], self.history[i+1], 2)

            pygame.draw.circle(self.screen, (255,255,255), mouse_px, 9, 2)
            mouse_angle_indicator = tuple(np.subtract(mouse_px, rotateVector((0, 20), world_arena_angle)))
            pygame.draw.line(self.screen,(255,255,255), mouse_px , mouse_angle_indicator, 2)

    def poop(self, poop_pos):
        if random.random() < 0.001
            self.poops.append(poop_pos)
