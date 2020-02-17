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
import matplotlib.image as mpimg
from itertools import product
import time


pygame.init()

# =============================================================================
# LOAD SOUND AND GRAPHICS
# =============================================================================
#board and tiles
bg_board=pygame.image.load('./graphics/sudoku_board.png')
tile_images=[pygame.image.load('./graphics/'+str(i)+'.jpg') for i in range(1,10)]

#screen background
bg_screen=pygame.image.load('./graphics/other/light_wood.jpg')

#screen title and submenu
screen_title=pygame.image.load('./graphics/title.jpg')
screen_submenu=pygame.image.load('./graphics/menu_box.jpg')

#sound effects iconcs
sound_effects_icon=pygame.image.load('./graphics/sound_effects_icon.png')
music_icon=pygame.image.load('./graphics/music_icon.png')

#Sound effects
sound_effects_playing=True
oops_1=pygame.mixer.Sound('./sound-effects/ouch_1.wav')
oops_2=pygame.mixer.Sound('./sound-effects/ouch_2.wav')
pew=pygame.mixer.Sound('./sound-effects/laser_pew.wav')

music_playing=True
music=pygame.mixer.music.load('./sound-effects/music.mp3')
pygame.mixer.music.play(-1)

#Logo
logo=pygame.image.load('./graphics/simple-logo.png')
pygame.display.set_icon(logo)

#pen, pencil, and back icons
pencil_icon=pygame.image.load('./graphics/pencil_1.png')
pen_icon=pygame.image.load('./graphics/pen_3.jpg')
back_icon=pygame.image.load('./graphics/back_icon.jpg')

# =============================================================================
# SET INITIAL CONDITIONS AND CONSTRAINTS AND SCALE SURFACES ACCORDING TO SCREEN
# =============================================================================
#Choose Screen Size
screen_x,screen_y=450,728 #golden ratio for aesthetics

#Scale background images
bg_screen=pygame.transform.scale(bg_screen,(screen_x,screen_y))
bg_board=pygame.transform.scale(bg_board,(screen_x,screen_x))

#scale main menu items
screen_title=pygame.transform.scale(screen_title,(int(0.8*screen_x),int(screen_title.get_size()[1]*(0.8*screen_x/screen_title.get_size()[0]))))
screen_submenu=pygame.transform.scale(screen_submenu,(int(0.6*screen_x),int(0.7*screen_y)))

icon_scale=0.13
sound_effects_icon=pygame.transform.scale(sound_effects_icon, (int(icon_scale*screen_x), int(icon_scale*screen_x)))
music_icon=pygame.transform.scale(music_icon,(int(icon_scale*screen_x), int(icon_scale*screen_x)))

#scale tiles
tile_size=int(bg_board.get_size()[0]*0.1)
tile_images=[pygame.transform.scale(img,(tile_size,tile_size)) for img in tile_images]

#scale pen, pencil, and back icons
pencil_icon=pygame.transform.scale(pencil_icon,(tile_size,tile_size))
pen_icon=pygame.transform.scale(pen_icon,(tile_size,tile_size))
back_icon=pygame.transform.scale(back_icon,(int(1.5*tile_size),tile_size))

#Add alpha value to title and submenu images 
trans_color=screen_title.get_at((0,0))
screen_title.set_colorkey(trans_color)
screen_submenu.set_colorkey(trans_color)

#Add alpha channel to pen and back icons
pen_icon.set_colorkey(pen_icon.get_at((0,0)))
back_icon.set_colorkey((255,255,255))


#Screen Size
win=pygame.display.set_mode(bg_screen.get_size())

clock=pygame.time.Clock()

#track the times a tile was misplayed
errors=0

#title
pygame.display.set_caption('Pseudo Ku')

# =============================================================================
# TILES FOR THE BOARD
# =============================================================================

class tile(object):
    def __init__(self,x,y,value,width=50,height=50):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.value=value
        
    def draw(self):
        win.blit(tile_images[self.value-1],(self.x,self.y))
        
        font=pygame.font.SysFont('comicsans',30)
        text=font.render(str(self.value),1,(255,255,255))
        win.blit(text,(int(self.x+self.width/2-text.get_size()[0]/2),int(self.y+self.height/2-text.get_size()[1]/2)))

