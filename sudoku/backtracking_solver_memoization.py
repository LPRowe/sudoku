# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:29:07 2020

@author: Logan Rowe
"""

import numpy as np
from humanoid_solver import sudoku
import time

arr=np.ndarray.astype(np.genfromtxt('./puzzles/sudoku_inkala.txt',delimiter=' '),'int')

s=sudoku(arr)

def firstEmptySquare(arr):
    for x in range(9):
        for y in range(9):
            if arr[y,x]==0:
                return(x,y)
    #No empty squares
    return False

def mostConstrainedSquare(updated_possible_values_dict):
    '''
    Returns the most constrained square (x,y)
    
    If there are no constrained squares returns False
    '''
    constrained_squares=[k for k in updated_possible_values_dict if updated_possible_values_dict[k]==min(updated_possible_values_dict.values(),key=len)]
    if len(constrained_squares)>1:
        return (constrained_squares[0][0],constrained_squares[0][1])
    elif len(constrained_squares)==1:
        return (constrained_squares[0][0],constrained_squares[0][1])
    
    #there are no empty squares
    return False
                
def valid_input(arr,val,loc):
    x,y=loc%9,loc//9
    if val in s.possible_values_at(x,y):
        return True
    return False

hist=np.full((9,9),0)
count=0

def solve(arr):
    global solution, hist, count
    arr=sudoku(arr)
    
    #Try solving arr and use possible values (paired down) as tries
    arr.pair_by_pair(highest_pair=3)
    for val in arr.history:
        count+=1
        hist[val[0][1],val[0][0]]=count
    
    find=mostConstrainedSquare(arr.updated_possible_values)
    
    if int(arr.percent())==100:
        #if there are no empty squares then the puzzle is solved
        solution=arr
        return True
    elif not find:
        return False
    else:
        x,y=find
    
    if tuple((x,y)) not in arr.updated_possible_values:
        return False
    
    for val in arr.updated_possible_values[(x,y)]:
        #check if input is valid (we know its valid)
        count+=1
        arr.arr[y,x]=val
        hist[y,x]=count
        if solve(arr.arr):
            return True
        
        arr.arr[y,x]=0
    
    return False

s.show()
t0=time.time()
solve(s.arr)
t1=time.time()
print()
s.arr=solution.arr
s.show()
print()
print(str(round(1000*(t1-t0),1)),'ms')