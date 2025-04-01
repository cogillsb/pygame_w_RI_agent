# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 17:38:42 2023

@author: grace
"""

# game setup
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5

WIDTH, HEIGHT = 800, 800


PLAYER_DAT = {
    "K":[(55,55),(85, HEIGHT + 50)],
    "E":[(55, HEIGHT-85), (85, HEIGHT + 100)],
    "S":[(WIDTH-55, 55), (WIDTH - 230, HEIGHT + 50)],
    "H":[(WIDTH-55, HEIGHT-55), (WIDTH-230, HEIGHT+100)]
    #"O":(WIDTH/2, HEIGHT/2)
    }

AI_MOVES = [[1,0], [-1,0], [0,1], [0,-1], [1,1], [-1,-1], [1,-1], [-1,1]]*2