# =============================================================================
# MAIN PAGE
# =============================================================================

class main_page(object):
    def __init__(self,x=0,y=0,width=screen_x,height=screen_y):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        
        #location of title and sub_menu
        self.title_loc=(int(self.width/2-screen_title.get_size()[0]/2),int(self.height*0.05))
        self.sub_menu_loc=(int(0.9*self.width-screen_submenu.get_size()[0]),int(0.95*self.height-screen_submenu.get_size()[1]))
        
        #submenu options
        self.menu_options=['Easy','Medium','Hard','Expert','About']
        self.font=pygame.font.SysFont('tahoma',50,bold=True)
        
        #locations of music and sound effects icons
        self.music_loc=(int(self.sub_menu_loc[0]*0.5-music_icon.get_size()[0]*0.5), int(self.sub_menu_loc[1]+screen_submenu.get_size()[1]*0.3))
        self.sound_effect_loc=(int(self.sub_menu_loc[0]*0.5-sound_effects_icon.get_size()[0]*0.5), int(self.sub_menu_loc[1]+screen_submenu.get_size()[1]*0.6))
        
    def draw(self):
        #ADD TITLE
        win.blit(screen_title, self.title_loc)
        
        #ADD SUB MENU
        win.blit(screen_submenu, self.sub_menu_loc)
        
        #ADD TEXT TO SUBMENU
        item=0
        for option in self.menu_options:
            text=self.font.render(option,1,(100,100,100))
            win.blit(text,(int(self.sub_menu_loc[0]+screen_submenu.get_size()[0]/2-text.get_size()[0]/2),int(self.sub_menu_loc[1]+screen_submenu.get_size()[1]*(0.5+item)/(1+len(self.menu_options)))))
            item+=1
            
        #ADD SOUND EFFECTS AND MUSIC ICONS
        win.blit(music_icon,self.music_loc)
        win.blit(sound_effects_icon,self.sound_effect_loc)
        
        
