# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 22:58:10 2020

@author: Logan Rowe

For expertly crafted extremely difficult sudokus I used sudokus from here:
    
    http://forum.enjoysudoku.com/the-hardest-sudokus-new-thread-t6539.html
    
The name given to the sudoku by its creator is retained in the file name.

    i.e. '{Given Sudoku Name}_extreme.txt'
    
The sudokus are given in the following format:
    
     1 2 . | 4 . . | 3 . . 
     3 . . | . 1 . | . 5 . 
     . . 6 | . . . | 1 . . 
    -------+-------+------
     7 . . | . 9 . | . . . 
     . 4 . | 6 . 3 | . . . 
     . . 3 | . . 2 | . . . 
    -------+-------+------
     5 . . | . 8 . | 7 . . 
     . . 7 | . . . | . . 5 
     . . . | . . . | . 9 8 
     
     
This script simply reformats the sudoku into the following format, ready to 
be read by the humanoid_solver.py or sudoku_game.py scripts.

    1 2 0 4 0 0 3 0 0
    3 0 0 0 1 0 0 5 0
    0 0 6 0 0 0 1 0 0
    7 0 0 0 9 0 0 0 0
    0 4 0 6 0 3 0 0 0
    0 0 3 0 0 2 0 0 0
    5 0 0 0 8 0 7 0 0
    0 0 7 0 0 0 0 0 5
    0 0 0 0 0 0 0 9 8

"""

import numpy as np
import os
import glob

basefile='./puzzles/worlds-hardest/'

name='Discrepancy'

names=[name.split("\\")[-1].split('.')[0] for name in glob.glob(basefile+'*')]
for name in names:
    if '_' not in name:
        with open(basefile+name+'.txt', 'r') as file:
            data = file.read().replace('.', '0')
        
        data=data.split('\n')
        
        #remove horizontal box dividers
        data=data[:3]+data[4:7]+data[8:]
        
        #remove vertical box dividers
        for row in range(len(data)):
            data[row]=data[row].replace('| ','').strip()
            
        
        f=open(basefile+name+'_extreme.txt','w')
        for row in data:
            f.write(row)
            if row!=data[-1]:
                f.write('\n')
        f.close()