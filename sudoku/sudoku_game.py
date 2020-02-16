# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 00:15:57 2020

@author: Logan Rowe
"""

import pygame
import numpy as np
import os
import glob
import matplotlib.pyplot as plt

pygame.init()

# =============================================================================
# IMPORT SOUND AND GRAPHICS
# =============================================================================
bg=pygame.image.load('./graphics/sudoku_board.png')
tile_images=[pygame.image.load('./graphics/'+str(i)+'.jpg') for i in range(1,10)]

oops_1=pygame.mixer.Sound('./sound-effects/ouch_1.wav')
oops_2=pygame.mixer.Sound('./sound-effects/ouch_2.wav')
pew=pygame.mixer.Sound('./sound-effects/laser_pew.wav')

music=pygame.mixer.music.load('./sound-effects/music.mp3')
pygame.mixer.music.play(-1)

# =============================================================================
# SET INITIAL CONDITIONS AND CONSTRAINTS
# =============================================================================
#Screen Size
win=pygame.display.set_mode(bg.get_size())

clock=pygame.time.Clock()

#track the times a tile was misplayed
errors=0

#title
pygame.display.set_caption('Pseudo Koo')

# =============================================================================
# TILES FOR THE BOARD
# =============================================================================

class tile(object):
    def __init__(self,x,y,width,height,value):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.value=value
        
    def draw(self):
        win.blit(tile_images[self.value-1],(self.x,self.y))
        
        font1=pygame.font.SysFont('comicsans',30)
        text=font1.render(str(self.value),1,(255,255,255))
        win.blit(text,(int(self.x+self.width/2-text.get_size()[0]/2),int(self.y+self.height/2-text.get_size()[1]/2)))



# =============================================================================
# REDRAW GAME WINDOW     
# =============================================================================
border_thickness=0.017*bg.get_size()[0]
board_size=int(bg.get_size()[0]-2*border_thickness)
line_spacing=int(board_size/9)

def redrawGameWindow():
    
    #add background    
    win.blit(bg, (0,0))
    
    #Add lines for sudoku blocks
    for x in range(1,9):
        pygame.draw.line(win,(255,255,255),(border_thickness+x*line_spacing,border_thickness),(border_thickness+x*line_spacing,border_thickness+board_size))
    for y in range(1,9):
        pygame.draw.line(win,(255,255,255),(border_thickness,border_thickness+y*line_spacing),(border_thickness+board_size,border_thickness+y*line_spacing))
    
    #Add thick lines for boxes
    for x in range(1,3):
        pygame.draw.line(win,(255,255,255),(border_thickness+3*x*line_spacing,border_thickness),(border_thickness+3*x*line_spacing,border_thickness+board_size),10)
    for y in range(1,3):
        pygame.draw.line(win,(255,255,255),(border_thickness,border_thickness+3*y*line_spacing),(border_thickness+board_size,border_thickness+3*y*line_spacing),10)

    for num in numbers:
        num.draw(win)
        
    pygame.display.update()



# =============================================================================
# MAIN LOOP
# =============================================================================
numbers=[] #populate numbers with the initially given values

#Text for screen (bold and italiscized)
font = pygame.font.SysFont('comicsans', 30,True)

run = True
while run:
    #slow the game so it only blits every 100/1000 seconds
    pygame.time.delay(50)
    
    #get list of all events that happen i.e. keyboard, mouse, ...
    for event in pygame.event.get():
        #Check if the red X was clicked
        if event.type==pygame.QUIT:
            run=False
    

    #Move character
    keys=pygame.key.get_pressed()
    mouse=pygame.mouse
    
    #TRACK MOUSE CLICKS
    if mouse.get_pressed()[0]:
        print(mouse.get_pos())
    '''
    #MOVING LEFT AND RIGHT
    man.standing=True
    if keys[pygame.K_LEFT]:
        man.standing=False
        man.x-=man.vel
        man.left,man.right=True,False
        if man.x<0:
            man.x=0
    if keys[pygame.K_RIGHT]:
        man.standing=False
        man.x+=man.vel
        man.right,man.left=True,False
        if man.x+man.width>win.get_size()[0]:
            man.x=win.get_size()[0]-man.width
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        #character is standing still
        man.left=man.right=False
    '''
    
    redrawGameWindow()





pygame.quit()