# =============================================================================
# GAME BOARD
# =============================================================================
class game_board(object):
    
    def __init__(self,x,y,width,height,difficulty,arr,pencil_marks):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        
        #Load images for all tiles played in given locations {(x,y):value,...}
        self.arr=arr
        
        #Load pencil marks (text) for all uninserted values {(x,y):[values],...}
        self.pencil_marks=pencil_marks
        
        #difficulty for when the board is first set
        self.difficulty=difficulty
        
        #Has the board been populated with the initial values
        self.board_set=False
        
        #add font for the tiles
        self.font=pygame.font.SysFont('tahoma',35,bold=True)
        
        #Box (highlight) the input square on a grid if it is selected by the user
        self.is_boxed=False
        
        #The square is given by grid coordinates i.e. (0,0) or (4,8)
        self.boxed=None
        
        
        # =============================================================================
        # locations of each icon and active area
        # =============================================================================
        
        #input tile row and spacing between left side of each tile
        self.input_tiles_y=int(self.y+bg_board.get_size()[1]*1.08)
        self.buffer_between_tiles=tile_size*1.05
        
        #pen
        self.pen_y=int(self.input_tiles_y+tile_size+0.5*(bg_screen.get_size()[1]-self.input_tiles_y-tile_size)-pen_icon.get_size()[1]*0.5)
        self.pen_x=int(0.36*bg_screen.get_size()[0]-pen_icon.get_size()[0]*0.5)
        
        #pencil
        self.pencil_y=self.pen_y
        self.pencil_x=int(0.63*bg_screen.get_size()[0]-pencil_icon.get_size()[0]*0.5)
        
        #music
        self.music_y=self.pen_y
        self.music_x=int(0.1*bg_screen.get_size()[0]-music_icon.get_size()[0]*0.5)
        
        #sound effects
        self.sound_effects_y=self.pen_y
        self.sound_effects_x=int(0.9*bg_screen.get_size()[0]-sound_effects_icon.get_size()[0]*0.5)
        
        #back button
        self.back_y=int(0.5*tile_size)
        self.back_x=int(0.5*tile_size)
        

        
    def draw(self):
        global elapsed_time, clock
        global square, square_of_focus
        
        win.blit(bg_board,(self.x,self.y))
        
        #Add lines for sudoku blocks
        for i in range(1,9):
            pygame.draw.line(win,(255,255,255),(self.x+border_thickness+i*line_spacing,self.y+border_thickness),(self.x+border_thickness+i*line_spacing,self.y+border_thickness+grid_size))
        for j in range(1,9):
            pygame.draw.line(win,(255,255,255),(self.x+border_thickness,self.y+border_thickness+j*line_spacing),(self.x+border_thickness+grid_size,self.y+border_thickness+j*line_spacing))
                
        #If sudoku is not populated, populate the sudoku
        if not self.board_set:
            self.arr=populate_board(self.difficulty)
            self.board_set=True
            
        #Add Tiles
        for (row,column) in product(range(9),range(9)):
            if self.arr[row,column]!=0:
                #Blit Tile
                tile_x=int(self.x+border_thickness+column*line_spacing+(line_spacing-tile_size)/2)
                tile_y=int(self.y+border_thickness+row*line_spacing+(line_spacing-tile_size)/2)
                win.blit(tile_images[self.arr[row,column]-1],(tile_x,tile_y))
                
                #Blit Text
                text=self.font.render(str(self.arr[row,column]),1,(255,255,255))
                win.blit(text,(int(tile_x+0.5*tile_size-0.5*text.get_size()[0]), int(tile_y+0.5*tile_size-0.5*text.get_size()[1])))
        
        #Add thick lines for boxes
        for i in range(1,3):
            pygame.draw.line(win,(255,255,255),(self.x+border_thickness+3*i*line_spacing,self.y+border_thickness),(self.x+border_thickness+3*i*line_spacing,self.y+border_thickness+grid_size),10)
        for j in range(1,3):
            pygame.draw.line(win,(255,255,255),(self.x+border_thickness,self.y+border_thickness+3*j*line_spacing),(self.x+border_thickness+grid_size,self.y+border_thickness+3*j*line_spacing),10)

        #Highlight a box if the user is focusing on it to insert a value
        if self.is_boxed:
            column,row=self.box
            tile_x=int(self.x+border_thickness+column*line_spacing+(line_spacing-tile_size)/2)
            tile_y=int(self.y+border_thickness+row*line_spacing+(line_spacing-tile_size)/2)
            pygame.draw.rect(win,(0,0,128),(tile_x,tile_y,tile_size,tile_size),width=2)
            
        #Add a line of tiles below the grid
        count=0
        for surf in tile_images:
            #Add row of tiles at location (surf_x,surf_y)
            surf_x=int(self.x+count*self.buffer_between_tiles+0.5*(bg_screen.get_size()[0]-9*self.buffer_between_tiles))
            surf_y=self.input_tiles_y
            if on_pen:
                #only blit the row of selectable tiles if in pen mode
                win.blit(surf,(surf_x,surf_y))
            count+=1
            
            #Blit Text
            if on_pen:
                #white text on tiles for permanent pen mode
                text=self.font.render(str(count),1,(255,255,255))
            else:
                #white text no boxes for pencil mode
                text=self.font.render(str(count),1,(0,0,0))
            win.blit(text,(int(surf_x+0.5*tile_size-0.5*text.get_size()[0]), int(surf_y+0.5*tile_size-0.5*text.get_size()[1])))
        
        #Add a pen and pencil below the boxes that will be used to switch
        #between writing potential values and permanent values
        win.blit(pen_icon,(self.pen_x,self.pen_y))
        win.blit(pencil_icon,(self.pencil_x,self.pencil_y))
        
        #Add sound effects and music button on game page too
        win.blit(music_icon,(self.music_x,self.music_y))
        win.blit(sound_effects_icon,(self.sound_effects_x,self.sound_effects_y))
    
        #Add a back button to return to the main menu
        win.blit(back_icon,(self.back_x,self.back_y))
        
        #Add a timer in the top right corner
        elapsed_time+=clock.tick()/1000
        zeros='00'
        if elapsed_time>=3600:
            h=str(int(elapsed_time//3600))
            m=str(int(elapsed_time//60))
            s=str(int(elapsed_time%60))
            t=h+':'+zeros[:-len(m)]+m+':'+zeros[:-len(s)]+s
        else:
            m=str(int(elapsed_time//60))
            s=str(int(elapsed_time%60))
            t=zeros[:-len(m)]+m+':'+zeros[:-len(s)]+s
            
        text=self.font.render(t,1,(0,0,0))            
        time_y=int(0.5*tile_size)
        time_x=int(bg_screen.get_size()[0]-0.5*tile_size-text.get_size()[0])
        win.blit(text,(time_x,time_y))

# =============================================================================
# GENERATE INITIAL VALUES BASED ON SELECTED DIFFICULTY
# =============================================================================
def populate_board(difficulty):
    return np.ndarray.astype(np.genfromtxt('./puzzles/sudoku_'+difficulty.lower()+'.txt',delimiter=' '),'int')


# =============================================================================
# RETURN WHAT (IF ANY) ITEM WAS CLICKED BY THE MOUSE
# =============================================================================
def clicked(x,y):
    '''
    item_locations={'text':(x1,y1,x2,y2),icon_name:(x1,y1,x2,y2)}
    where x1 and y1 are top left corner and x2 and y2 are bottom right corner
    
    check if click was in any of the ranges in item_locations
    
    if so return location_name as string
    
    if not return None
    '''
    pygame.time.delay(100)

    item_locations={}
    
    # =============================================================================
    # WHEN ON MAIN MENU POPULATE item_locations WITH ITEMS ON MENU    
    # =============================================================================
    if on_menu:
        #The sub-menu items
        count=0
        for item in screen.menu_options:
            text=screen.font.render(item,1,(100,100,100))
            item_locations[item]=(
                    int(screen.sub_menu_loc[0]+screen_submenu.get_size()[0]/2-text.get_size()[0]/2),
                    int(screen.sub_menu_loc[1]+screen_submenu.get_size()[1]*(0.5+count)/(1+len(screen.menu_options))),
                    int(screen.sub_menu_loc[0]+screen_submenu.get_size()[0]/2+text.get_size()[0]/2),
                    int(screen.sub_menu_loc[1]+screen_submenu.get_size()[1]*(0.5+count)/(1+len(screen.menu_options))+text.get_size()[1])
                    )
            count+=1
        
        #Sound and Music
        (dx,dy)=music_icon.get_size()
        item_locations['music_icon']=(screen.music_loc[0],screen.music_loc[1],screen.music_loc[0]+dx,screen.music_loc[1]+dy)
        
        (dx,dy)=sound_effects_icon.get_size()
        item_locations['sound_effects_icon']=(screen.sound_effect_loc[0],screen.sound_effect_loc[1],screen.sound_effect_loc[0]+dx,screen.sound_effect_loc[1]+dy)
        
        #LOOK TO SEE IF THE CLICK WAS ON AN ITEM
        for item in item_locations:
            x1,y1,x2,y2=item_locations[item]
            if (x>=x1 and x<=x2) and (y>=y1 and y<=y2):
                return item
        
        #no item was clicked
        return None
    
    # =============================================================================
    # WHEN ON GAME BOARD POPULATE item_locations WITH ITEMS ON BOARD    
    # =============================================================================
    if on_game:
        #The row of numbers on the bottom ['1','2','3',...]
        count=0
        for surf in tile_images:
            #Add row of tiles
            surf_x=int(board.x+count*board.buffer_between_tiles+0.5*(bg_screen.get_size()[0]-9*board.buffer_between_tiles))
            surf_y=int(board.y+bg_board.get_size()[1]*1.08)
            count+=1
            item_locations[str(count)]=(surf_x,surf_y,surf_x+tile_size,surf_y+tile_size)
        

        #the music, pen, pencil, and sound effects
        (dx,dy)=music_icon.get_size()
        item_locations['music_icon']=(board.music_x,board.music_y,board.music_x+dx,board.music_y+dy)
        
        (dx,dy)=sound_effects_icon.get_size()
        item_locations['sound_effects_icon']=(board.sound_effects_x,board.sound_effects_y,board.sound_effects_x+dx,board.sound_effects_y+dy)

        (dx,dy)=pencil_icon.get_size()
        item_locations['pencil_icon']=(board.pencil_x,board.pencil_y,board.pencil_x+dx,board.pencil_y+dy)

        (dx,dy)=pen_icon.get_size()
        item_locations['pen_icon']=(board.pen_x,board.pen_y,board.pen_x+dx,board.pen_y+dy)
        
        (dx,dy)=back_icon.get_size()
        item_locations['back_icon']=(board.back_x,board.back_y,board.back_x+dx,board.back_y+dy)
        
        #if click is on the game board, check which square was clicked
        if (x>=board.x+border_thickness and x<=board.x+grid_size-border_thickness) and (y>=board.y+border_thickness and y<=board.y+grid_size-border_thickness):
            #click was on the sudoku grid
            grid_x=int(9*(-board.x-border_thickness+x)/grid_size)
            grid_y=int(9*(-board.y-border_thickness+y)/grid_size)
            return '({},{})'.format(grid_x,grid_y)
            
            
        #LOOK TO SEE IF THE CLICK WAS ON AN ITEM
        for item in item_locations:
            x1,y1,x2,y2=item_locations[item]
            if (x>=x1 and x<=x2) and (y>=y1 and y<=y2):
                return item
        
        #no item was clicked
        return None

elapsed_time=-0.01
def take_action(action):
    global music_playing, sound_effects_playing
    global on_game, on_menu
    global elapsed_time, clock
    global on_pen, on_pencil
    global difficulty
    global square_of_focus, square
    
    # =========================================================================
    # MAIN MENU ACTIONS   
    # =========================================================================
    if action in ['Easy','Medium','Hard','Expert']:
        #set game difficulty
        difficulty=action
        
        #Switch menu off and game on
        on_game,on_menu=on_menu,on_game
        
        #add tiles to the board according to the difficulty
        populate_board(action)
        
        #Start game timer
        clock=pygame.time.Clock()
        
        #reset the timer to zero only if it is the first time the game is started
        if elapsed_time<0:
            elapsed_time=0
        
    if action=='music_icon':
        if music_playing:
            pygame.mixer.music.stop()
            music_playing=False
        else:
            pygame.mixer.music.play(-1)
            music_playing=True
    
    if action=='sound_effects_icon':
        if sound_effects_playing:
            sound_effects_playing=False
        else:
            sound_effects_playing=True
            
    # =========================================================================
    # IN GAME ACTIONS (except music and sound effects which are listed above)
    # =========================================================================    
    
    if action=='back_icon':
        #Switch game off and menu on
        on_game,on_menu=on_menu,on_game
        
    if action=='pencil_icon':
        on_pencil,on_pen=True,False
    
    if action=='pen_icon':
        on_pen,on_pencil=True,False
    
    #If a square on the grid is clicked
    if action[0]=='(':
        #Note the location on the grid that was clicked by making it
        #the square of focus
        focus=eval(action)
        is_focused=True
        
        #if a square is already boxed and is clicked again, defocus the square
        if focus==board.boxed and board.is_boxed:
            #remove focus from that box
            board.is_boxed=False

        pass
    

# =============================================================================
# REDRAW GAME WINDOW     
# =============================================================================
#Trim thickness around the board
border_thickness=0.017*bg_board.get_size()[0]
grid_size=int(bg_board.get_size()[0]-2*border_thickness)

#spacing between white grid lines
line_spacing=int(grid_size/9)

#switch between board and title screen
on_menu=True
on_game=False

#switch between marking up the board and permanent entries
on_pen=True
on_pencil=False

def redrawGameWindow():
    
    #add wooden screen background
    win.blit(bg_screen,(0,0))
    
    if on_menu:
        screen.draw()
    
    if on_game:
        #add board     
        board.draw()


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

    if on_menu:
        try:
            sudoku_arr=board.arr
        except:
            sudoku_arr=None
        difficulty='easy'

    screen=main_page()
    board=game_board(0,120,bg_board.get_size()[0],bg_board.get_size()[1],difficulty,None,None)

    
    #Move character
    keys=pygame.key.get_pressed()
    mouse=pygame.mouse
    
    #TRACK MOUSE CLICKS
    if mouse.get_pressed()[0]:
        mouse_pos=mouse.get_pos()
        
        #Check to see if a button was clicked
        item_clicked=clicked(mouse_pos[0],mouse_pos[1])
        if item_clicked:
            print(item_clicked)
            take_action(item_clicked)
        
        
    sudoku_arr=board.arr
    
    redrawGameWindow()





pygame.quit()