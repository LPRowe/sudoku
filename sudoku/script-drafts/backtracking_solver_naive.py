# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:29:07 2020

@author: Logan Rowe
"""

import numpy as np
from humanoid_solver import sudoku

arr=np.ndarray.astype(np.genfromtxt('./puzzles/sudoku_inkala.txt',delimiter=' '),'int')

s=sudoku(arr)

def firstEmptySquare(arr):
    for x in range(9):
        for y in range(9):
            if arr[y,x]==0:
                return(x,y)
    #No empty squares
    return False
                
def valid_input(arr,val,loc):
    x,y=loc%9,loc//9
    if val in s.possible_values_at(x,y):
        return True
    return False

backtrack_count=0
def solve(arr):
    global solution, backtrack_count
    arr=sudoku(arr)
    find=firstEmptySquare(arr.arr)
    
    if int(arr.percent())==100:
        #if there are no empty squares then the puzzle is solved
        solution=arr.arr
        return True
    else:
        x,y=find
    
    for val in arr.possible_values_at(x,y):
        #check if input is valid (we know its valid)
        arr.arr[y,x]=val
        if solve(arr.arr):
            return True
        
        arr.arr[y,x]=0
    
    backtrack_count+=1
    return False

s.show()
t0=time.time()
solve(s.arr)
t1=time.time()
print()
s.arr=solution
s.show()
print()
print(str(round(1000*(t1-t0),1)),'ms')