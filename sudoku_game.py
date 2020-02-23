# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 00:15:57 2020

@author: Logan Rowe
"""

import pygame
import numpy as np
from itertools import product
import humanoid_solver as hs
import glob

pygame.init()

# =============================================================================
# LOAD GRAPHICS
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
sound_effects_off_icon=pygame.image.load('./graphics/sound_effects_off_icon.png')
music_icon=pygame.image.load('./graphics/music_icon.png')

#Logo
logo=pygame.image.load('./graphics/simple-logo.png')
pygame.display.set_icon(logo)

#pen, pencil, and back icons
pencil_icon=pygame.image.load('./graphics/pencil_1.png')
pen_icon=pygame.image.load('./graphics/pen_3.jpg')
back_icon=pygame.image.load('./graphics/back_icon.jpg')

#cycle for changing music
cycle_icon=pygame.image.load('./graphics/cycle.jpg')

#replay icon for after a game is complete
replay_icons=[pygame.image.load(file) for file in glob.glob('./graphics/rotation/*')]

# =============================================================================
# LOAD SOUND EFFECTS AND MUSIC
# =============================================================================
sound_effects_playing=True
pygame.mixer.init()

#click sound effect
play_tile_sound_effect=pygame.mixer.Sound('./sound-effects/clicks/click-3.wav')

#new game sound effect
new_game_sound_effect=pygame.mixer.Sound('./sound-effects/new-game/gong.wav')

#mistake sound effect
mistake_sound_effect=pygame.mixer.Sound('./sound-effects/oops/light-beat-wrong-bertof.wav')


#Background Music
music_playing=True
music_cycle=0
music_files=['./sound-effects/background/music.mp3','./sound-effects/background/chill-retro-background-magntron.mp3','./sound-effects/background/melancholic-background-goodbyte.mp3','./sound-effects/background/up-beat-electric-background-cebuana.mp3']
music=pygame.mixer.music.load('./sound-effects/background/music.mp3')
pygame.mixer.music.play(-1)

# =============================================================================
# SCALE SURFACES ACCORDING TO WINDOW SIZE
# =============================================================================
#Choose Screen Size
screen_x,screen_y=450,728 #golden ratio for aesthetics

#background images
bg_screen=pygame.transform.scale(bg_screen,(screen_x,screen_y))
bg_board=pygame.transform.scale(bg_board,(screen_x,screen_x))

#main menu items
screen_title=pygame.transform.scale(screen_title,(int(0.8*screen_x),int(screen_title.get_size()[1]*(0.8*screen_x/screen_title.get_size()[0]))))
screen_submenu=pygame.transform.scale(screen_submenu,(int(0.6*screen_x),int(0.7*screen_y)))

#sound-effects, music and cycle
icon_scale=0.13
sound_effects_icon=pygame.transform.scale(sound_effects_icon, (int(icon_scale*screen_x), int(icon_scale*screen_x)))
sound_effects_off_icon=pygame.transform.scale(sound_effects_off_icon, (int(icon_scale*screen_x), int(icon_scale*screen_x)))
music_icon=pygame.transform.scale(music_icon,(int(icon_scale*screen_x), int(icon_scale*screen_x)))
cycle_icon=pygame.transform.scale(cycle_icon,(int(0.4*music_icon.get_size()[0]),int(0.4*music_icon.get_size()[0])))

#tiles
tile_size=int(bg_board.get_size()[0]*0.1)
tile_images=[pygame.transform.scale(img,(tile_size,tile_size)) for img in tile_images]

#pen, pencil, and back icons
pencil_icon=pygame.transform.scale(pencil_icon,(tile_size,tile_size))
pen_icon=pygame.transform.scale(pen_icon,(tile_size,tile_size))
back_icon=pygame.transform.scale(back_icon,(int(1.5*tile_size),tile_size))

#logo and replay icon
logo=pygame.transform.scale(logo,(int(1.3*tile_size),int(1.3*tile_size)))
replay_icons=[pygame.transform.scale(icon,logo.get_size()) for icon in replay_icons]
replay_icon=replay_icons[0]

# =============================================================================
# ADD ALPHA CHANNELS TO IMAGES WITH OPAQUE BACKGROUNDS
# =============================================================================

#Add alpha value to title, and submenu images 
trans_color=screen_title.get_at((0,0))
screen_title.set_colorkey(trans_color)
screen_submenu.set_colorkey(trans_color)

#Add alpha channel to pen, back and cycle icons
pen_icon.set_colorkey(pen_icon.get_at((0,0)))
back_icon.set_colorkey((255,255,255))
cycle_icon.set_colorkey((255,255,255))

#Add alpha channel to replay icons
'''
for icon in replay_icons:
    icon.set_colorkey((255,255,255))
'''

#Screen Size
win=pygame.display.set_mode(bg_screen.get_size())

clock=pygame.time.Clock()

#title
pygame.display.set_caption('Pseudo Ku')

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def puzzle_finished_check():
    #if board is complete (no 0 values) board.puzzle_complete=True
    board.puzzle_complete=np.sum(board.arr==0)==0  
    

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
        self.menu_options=['Easy','Medium','Hard','Expert','Extreme']
        self.font=pygame.font.SysFont('tahoma',50,bold=True)
        
        #locations of music, music cycle, and sound effects icons
        self.music_loc=(int(self.sub_menu_loc[0]*0.5-music_icon.get_size()[0]*0.5), int(self.sub_menu_loc[1]+screen_submenu.get_size()[1]*0.3))
        self.cycle_loc=(int(self.music_loc[0]+music_icon.get_size()[0]),int(self.music_loc[1]+music_icon.get_size()[1]-cycle_icon.get_size()[1]))
        self.sound_effect_loc=(int(self.sub_menu_loc[0]*0.5-sound_effects_icon.get_size()[0]*0.5), int(self.sub_menu_loc[1]+screen_submenu.get_size()[1]*0.6))
        self.sound_effect_off_loc=(int(self.sub_menu_loc[0]*0.5-sound_effects_off_icon.get_size()[0]*0.5), int(self.sub_menu_loc[1]+screen_submenu.get_size()[1]*0.6))

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
        win.blit(cycle_icon,self.cycle_loc)
        if sound_effects_playing:
            win.blit(sound_effects_icon,self.sound_effect_loc)
        else:
            win.blit(sound_effects_off_icon,self.sound_effect_loc)

        
        
# =============================================================================
# GAME BOARD
# =============================================================================
class game_board(object):
    
    def __init__(self,x,y,width,height,difficulty,arr):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        
        #Load images for all tiles played in given locations {(x,y):value,...}
        self.arr=arr
        
        #True if all squares have been filled in the puzzle
        self.puzzle_complete=False
        
        #solutin will be generated when the array is populated
        self.solution=None
        
        #the history of moves ((x,y),value) used to find solution
        self.history=None
        
        #Load pencil marks temporary values for all empty squares {(x,y):[values],...}
        self.pencil_marks={}
        self.pencil_color=(60,60,60)
        self.pencil_font=pygame.font.SysFont('tahoma',11,bold=True)
        
        #difficulty for when the board is first set
        self.difficulty=difficulty
        
        #Has the board been populated with the initial values
        self.board_set=False
        
        #remember the initial state of the board prior to solving
        self.board_start_state=None
        
        #add font for the tiles
        self.font=pygame.font.SysFont('tahoma',35,bold=True)
        
        #Box (highlight) the input square on a grid if it is selected by the user
        self.is_boxed=False
        
        #The square is given by grid coordinates i.e. (0,0) or (4,8)
        self.boxed=None
        self.box_color=(0,0,200)
        
        #box separating line properties
        self.thick_line_thickness=5
        self.thick_line_color=(43,29,14)
        #deep brown: (43,29,14)
        #light brown: (86,58,28)
        
        #grid line properties
        self.thin_line_color=(255,255,255)
        
        #Display a warning message if true
        self.warn=False
        self.warning_message=''
        self.warning_color=(200,0,0)
        self.warning_font=pygame.font.SysFont('tahoma',25,bold=True)
        self.warning_time=2 #seconds
        self.warning_start=0
        
        #If active replay: resets board and auto-replays game one tile at a time
        self.active_replay=False
        self.active_replay_tile_count=0
        
        #Always load sudoku_inkala when in demo mode
        self.demo=False
        
        # =============================================================================
        # locations of each icon and active area
        # =============================================================================
        
        #input tile row and spacing between left side of each tile
        self.input_tiles_y=int(self.y+bg_board.get_size()[1]*1.08)
        self.buffer_between_tiles=tile_size*1.05
        
        #pen_icon
        self.pen_y=int(self.input_tiles_y+tile_size+0.5*(bg_screen.get_size()[1]-self.input_tiles_y-tile_size)-pen_icon.get_size()[1]*0.5)
        self.pen_x=int(0.36*bg_screen.get_size()[0]-pen_icon.get_size()[0]*0.5)
        
        #pencil_icon
        self.pencil_y=self.pen_y
        self.pencil_x=int(0.63*bg_screen.get_size()[0]-pencil_icon.get_size()[0]*0.5)
        
        #music
        self.music_y=self.pen_y
        self.music_x=int(0.1*bg_screen.get_size()[0]-music_icon.get_size()[0]*0.5)
        
        #sound effects
        self.sound_effects_y=self.pen_y
        self.sound_effects_x=int(0.9*bg_screen.get_size()[0]-sound_effects_icon.get_size()[0]*0.5)
        
        #sound effects off
        self.sound_effects_off_y=self.sound_effects_y
        self.sound_effects_off_x=self.sound_effects_x
        
        #back button
        self.back_y=int(0.5*tile_size)
        self.back_x=int(0.5*tile_size)
        
        #logo
        self.logo_y=int(0.5*tile_size)
        self.logo_x=int(bg_screen.get_size()[0]*0.5-logo.get_size()[0]*0.5)
        
        #replay icon (replaces logo at end of game)
        self.replay_y=self.logo_y
        self.replay_x=self.logo_x
        self.replay_icon=replay_icon
        
        #cycle-icon
        self.cycle_x=int(self.music_x+music_icon.get_size()[0])
        self.cycle_y=int(self.music_y+music_icon.get_size()[1]-cycle_icon.get_size()[1])
        
        

        
    def draw(self):
        global elapsed_time, clock
        global is_focused
        
        win.blit(bg_board,(self.x,self.y))
        
        #ADD A GRID FOR THE SUDOKU TILES
        line_start_buffer=1 #[pixels] shift the beginning of the line to account for rounding errors
        #line_end_buffer=0 #[pixels] shift the end of the line to account for rounding errors
        for i in range(1,9):
            #vertical lines
            pygame.draw.line(win,self.thin_line_color,(int(self.x+border_thickness+i*line_spacing),int(line_start_buffer+self.y+border_thickness)),(int(self.x+border_thickness+i*line_spacing),int(self.y+border_thickness+grid_size)))
        for j in range(1,9):
            #horizontal lines
            pygame.draw.line(win,self.thin_line_color,(int(line_start_buffer+self.x+border_thickness),int(self.y+border_thickness+j*line_spacing)),(int(self.x+border_thickness+grid_size),int(self.y+border_thickness+j*line_spacing)))
                
        #IF THE SUDOKU IS EMPTY POPULATE IT WITH INITIAL TILE VALUES
        #ALSO STORE THE SOLUTION AND HISTORY OF MOVES
        if not self.board_set:
            self.arr=populate_board(self.difficulty)
            self.board_set=True
            self.board_start_state=np.copy(self.arr)
            
            temp_sudoku=solve_sudoku(self.arr)
            self.solution=temp_sudoku.arr
            self.history=temp_sudoku.history_intelligent
            
        #ADD TILES
        for (row,column) in product(range(9),range(9)):
            if self.arr[row,column]!=0:
                #Blit Tile
                tile_x=int(self.x+border_thickness+column*line_spacing+(line_spacing-tile_size)/2)
                tile_y=int(self.y+border_thickness+row*line_spacing+(line_spacing-tile_size)/2)
                win.blit(tile_images[self.arr[row,column]-1],(tile_x,tile_y))
                
                #Blit Text
                text=self.font.render(str(self.arr[row,column]),1,(255,255,255))
                win.blit(text,(int(tile_x+0.5*tile_size-0.5*text.get_size()[0]), int(tile_y+0.5*tile_size-0.5*text.get_size()[1])))
        
        #ADD PENCIL MARKS
        for square in self.pencil_marks:
            (column,row)=square
            square_x=int(self.x+border_thickness+column*line_spacing+(line_spacing-tile_size)/2)
            square_y=int(self.y+border_thickness+row*line_spacing+(line_spacing-tile_size)/2)
            
            #make pencil text 3 numbers separated by commas and only three numbers per row i.e.:
            #1, 2, 3
            #5, 7, 9
            text=''
            for idx,number in enumerate(sorted(self.pencil_marks[square])):
                text+=str(number)
                if (idx+1)%3!=0:
                    text+=', '
                else:
                    text+='-'
            
            #make 1 to 3 rows of text to blit separately
            input_text=text.split('-')
            
            #Blit Text
            for idx,text in enumerate(input_text):
                text=self.pencil_font.render(text,1,self.pencil_color)
                height=(idx-1)*text.get_size()[1]
                win.blit(text,(int(square_x+0.5*tile_size-0.5*text.get_size()[0]), int(square_y+0.5*tile_size-0.5*text.get_size()[1]+height)))
        
        #ADD THICK LINES FOR BOXES
        for i in range(1,3):
            pygame.draw.line(win,self.thick_line_color,(self.x+border_thickness+3*i*line_spacing,self.y+border_thickness),(self.x+border_thickness+3*i*line_spacing,self.y+border_thickness+grid_size),self.thick_line_thickness)
        for j in range(1,3):
            pygame.draw.line(win,self.thick_line_color,(self.x+border_thickness,self.y+border_thickness+3*j*line_spacing),(self.x+border_thickness+grid_size,self.y+border_thickness+3*j*line_spacing),self.thick_line_thickness)

        #HIGHLIGHT A BOX IF THE USER IS FOCUSING ON THE BOX TO INSERT A VALUE
        if self.is_boxed:
            if type(self.boxed)==tuple:
                column,row=self.boxed[0],self.boxed[1]
                tile_x=int(self.x+border_thickness+column*line_spacing+(line_spacing-tile_size)/2)
                tile_y=int(self.y+border_thickness+row*line_spacing+(line_spacing-tile_size)/2)
                pygame.draw.rect(win,self.box_color,(tile_x,tile_y,tile_size,tile_size),3)
            elif type(self.boxed)==list:
                for item in self.boxed:
                    column,row=item[0],item[1]
                    tile_x=int(self.x+border_thickness+column*line_spacing+(line_spacing-tile_size)/2)
                    tile_y=int(self.y+border_thickness+row*line_spacing+(line_spacing-tile_size)/2)
                    pygame.draw.rect(win,self.box_color,(tile_x,tile_y,tile_size,tile_size),3)
            
        #ADD A LINE OF TILES BELOW THE GRID (INPUT BOXES)
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
        
        #ADD PEN AND PENCIL ICON BELOW THE INPUT BOXES
        win.blit(pen_icon,(self.pen_x,self.pen_y))
        win.blit(pencil_icon,(self.pencil_x,self.pencil_y))
        
        #ADD ICONS FOR TURNING MUSIC AND SOUND EFFECTS ON/OFF
        win.blit(music_icon,(self.music_x,self.music_y))
        if sound_effects_playing:
            win.blit(sound_effects_icon,(self.sound_effects_x,self.sound_effects_y))
        else:
            win.blit(sound_effects_off_icon,(self.sound_effects_off_x,self.sound_effects_off_y))

        #ADD ICON FOR CYCLING THE MUSIC
        win.blit(cycle_icon,(self.cycle_x,self.cycle_y))
    
        #ADD A BACK BUTTON TO RETURN TO THE MAIN MENU
        win.blit(back_icon,(self.back_x,self.back_y))
        
        #ADD LOGO AS SECRET HELPER BUTTON OR REPLAY BUTTON IF GAME IS FINISHED
        if not self.puzzle_complete:
            win.blit(logo,(self.logo_x,self.logo_y))
        else:
            win.blit(self.replay_icon,(self.replay_x,self.replay_y))
        
        #ADD A GAME TIMER
        #Only count elapsed time if puzzle is not finished
        if not board.puzzle_complete:
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
        
        
        #BLIT WARNING MESSAGE IF ANY
        if self.warning_time+self.warning_start>=elapsed_time:
            message_x=int(0.5*bg_screen.get_size()[0])
            message_y=int(board.y)
            text=self.warning_font.render(self.warning_message,1,self.warning_color)
            win.blit(text,(int(message_x-text.get_size()[0]*0.5),int(message_y-text.get_size()[1])))


# =============================================================================
# GENERATE INITIAL VALUES BASED ON SELECTED DIFFICULTY
# =============================================================================
def populate_board(difficulty):
    board.demo=False
    if board.demo:
        puzzle='./puzzles/extreme/ArtoInkala_extreme.txt'
    else:
        #pick a random puzzle from the collection of puzzles for given difficulty
        puzzle=np.random.choice([i for i in glob.glob('./puzzles/'+difficulty.lower()+'/*')])
    
    #return the puzzle after converting it to a numpy array
    return np.ndarray.astype(np.genfromtxt(puzzle,delimiter=' '),'int')

def solve_sudoku(arr):    
    arr=hs.sudoku(arr)
    
    if int(arr.percent())!=100:
        #if the sudoku is not already solved, use hs.solve_intelligent() 
        arr.solve_intelligent(arr.arr)
    
    if int(arr.percent())==100:
        board.history=arr.history_intelligent
        return arr
    else:
        print('The resulting sudoku would not be solvable by human methods.\n')
        board.warning_message='The resulting sudoku would not be solvable by human methods.'
        board.warning_start=elapsed_time
        if sound_effects_playing:
            mistake_sound_effect.play()
        return None


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
    pygame.time.delay(50)

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
        
        (dx,dy)=cycle_icon.get_size()
        item_locations['cycle_icon']=(screen.cycle_loc[0],screen.cycle_loc[1],screen.cycle_loc[0]+dx,screen.cycle_loc[1]+dy)
        
        
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
        
        (dx,dy)=logo.get_size()
        item_locations['logo']=(board.logo_x,board.logo_y,board.logo_x+dx,board.logo_y+dy)
        
        (dx,dy)=cycle_icon.get_size()
        item_locations['cycle_icon']=(board.cycle_x,board.cycle_y,board.cycle_x+dx,board.cycle_y+dy)
        
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
    global music_playing, sound_effects_playing, music_cycle
    global on_game, on_menu
    global elapsed_time, clock
    global on_pen, on_pencil
    global difficulty
    global focus, is_focused
    global board, screen
    global oops_count
    
    pygame.time.delay(100)
    
    # =========================================================================
    # MAIN MENU ACTIONS   
    # =========================================================================
    if action in ['Easy','Medium','Hard','Expert','Extreme']:
        if sound_effects_playing:
            new_game_sound_effect.play()
        
        #set game difficulty
        difficulty=action
        oops_count=0
        
        board=game_board(0,120,bg_board.get_size()[0],bg_board.get_size()[1],difficulty,None)
        
        elapsed_time=0
        
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
            
    if action=='cycle_icon' and music_playing:
        music_cycle+=1
        pygame.mixer.music.load(music_files[music_cycle%len(music_files)])
        pygame.mixer.music.play(-1)
            
    # =========================================================================
    # IN GAME ACTIONS (except music and sound effects which are listed above)
    # =========================================================================    
    
    if action=='back_icon':
        screen=main_page()
        
        #Switch game off and menu on
        on_game,on_menu=on_menu,on_game
        
    if action=='pencil_icon':
        on_pencil,on_pen=True,False
    
    if action=='pen_icon':
        on_pen,on_pencil=True,False
        
    if action=='logo' and board.puzzle_complete!=True:
        #Fill in the next human solvable value
        for ((x,y),val) in board.history:
            if board.arr[y,x]==0:
                board.arr[y,x]=val
                board.pencil_marks[(x,y)]=[]
                board.is_boxed=False
                puzzle_finished_check()
                if sound_effects_playing:
                    play_tile_sound_effect.play()
                break
        return None
    
    if action=='logo' and board.puzzle_complete:
        board.active_replay=True
        board.active_replay_tile_count=0
        
    if action[0]=='(':
        #Note the location on the grid that was clicked by making it
        #the square of focus
        focus=eval(action)
        
        #if a square is already boxed and is clicked again, defocus the square
        if board.is_boxed and focus==board.boxed:
            #remove focus from that box
            is_focused=False
            board.is_boxed=False
            board.boxed=tuple((focus[0],focus[1]))
        #highlight the new square if the square is not solved for yet
        elif focus!=board.boxed and board.arr[focus[::-1]]==0:
            board.is_boxed=True
            board.boxed=tuple(focus)
            is_focused=True
            
            #make box blue
            board.box_color=(0,0,200)
        #highlight all squares that have been solved for with that value
        elif focus!=board.boxed and board.arr[focus[::-1]]!=0:
            solved_value=board.arr[focus[::-1]]
            board.is_boxed=True
            board.boxed=[]

            i=0
            for row in board.arr:
                j=0
                for column in row:
                    if board.arr[i,j]==solved_value:
                        board.boxed.append((j,i))
                    j+=1
                i+=1
            
            #make boxes green
            board.box_color=(0,200,0)
    
    
    #If a number is clicked in the input number row and pen is on for permanent inputs
    input_numbers=[str(i) for i in range(1,10)]
    if (action in input_numbers) and on_pen:
        if type(board.boxed)!=tuple:
            #take no action if a valid input square is not already selected
            return None
        elif type(board.boxed)==tuple and len(board.arr[board.arr==int(action)])==9:
            #if there are already 9 of this number inserted
            #highlight the inserted values on the board
            board.is_boxed=True
            board.boxed=[]

            i=0
            for row in board.arr:
                j=0
                for column in row:
                    if board.arr[i,j]==int(action):
                        board.boxed.append((j,i))
                    j+=1
                i+=1
            
            #make boxes green
            board.box_color=(0,200,0)
            
        elif type(board.boxed)==tuple and board.solution[board.boxed[::-1]]==int(action):
            #If a box is selected and the input value matches the solution
            #add the input value into the array, unbox the square and remove pencil marks
            board.arr[board.boxed[::-1]]=int(action)
            board.is_boxed=False
            board.pencil_marks[board.boxed]=[]
            puzzle_finished_check()
            if sound_effects_playing:
                play_tile_sound_effect.play()
        elif type(board.boxed)==tuple and board.solution[board.boxed[::-1]]!=int(action):
            #an input was inserted, but it does not agree with the solution
            violation=True
            
            #check if the input value violates any box, row or column rules
            input_col,input_row=board.boxed[0],board.boxed[1]
            test_arr=hs.sudoku(arr=board.arr)
            test_arr.insert(board.boxed[0],board.boxed[1],int(action))
            if list(test_arr.cols()[input_col]).count(int(action))==1:
                if list(test_arr.rows()[input_row]).count(int(action))==1:
                    if list(test_arr.list_boxes()[test_arr.in_box(input_col,input_row)]).count(int(action))==1:
                        violation=False
            
            if violation:
                print('This is not a valid entry')  
                board.warning_message='Not a valid entry.'
                board.warning_start=elapsed_time
                if sound_effects_playing:
                    mistake_sound_effect.play()
                return None

            #if the value is not in violation of box, row or column rules
            #check to see if a solution exists to the array with the new input value
            if solve_sudoku(test_arr.arr)!=None:
                board.arr[board.boxed[::-1]]=int(action)
                board.is_boxed=False
                board.pencil_marks[board.boxed]=[]
                puzzle_finished_check()
            else:
                print('This entry would lead to an unsolvable puzzle.')
                board.warning_message='Entry makes sudoku unsolvable.'
                board.warning_start=elapsed_time
                oops_count+=1
                if sound_effects_playing:
                    mistake_sound_effect.play()
                return None
        
        
    #IF A NUMBER IS CLICKED IN INPUT ROW AND PENCIL IS ON FOR TEMPORARY MARKING
    if (action in input_numbers) and on_pencil:
        if type(board.boxed)!=tuple:
            #take no action if a valid input square is not already selected
            return None
        if board.boxed in board.pencil_marks.keys():
            #the box has been marked by a pencil before
            if int(action) in board.pencil_marks[board.boxed]:
                #the pencil mark is in the box already, remove it
                board.pencil_marks[board.boxed].remove(int(action))
                return None
            else:
                #the pencil mark is not already in the box, so lets add it
                board.pencil_marks[board.boxed].append(int(action))
        else:
            #The box has not been touched by pencil before so lets add the first mark
            board.pencil_marks[board.boxed]=[int(action)]


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

#set starting point for replay icon
angle_idx=0

def redrawGameWindow():
    global replay_icons, angle_idx
    
    #add wooden screen background
    win.blit(bg_screen,(0,0))
    
    if on_menu:
        screen.draw()
        
        
    if on_game:          
        #add board     
        board.draw()
        
        if board.puzzle_complete:
            angle_idx=int((angle_idx+1)%len(replay_icons)) #because every other angle
            board.replay_icon=replay_icons[angle_idx]
            
            #SHOW A REPLAY OF THE GAME IF REPLAY BUTTON IS PRESSED
            if board.active_replay:
                if board.active_replay_tile_count==0:
                    #reset board to the start state of the puzzle
                    board.arr=np.copy(board.board_start_state)
                    
                #Add tiles in one at a time from history
                ((x,y),val)=board.history[board.active_replay_tile_count]
                if board.arr[y,x]!=0:
                    #if the tile is already on the board find the next tile in history that is not
                    board.active_replay_tile_count+=1
                    ((x,y),val)=board.history[board.active_replay_tile_count]
                
                #add the tile to the board
                board.arr[y,x]=val
                pygame.time.delay(150)
                
                board.active_replay_tile_count+=1
                
                if np.sum(board.arr==0)==0:
                    board.active_replay=False
                    board.active_replay_tile_count=0

            

        

        
    pygame.display.update()

# =============================================================================
# MAIN LOOP
# =============================================================================
screen=main_page()

#start off not focusing on any given square
is_focused=False

#Text for screen (bold and italiscized)
font = pygame.font.SysFont('comicsans', 30,True)

#Track mistakes made
oops_count=0

run = True
while run:
    #slow the game so it only blits every n/1000 seconds
    pygame.time.delay(25)
    
    #get list of all events that happen i.e. keyboard, mouse, ...
    for event in pygame.event.get():
        #Check if the red X was clicked
        if event.type==pygame.QUIT:
            run=False

    #Accept key and mouse inputs
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
    
    redrawGameWindow()





pygame.quit()