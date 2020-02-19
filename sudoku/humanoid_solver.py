# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:01:18 2020

@author: Logan Rowe

Big picture:
    
Write a script that solves a sudoku using the same techniques that a human would
use 
    --maybe rely on brute force tactics if there are only a few empty squares remaining

The purpose of this will be to check if a sudoku is solvable by a human from
a given state and then to list the human method used for each insertion
one at a time
"""

import numpy as np
from itertools import product

class sudoku(object):
    def __init__(self, arr):
        self.arr=np.array(arr)
        
        #Track the history of how the sudoku was solved
        self.history=[]
        
        #Remember how the array looked before solving
        self._locked_arr=self.arr
        
    def show(self):
        print(self.arr)
        
    def insert(self,x,y,value):
        self.arr[y,x]=value
        self.history.append(((x,y),value))
        
    def rows(self):
        return [row for row in self.arr]
    
    def cols(self):
        return [col for col in np.transpose(self.arr)]
    
    def boxes(self):
        self.dx=self.dy=3
        return [box for box in [self.arr[i*self.dx:(i+1)*self.dx,j*self.dy:(j+1)*self.dy] for (i,j) in product(range(0,3),range(0,3))]]
    
    def list_boxes(self):
        return [np.reshape(box,(-1,)) for box in self.boxes()]
    
    @staticmethod
    def in_box(x,y):
        '''
        given x=column and y=row value return the box (x,y) resides in
        
        [[0][1][2]
         [3][4][5]
         [6][7][8]]
        
        Note: this box order coincides with boxes and list_boxes output
        '''
        return (x//3+3*(y//3))
    
    def percent(self):
        '''
        Return what percent of the sudoku is complete
        
        sudoku.percent()
        >>>52.5
        '''
        return round(100*(1-len(self.arr[self.arr==0])/81),2)
        
    
    def square_by_square(self):
        '''
        For each empty square, check values in row and column and box values
        If there is only one possible value, insert the value into the sudoku
        
        Repeat this cycle until no new values are found
        
        Aside: This is the most basic strategy for filling a sudoku puddle, 
        find a square where no other values are allowed and fill it
        '''
        new_values_found=-1
        while new_values_found!=0:
            found_values=0
            for (x,y) in product(range(0,9),range(0,9)):
                if self.arr[y,x]==0:
                    #check column for unused values
                    col_set=set()            
                    for value in range(1,10):
                        if value not in self.cols()[x]:
                            col_set.add(value)
                    
                    #check row for unused values
                    row_set=set()
                    for value in range(1,10):
                        if value not in self.rows()[y]:
                            row_set.add(value)
                    
                    #check box for unused values
                    box_set=set()
                    for value in range(1,10):
                        if value not in self.list_boxes()[self.in_box(x,y)]:
                            box_set.add(value)
                            
                    
                    #Check to see if there is only one possible value
                    intersecting_values=col_set.intersection(row_set.intersection(box_set))
                    if len(intersecting_values)==0:
                        print('No value satisfies position ({},{}), previous error exists.'.format(x,y))
                        return None
                    if len(intersecting_values)==1:
                        #insert the value into the sudoku at location (x,y)
                        true_value=intersecting_values.pop()
                        self.insert(x,y,true_value)
                        #print('({},{}) is {} according to square_by_square method.'.format(x,y,true_value))
                        found_values+=1
            new_values_found=found_values
            print('{} new values inserted into sudoku.'.format(new_values_found))
    
    def all_possible_values(self):
        '''
        Returns a dictoinary of {(x,y):[1,3,5],(x,y):[2,4,6,9]} for all empty
        spaces on the sudoku board
        '''
        
        #Use a dictionary to track what values could go in location (x,y)
        possible_values={}
        
        for (x,y) in product(range(0,9),range(0,9)):
            if self.arr[y,x]==0:
                #check column for unused values
                col_set=set()            
                for value in range(1,10):
                    if value not in self.cols()[x]:
                        col_set.add(value)
                
                #check row for unused values
                row_set=set()
                for value in range(1,10):
                    if value not in self.rows()[y]:
                        row_set.add(value)
                
                #check box for unused values
                box_set=set()
                for value in range(1,10):
                    if value not in self.list_boxes()[self.in_box(x,y)]:
                        box_set.add(value)
                        
                
                #Check to see if there is only one possible value
                intersecting_values=col_set.intersection(row_set.intersection(box_set))
                if len(intersecting_values)==0:
                    print('No value satisfies position ({},{}), previous error exists.'.format(x,y))
                elif len(intersecting_values)==1:
                    #insert the value into the sudoku at location (x,y)
                    true_value=intersecting_values.pop()
                    self.insert(x,y,true_value)
                else:
                    possible_values[(x,y)]=intersecting_values
        
        return possible_values
    
    def _pair_by_pair(self,value_dict,pair_size):
        '''
        Helper function for pair by pair
        
        value_dict: {(x,y):(1,2,3),(x,y):(2,3,6)...} is location and possible values
                for (x,y) values that reside in the same row, box, or column exclusively
                
        pair_size: if 2 it finds doubles: two (x,y) that share the same (2,4) (2,4) and removes
                2 and 4 from the remaining locations in the shared row, box, or column
                
                if 3 it finds triples: three (x,y) that share the same (1, 4, 5) (1, 4, 5) and
                removes 1, 4, and 5 from all other locations in the shared row, box or column
                
                if 4... or 5...
        '''
        col_dict=value_dict
        
        bonded_pair_count=0
        for location in col_dict:
            if len(col_dict[location])==pair_size and list(col_dict.values()).count(col_dict[location])==pair_size:
                #We found two (or pair_size) squares that both can only have the same two values
                bonded_pair=col_dict[location]
                new_col_dict={}
                for k in col_dict:
                    if col_dict[k]!=bonded_pair:
                        new_col_dict[k]=col_dict[k].difference(bonded_pair) 
                    else:
                        new_col_dict[k]=col_dict[k]
                bonded_pair_count+=1
                #print(new_col_dict)
                #print()
        
        # =============================================================================
        # UPDATE DICTIONARY OF POSSIBLE VALUES AND FILL IN ANY DEFNITE SQUARES         
        # =============================================================================
        #If a bonded pair was found, update the full dictionary with the findings from the column
        if bonded_pair_count!=0:
            for key in new_col_dict:
                #If there is a location with only one possibility, then insert that possibility
                if len(new_col_dict[key])==1:
                    true_value=new_col_dict[key].pop()
                    self.insert(key[0],key[1],true_value)
                self.updated_possible_values[key]=new_col_dict[key]
    

    def pair_by_pair(self):
        '''
        perform all square_by_square operations and create a dictionary
        consisting of:
            
        possible_values={frozenset(x,y):[1,3,7], frozenset(x,y):[2,8], ...}
        
        then check each column, row, and box to see if any share two (x,y)
        that are both missing the same [8,2]
        
        When such a set is found, remove 2 and 8 for all other squares in the
        same row, column and/or box (whichever they are shared in)
        
        If any square now has only one value, fill it in.  
        
        Recheck for new pairs (or triplets) and repeat until a new value is inserted
        or no new sets are found.  
        '''
        

        max_pair=3
        while max_pair<8:
            #Start by only looking for doubles (becaues its fast)
            #If the problem is not solved with doubles, switch to doubles and triples
            #and so on until we are looking for pairs of 8
            if int(self.percent())==100:
                max_pair=9
                continue
            
            #Continuallly look for pairs, triplets and quadruplets to reduce the possible
            #values for each space until no forward progress is made or the puzzle is solved
            progress=1
            while progress>0:
                #progress before looking for pairs is pre_loop progress
                preloop_progress=self.percent()
                print(self.percent())
                for pair_size in range(2,max_pair+1):
                    #self.updated_possible_values contains all possible values for each sudoku square
                    self.updated_possible_values=self.all_possible_values()
                    
                    '''
                    Cross reference the possible values for each square that match other squares
                    located in the same row, a column or a box
                    
                    the values contained in identical pairs, triplets or quadruplets 
                    cannot exist in squares outside of the pair
                    
                    #i.e. square1 can be {2,3} square2 can be {2,3} square5 can be {2,3,6} 
                    therefore square5 must be {6} because square1 and square2 must be {2} or {3}.  
                    '''
                
                    # =================================================================
                    # CHECK FOR BONDED PAIRS IN COLUMNS                 
                    # =================================================================
                    for x in range(0,9):
                        col_dict={k:self.updated_possible_values[k] for k in self.updated_possible_values if k[0]==x}
                        
                        #User helper function to find pairs, deduce impossible values
                        #and update the sudoku board when definite values are found
                        self._pair_by_pair(col_dict,pair_size)
                        
                    # =================================================================
                    # CHECK FOR BONDED PAIRS IN ROWS                 
                    # =================================================================
                    for y in range(0,9):
                        row_dict={k:self.updated_possible_values[k] for k in self.updated_possible_values if k[0]==y} 
            
                        #User helper function to find pairs, deduce impossible values
                        #and update the sudoku board when definite values are found
                        self._pair_by_pair(row_dict,pair_size)     
                    
                    # =============================================================================
                    # CHECK FOR BONDED PAIRS IN BOXES
                    # =============================================================================
                    for box in range(0,9):
                        box_dict={k:self.updated_possible_values[k] for k in self.updated_possible_values if self.in_box(k[0],k[1])==box}
            
                        #User helper function to find pairs, deduce impossible values
                        #and update the sudoku board when definite values are found
                        self._pair_by_pair(box_dict,pair_size)   
                        
                progress=self.percent()-preloop_progress
            max_pair+=1
        
    
    def valid(self):
        '''
        Check whether the completed puzzle is a valid solution
        '''
        if int(self.percent())!=100:
            print('Puzzle is incomplete.')
            return
        
        digits=[i for i in range(1,10)]
        for col in self.cols():
            for value in col:
                if value not in digits:
                    return False
        
        for row in self.rows():
            for value in row:
                if value not in digits:
                    return False
                
        for box in self.list_boxes():
            for value in box:
                if value not in digits:
                    return False
        return True
    
    def make_sudoku(self,difficulty):
        '''
        Populate sudoku with 17 random inputs that do not conflict with sudoku rules
        
        Test whether sudoku is solvable by methods used in this class (if so it is unique)
        
        While sudoku is not unique:
            add another random value that does not conflict
            check if sudoku is unique
        
        if expert: return sudoku
        if hard: return sudoku + 5 random inputs from solution history
        if medium: return sudoku + 10 random inputs from solution history
        if easy: return sudoku + 15 random inputs from solution history
        '''
        if difficulty.lower() not in ['easy','medium','hard','expert']:
            print('Difficulty must be in ["easy","medium","hard","expert"]')
            return None
        
        arr=np.full((9,9),0)
        
        while np.sum(arr==0)>81-17:
            #pick a random location on arr that is not filled in
            x,y=np.random.randint(0,9),np.random.randint(0,9)
            while arr[y,x]!=0:
                x,y=np.random.randint(0,9),np.random.randint(0,9)
                
            possible_values=self.possible_values_at(x,y,arr)
            print(possible_values)
            arr[y,x]=np.random.choice([i for i in possible_values])
        
        while True:
            temp_arr=sudoku(arr)
            temp_arr.square_by_square()
            temp_arr.pair_by_pair()
            if int(temp_arr.percent())==100:
                #arr is now a unique sudoku with solution hist [((x,y),value),((x,y),value),...]
                hist=temp_arr.history()
                break
            else:
                #add another value to arr
                x,y=np.random.randint(0,9),np.random.randint(0,9)
                while arr[y,x]!=0:
                    x,y=np.random.randint(0,9),np.random.randint(0,9)
                
                possible_values=self.possible_values_at(x,y,arr)
                arr[y,x]=np.random.choice([i for i in possible_values])
            
            if np.sum(arr==0)<33:
                print('The sudoku was converging on an impossible solution.')
                print('Resetting sudoku to 17 random values.')
                arr=np.full((9,9),0)
        
                while np.sum(arr==0)>81-17:
                    #pick a random location on arr that is not filled in
                    x,y=np.random.randint(0,9),np.random.randint(0,9)
                    while arr[y,x]!=0:
                        x,y=np.random.randint(0,9),np.random.randint(0,9)
                        
                    possible_values=self.possible_values_at(x,y,arr)
                    arr[y,x]=np.random.choice([i for i in possible_values])
        
        
        given_values={'expert':0,
                      'hard':5,
                      'medium':10,
                      'easy':15}
    
        for i in range(given_values[difficulty]):
            #pick a random entry from the solution
            ((x,y),value)=np.random.choice(hist)
            while arr[y,x]!=0:
                #if that entry was already selected try again
                ((x,y),value)=np.random.choice(hist)
            arr[y,x]=value
            
        return arr

    def possible_values_at(self,x,y,temp_arr):
        '''
        returns a list of all possible values for a given square:
        
            In:  possible_values_at(3,4)
            Out: [1,3,6,7,8,9]
        '''        
        
        temp_array=sudoku(temp_arr)
       
        #check column for unused values
        col_set=set()            
        for value in range(1,10):
            if value not in temp_array.cols()[x]:
                col_set.add(value)
        
        #check row for unused values
        row_set=set()
        for value in range(1,10):
            if value not in temp_array.rows()[y]:
                row_set.add(value)
        
        #check box for unused values
        box_set=set()
        for value in range(1,10):
            if value not in temp_array.list_boxes()[temp_array.in_box(x,y)]:
                box_set.add(value)
                
        #Check to see if there is only one possible value
        intersecting_values=col_set.intersection(row_set.intersection(box_set))
        print(intersecting_values)
        return intersecting_values
    

    
def make_sudoku():
    '''
    Populate sudoku with 17 random inputs that do not conflict with sudoku rules
    
    Test whether sudoku is solvable by methods used in this class (if so it is unique)
    
    While sudoku is not unique:
        add another random value that does not conflict
        check if sudoku is unique
    
    if expert: return sudoku
    if hard: return sudoku + 5 random inputs from solution history
    if medium: return sudoku + 10 random inputs from solution history
    if easy: return sudoku + 15 random inputs from solution history
    '''
    
    #    if difficulty.lower() not in ['easy','medium','hard','expert']:
    #        print('Difficulty must be in ["easy","medium","hard","expert"]')
    #        return None
    
    arr=np.full((9,9),0)
    
    #populate every third square with a value
    #make three lists of values where two of the same number are never at the same index
    values_1=np.array([i for i in range(1,10)])
    values_2=np.array([i for i in range(1,10)])
    values_3=np.array([i for i in range(1,10)])
    
    np.random.shuffle(values_1)
    np.random.shuffle(values_2)
    np.random.shuffle(values_3)
    
    #rearrange second list to not conflict with first list
    for idx in [0,3,6]:
        #if values in middle row of boxes align with first row, rotate columns in the offending middle boxes
        while np.sum(values_2[idx:idx+3]==values_1[idx:idx+3])>0:
            temp=[values_2[idx+2],values_2[idx],values_2[idx+1]]
            values_2[idx:idx+3]=temp

    #rearrange third list to not conflict with first or second list
    for idx in [0,3,6]:
        #if values in bottom row of boxes align with first or second row, rotate columns in the offending bottom boxes
        count=0
        while True:
            column_1=values_3[idx] not in [values_2[idx],values_1[idx]]
            column_2=values_3[idx+1] not in [values_2[idx+1],values_1[idx+1]]
            column_3=values_3[idx+2] not in [values_2[idx+2],values_1[idx+2]]
            if column_1 and column_2 and column_3:
                #box values do not interfere with boxes above it
                break
            else:
                #rotate columns in the box until the above conditions are met
                temp=[values_3[idx+2],values_3[idx],values_3[idx+1]]
                values_3[idx:idx+3]=temp
                count+=1
                if count%3==0:
                    #no permuation will satisfy column requirements: shuffle all values in bottom row of boxes
                    np.random.shuffle(values_3)
                    print('shuffling')
    
    #Load list values into the sudoku array
    box_row=0
    for input_values in [values_1,values_2,values_3]:
        column=0
        row=column%3
        for value in input_values:
            arr[3*box_row+row,column]=value
            column+=1
            row=column%3 #stagger values diagonally across box
        box_row+=1
    
    
    
    return(arr)


    
if __name__=='__main__':
    #load array as allinteger values
    arr=np.ndarray.astype(np.genfromtxt('./puzzles/sudoku_expert.txt',delimiter=' '),'int')
    
    '''
    #create sudoku object using array
    s=sudoku(arr)
    s.show()
    s.square_by_square()
    s.pair_by_pair()
    s.show()
    '''
    

    arr=make_sudoku()
    print(arr)
    print()
    s=sudoku(arr)
    
    for idx in range(81):
        x,y=idx%9,idx//9
        if s.arr[y,x]==0:
            s.arr[y,x]=np.random.choice([i for i in s.possible_values_at(x,y,s.arr)])
    print(s.arr)
    
    
    
    
    