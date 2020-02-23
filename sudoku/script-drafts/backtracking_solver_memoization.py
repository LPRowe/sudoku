# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:29:07 2020

@author: Logan Rowe
"""

import numpy as np
from humanoid_solver import sudoku
import time

difficulties=['easy','medium','hard','expert','inkala']
difficulty=difficulties[-1]
arr=np.ndarray.astype(np.genfromtxt('./puzzles/sudoku_'+difficulty+'.txt',delimiter=' '),'int')

s=sudoku(arr)
#s.arr[0,1]=1
#s.arr[0,2]=2

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

count=0
pres_to_future={} #returns future state of board given a present state of the board
backtrack_count=0
def solve(arr):
    global solution, hist, count, pres_to_future, backtrack_count
    arr=sudoku(arr)
    
    #MEMOISATION:
    #If a pair by pair solving process has already been done for the given board
    #skip to the end result using pres_to_future dictionary otherwise run the 
    #pair_by_pair solver and add the result to pres_to_future
    hashed_sudoku_present=arr.arr.tobytes()
    if hashed_sudoku_present in pres_to_future.keys():
        arr.arr=np.frombuffer(pres_to_future[hashed_sudoku_present][0],dtype='int32').reshape((9,9))
        arr.updated_possible_values=pres_to_future[hashed_sudoku_present][1]
        print('hash_used')
    else:
        #Try solving arr and use possible values (paired down) as tries
        arr.pair_by_pair(highest_pair=3)
        hashed_sudoku_future=arr.arr.tobytes()
        #future_possible_values=arr.updated_possible_values
        pres_to_future[hashed_sudoku_present]=(hashed_sudoku_future,arr.updated_possible_values)
    
    next_loc=mostConstrainedSquare(arr.updated_possible_values)
    
    if int(arr.percent())==100:
        #if there are no empty squares then the puzzle is solved
        solution=arr
        return True
    elif not next_loc:
        backtrack_count+=1
        return False
    else:
        x,y=next_loc
    
    if tuple((x,y)) not in arr.updated_possible_values:
        backtrack_count+=1
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