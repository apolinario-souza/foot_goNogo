#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 16:28:54 2025

@author: tercio
"""

import pygame
#pygame.init()
#Configuration trials
SUJ = 11
N_TRIALS = 30
PROB_6 = 0.15 
INTERSTIMULUS = 600
INTERSTIMULUS_6 = 2000
CAMERA = 0

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT  = screen.get_size()

#Colors
BLACK = (0, 0, 0)