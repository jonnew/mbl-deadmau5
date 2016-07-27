from deadmau5globals import *
from mouse import Mouse
import numpy as np
import os
import sys
import pygame
import math

class Maze():

    def __init__(self, screen, arena_rad_cm, site_rad_cm):

        self.screen = screen

        self.arena_rad_cm = arena_rad_cm
        self.site_rad_cm = site_rad_cm

        home_pos_angle=math.radians(globalAngleOffset(120))

        left_pos_angle=math.radians(globalAngleOffset(-30))
        right_pos_angle=math.radians(globalAngleOffset(-90))

        wall_angle = math.radians(globalAngleOffset(300))

        self.mice = []

        self.site_rad_pos_cm = arena_rad_cm 
        self.home_pos = [ math.cos(float(home_pos_angle))*self.site_rad_pos_cm, math.sin(float(home_pos_angle))*self.site_rad_pos_cm ]
        self.left_pos = [ math.cos(float(left_pos_angle))*self.site_rad_pos_cm, math.sin(float(left_pos_angle))*self.site_rad_pos_cm ]
        self.right_pos= [ math.cos(float(right_pos_angle))*self.site_rad_pos_cm, math.sin(float(right_pos_angle))*self.site_rad_pos_cm ]
        self.wall_pos = [ math.cos(float(wall_angle))*self.site_rad_pos_cm, math.sin(float(wall_angle))*self.site_rad_pos_cm ]

    def draw(self, pos):

        # Extract xy, heading
        if pos['pos_ok'] and pos['head_ok']:

            world_arena_pos_cm = pos['pos_xy']
            heading_unit_vec = pos['head_xy']

            # Arena
            pygame.draw.circle(self.screen, (10,10,200), cm2px((0,0)), CM2PX * self.arena_rad_cm, 3)

            # Wall
            pygame.draw.line(self.screen, (10,10,200), cm2px((0,0)), cm2px(self.wall_pos), 3)

            # Reward and home site
            pygame.draw.circle(self.screen, (200,200,200), cm2px(self.home_pos), CM2PX * self.site_rad_cm, 2)
            label = FONT.render("Home", 1, (255,255,0))
            self.screen.blit(label, cm2px(self.home_pos))

            pygame.draw.circle(self.screen, (0,200,0), cm2px(self.left_pos), CM2PX * self.site_rad_cm, 2)
            label = FONT.render("L", 1, (255,255,0))
            self.screen.blit(label, cm2px(self.left_pos))

            pygame.draw.circle(self.screen, (200,0,0), cm2px(self.right_pos), CM2PX * self.site_rad_cm, 2)
            label = FONT.render("R", 1, (255,255,0))
            self.screen.blit(label, cm2px(self.right_pos)) 

            # Print sample info
            time_idx =  "Index : " + str(pos['tick'] )
            label = FONT.render(time_idx, 1, (255,255,0))
            self.screen.blit(label, (10, SCREEN_PX_Y - 120))

            time_sec =  "Time (s): " + "%.2f" % (pos['usec'] / 1.0e6)
            label = FONT.render(time_sec, 1, (255,255,0))
            self.screen.blit(label, (10, SCREEN_PX_Y - 80))
            
            x = "%.2f" % pos['pos_xy'][0] 
            y = "%.2f" % pos['pos_xy'][1]
            pos_lab =  "Pos. (cm) [" + x + ", " + y + "]"
            label = FONT.render(pos_lab, 1, (255,255,0))
            self.screen.blit(label, (10, SCREEN_PX_Y - 40))
            

        for m in self.mice:
            m.draw(pos, self.screen)
            
    def addMouse(self, mouse):
        self.mice.append(mouse)
