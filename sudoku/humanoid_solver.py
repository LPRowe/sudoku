# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:01:18 2020

@author: Logan Rowe

Big picture:
    
Write a script that solves a sudoku using the same techniques that a human would
use, avoid using slow brute force tactics like backtracking.

The purpose of this will be to check if a sudoku is solvable by a human from
a given state and then to list the human method used for each insertion
one at a time
"""

import numpy as np
from itertools import product

class sudoku(object):
    def __init__(self, arr=np.full((9,9),0)):
        self.arr=np.array(arr)
        
        #Track the history of how the sudoku was solved
        self.history=[]
        
        #Track the history of how a sudoku was solved using solve_intelligent() (i.e. with backtracking)
        self.history_intelligent=np.full((9,9),0)
        
        #helper counter to keep track of the order values were added to history_intelligent
        self.count_intelligent=0
        
        #almost all sudokus require 0 backtracking to solve, if backtrack_count>0 after solving, the puzzle is rated expert+
        self.backtrack_count=0
        
        #pres_to_future={array_present.tobyte():(array_future.tobyte(),updated_possible_values),...}
        #tracks the state of a sudoku before and after solving with pair_by_pair and uses
        #memoisation techniques to utilize the information when solving with backtracking
        self.pres_to_future={}
        
        #Track the history of how the sudoku was generated
        self.generation=[]
        
        #Track the most complex human pair system used to solve the puzzle 
        #i.e: {2,3,4}, {2,3,4}, {2,3,4,5}, {2,3,4}, {2,3,4,5,6} --> square 3 is 5 and square 5 is 6
        #self.pair_difficulty=3 because triple-bonded pairs were used to solve the puzzle
        self.pair_difficulty=1
        
        #Remember how the array looked before solving
        self._locked_arr=self.arr
        
        #self.print=True only when debugging
        self.print=False
        
    def show(self):
        print(self.arr)
        
    def insert(self,x,y,value):
        '''Inserts a value into the sudoku where x is column and y is row'''
        self.arr[y,x]=value
        self.history.append(((x,y),value))
        
    def rows(self):
        '''Returns a list of the rows in the sudoku'''
        return [row for row in self.arr]
    
    def cols(self):
        '''Returns a list of columns in the sudoku'''
        return [col for col in np.transpose(self.arr)]
    
    def boxes(self):
        '''returns a list of boxes in the column, see in_box() for details about box locations'''
        self.dx=self.dy=3
        return [box for box in [self.arr[i*self.dx:(i+1)*self.dx,j*self.dy:(j+1)*self.dy] for (i,j) in product(range(0,3),range(0,3))]]
    
    def list_boxes(self):
        '''returns a list of the boxes in the sudoku array [[box0],[box1],[box2],...]
        see in_box() for details about the box locations'''
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
        
        In : s=sudoku(arr=arr)
        In : s.percent()
        Out: 52.5
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
                        if self.print:
                            print('No value satisfies position ({},{}), previous error exists.'.format(x,y))
                        return None
                    if len(intersecting_values)==1:
                        #insert the value into the sudoku at location (x,y)
                        true_value=intersecting_values.pop()
                        self.insert(x,y,true_value)
                        if self.print:
                            print('({},{}) is {} according to square_by_square method.'.format(x,y,true_value))
                        found_values+=1
            new_values_found=found_values
            if self.print:
                print('{} new values inserted into sudoku.'.format(new_values_found))
    
    def all_possible_values(self):
        '''Returns a dictoinary of {(x,y):[1,3,5],(x,y):[2,4,6,9]} for all empty
        spaces on the sudoku board'''
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
                    if self.print:
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
        Helper function for pair_by_pair()
        
        value_dict: {(x,y):(1,2,3),(x,y):(2,3,6)...} is location and possible values
                for (x,y) values that reside in the same row, box, or column exclusively
                
        pair_size: if 2 it finds doubles: two (x,y) that share the same (2,4) (2,4) and removes
                2 and 4 from the remaining locations in the shared row, box, or column
                
                if 3 it finds triples: three (x,y) that share the same (1, 4, 5) (1, 4, 5) and
                removes 1, 4, and 5 from all other locations in the shared row, box or column
                
                if 4... or 5...
        '''
        #within this helper function col_dict is general for row, column or box 
        #based on what is in the input value_dict
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
                if self.print:
                    print(new_col_dict)
                    print()
        
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
                    self.count_intelligent+=1
                    self.history_intelligent[key[1],key[0]]=self.count_intelligent
                self.updated_possible_values[key]=new_col_dict[key]
    

    def pair_by_pair(self,highest_pair=3):
        '''
        perform all square_by_square operations and create a dictionary
        consisting of:
            
        possible_values={(x,y):{2,8,9}, (x,y):{2,8}, (x,y):{2,8}, ...}
        
        then checks each column, row, and box to see if any share two (x,y)
        locations that are both only missing the same two values i.e. {2,8}
        
        When such a set is found, remove 2 and 8 for all other squares in the
        same row, column and/or box (whichever they are shared in)
        
        If any square now has only one value, fill it in.  
        
            In the example possible_values shown above, if all three squares share
            a row, column, or box, the first square would be filled in with value 9.
        
        Recheck for new pairs (or triplets or quadruplets or...) and repeat 
        until a new value is inserted or no new sets are found.  
        
        UPDATE 02/21/2020: 
            Extensive testing has shown highest_pair=3 is sufficient to solve
            almost any sudoku.  In general, it is also the most efficient value 
            to use.  
            
            For sudokus that require highest pair of 4 (i.e. 4 boxes that all
            are only missing the same 4 values) it is more efficient to
            use the hybrid pair_by_pair and backtracking method called
            solve_intelligent() than to increase the highest_pair value in
            pair_by_pair().
        '''
        
        max_pair=3
        while max_pair<=highest_pair:
            #Start by only looking for doubles (becaues its fast)
            #If the problem is not solved with doubles, switch to doubles and triples
            #and so on until the puzzle is solved or we end up looking for bonded pairs of length 8
            if int(self.percent())==100:
                max_pair=highest_pair+1
                continue
            
            if max_pair>self.pair_difficulty:
                self.pair_difficulty=max_pair
            
            #Continuallly look for pairs, triplets and quadruplets to reduce the possible
            #values for each space until no forward progress is made or the puzzle is solved
            progress=1
            while progress>0:
                #percentage of the puzzle solved before checking for pairs is pre_loop progress
                preloop_progress=self.percent()
                if self.print:
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
    
    def _mostConstrainedSquare(self,updated_possible_values_dict):
        '''
        This is a helper function for self.solve_intelligent()
        
        Returns the most constrained square (x,y), meaning the square that has 
        the fewest possible value options
        
        If there are no constrained squares returns False
        '''
        constrained_squares=[k for k in updated_possible_values_dict if updated_possible_values_dict[k]==min(updated_possible_values_dict.values(),key=len)]
        if len(constrained_squares)>1:
            return (constrained_squares[0][0],constrained_squares[0][1])
        elif len(constrained_squares)==1:
            return (constrained_squares[0][0],constrained_squares[0][1])
        
        #there are no empty squares
        return False
    

    def solve_intelligent(self,arr):
        '''
        THE BEST METHOD FOR SOLVING SUDOKUS (of those in this class)
        
        solve_intelligent(arr) where arr is an unsolved sudoku, will use human
        methods (such as those in pair_by_pair) to completely solve almost any
        sudoku.  
        
        
        In : arr=[[0 8 0 0 0 0 0 0 0]
                  [0 0 1 0 2 5 8 4 3]
                  [0 0 0 0 3 0 0 0 6]
                  [0 0 0 3 0 8 1 0 0]
                  [9 0 0 0 5 0 0 0 8]
                  [0 0 4 2 0 9 0 0 0]
                  [4 0 0 0 8 0 0 0 0]
                  [6 2 7 4 1 0 9 0 0]
                  [0 0 0 0 0 0 0 2 0]
        In : s=sudoku(arr)
        In : s.solve_intelligent(s.arr)
        In : s.show()
        Out: [[3 8 5 6 7 4 2 1 9]
              [7 6 1 9 2 5 8 4 3]
              [2 4 9 8 3 1 7 5 6]
              [5 7 6 3 4 8 1 9 2]
              [9 3 2 1 5 7 4 6 8]
              [8 1 4 2 6 9 5 3 7]
              [4 9 3 5 8 2 6 7 1]
              [6 2 7 4 1 3 9 8 5]
              [1 5 8 7 9 6 3 2 4]]
        
        For sudoku that cannot be solved by the methods used in pair_by_pair alone
        solve_intelligent() will:
            1) Store the current array (array.tobyte()) in its current state
               as a key in pres_to_future dict
            2) Use pair_by_pair() to fill in any squares where a definite correct
               value exists              
            3) When the sudoku array is at a state where a squares value must 
               be guessed before moving forward, update pres_to_future dict
               with tuple (array.tobyte(),updated_possible_values)
               
                   Note: steps 1-3 are for memoisation so if we return to
                   the above board state after making a wrong guess, we do not
                   need to rerun pair_by_pair().  Instead we can simply:
                       
                       array.arr=pres_to_future[array.arr.tobyte()][0] #get array state after pair_by_pair
                       array.arr=np.frombuffer(array.arr,dtype='int32').reshape((9,9),0) #convert back to array from string of bytes
                       array.updated_possible_values=pres_to_future[array.arr.tobytes()][1] #list of possible values for all squares after pair_by_pair
            
            3) Find the most constrained square a.k.a. the square with the fewest possible options            
            4) Check if the array is 100% solved, if so set s.arr=arr.arr
            5) Check if the most constrained square has any options
                    
                - if not a wrong guess was previously made return False -
            
            6) Of the possible values for the most constrained square, try each
               value, calling solve_intelligent() recursively
               
                - if the value does not lead to a solution, reset it to 0 -
                - if it does lead to a solution, step 4 will be triggered -
                
                
            UPDATE 02/21/2020:
                I have not found a sudoku that utilizes the memoisation section
                here, but since the increase in solve time due to its disuse is 
                negligible, I will leave it for the time being.  
        '''
        global solved_sudoku
        
        arr=sudoku(arr)
        
        #MEMOISATION:
        #If a pair by pair solving process has already been done for the given board
        #skip to the end result using pres_to_future dictionary otherwise run the 
        #pair_by_pair solver and add the result to pres_to_future
        hashed_sudoku_present=arr.arr.tobytes()
        if hashed_sudoku_present in self.pres_to_future.keys():
            arr.arr=np.frombuffer(self.pres_to_future[hashed_sudoku_present][0],dtype='int32').reshape((9,9))
            arr.updated_possible_values=self.pres_to_future[hashed_sudoku_present][1]
            print('hash_used')
        else:
            #Try solving arr and use possible values (paired down) as tries
            arr.pair_by_pair(highest_pair=3)
            hashed_sudoku_future=arr.arr.tobytes()
            #future_possible_values=arr.updated_possible_values
            self.pres_to_future[hashed_sudoku_present]=(hashed_sudoku_future,arr.updated_possible_values)
        
        if self.print:
            print(arr.updated_possible_values)
            
        if len(arr.updated_possible_values)>0:
            next_loc=self._mostConstrainedSquare(arr.updated_possible_values)
        elif int(arr.percent())==100:
            #if there are no empty squares then the puzzle is solved
            s.arr=arr.arr
            solved_sudoku=arr
            return True
        else:
            self.backtrack_count+=1
            return False    
        
        x,y=next_loc
        
        if tuple((x,y)) not in arr.updated_possible_values:
            self.backtrack_count+=1
            return False
        
        for val in arr.updated_possible_values[(x,y)]:
            #check if input is valid (we know its valid)
            arr.arr[y,x]=val
            self.count_intelligent+=1
            self.history_intelligent[y,x]=self.count_intelligent
            if self.solve_intelligent(arr.arr):
                return True
            
            arr.arr[y,x]=0
        
        return False
    
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
        
    
    def _generate_full_sudoku(self):
        '''
        This is a helper function for create_puzzle()
        
        1) Creates a 9 by 9 sudoku with all zero values
        2) Randomly fills (in accordance with sudoku rules) row 0 and the first 3 values of row 1
        3) Procedes to solve the sudoku one square at a time focusing on the most constrained square first
        4) If the sudoku is valid (which is true roughly 95% of the time) then it updates s.arr with a full sudoku
                  - if the sudoku is invalid, repeat steps 1-4

        Returns
        -------
        None.

        '''
        if int(self.percent())==100:
            #This way _generate_full_sudoku can be run while on the main page
            #and will not need to be rerun after the difficulty is selected
            #this should reduce the wait time between selecting a puzzle difficulty
            #and seeing the puzzle
            return None
        
        while True:
            self.arr=np.full((9,9),0)
            
            #INITIALIZE SUDOKU WITH RANDOM VALUES THAT UNDERCONSTRAIN THE SUDOKU
            #fill in first row and three values in second row first box
            for idx in range(12):
                x,y=idx%9,idx//9
                if self.arr[y,x]==0:
                    self.arr[y,x]=np.random.choice([i for i in self.possible_values_at(x,y)])
                    
                    #track sudoku generation pattern
                    self.generation.append(((x,y),self.arr[y,x]))
           
            #FILL THE MOST CONSTRAINED BOX WITH A VALID GUESS AND REPEAT UNTIL PUZZLE IS SOLVED
            count=0
            while np.sum(s.arr==0)>0:
                self.pair_by_pair(highest_pair=3)
                
                #insert random value from acceptable choices into the most constrained square
                constrained_squares=[k for k in self.updated_possible_values if self.updated_possible_values[k]==min(self.updated_possible_values.values(),key=len)]
                if len(constrained_squares)==0:
                    #puzzle is complete
                    break
                self.arr[constrained_squares[0][::-1]]=np.random.choice([i for i in self.updated_possible_values[constrained_squares[0]]])
                count+=1
                if self.print:
                    print(self.arr)
                
            self.show()
            if self.valid():
                print('Puzzle fully generated.')
                break
            else:
                print('Oops, that puzzle is broken.  Please wait one second for me to fix it.')
        
        
    
    def create_puzzle(self,difficulty):
        '''
        0) Generate a list of all mirrored pairs and scramble the list
        1) One at a time remove a mirrored pair from the completed sudoku (i.e. s.arr[3,2]=0 and s.arr[2,3]=0)
        2) Check whether the puzzle is still solvable
                If not: replace the piece and try the next mirrored pair
                
        3) Generate a list of all locations that are filled in and scramble the list
        4) One at a time remove the value from the sudoku (i.e. s.arr[5,4]=0)
        5) Check whether the puzzle is still solvable
    
        6) Add 
        
        
        if expert: return sudoku
        if hard: return sudoku + 5 random inputs from solution history
        if medium: return sudoku + 10 random inputs from solution history
        if easy: return sudoku + 15 random inputs from solution history
        '''
        if difficulty.lower() not in ['easy','medium','hard','expert']:
            print('Difficulty must be in ["easy","medium","hard","expert","guru"]')
            return None
        
        #CREATE A VALID SUDOKU THAT IS 100% COMPLETE
        self._generate_full_sudoku()
        
        # =============================================================================
        # ITERATIVELY REMOVE VALUES FROM SUDOKU AND CHECK IF IT IS STILL SOLVABLE
        # =============================================================================
        
        #Create a random ordered list of all of the tile locations in the top 
        #right half of the board
        locations=[]
        for (x,y) in product(range(9),range(9)):
            if x>=y:
                locations.append((x,y)) #x is column and y is row
                        
        #ranomize the order of the locations where tiles will be removed
        np.random.shuffle(locations)
        
        #ITERATIVELY REMOVE VALUES ONLY IF THEY DO NOT MAKE THE PUZZLE UNSOLVABLE
        for loc in locations:
            v1,v2=self.arr[loc],self.arr[loc[::-1]]
            
            self.arr[loc],self.arr[loc[::-1]]=0,0
            static_arr=sudoku(self.arr)
            static_arr.pair_by_pair()
                        
            if static_arr.percent()!=100:
                self.arr[loc],self.arr[loc[::-1]]=v1,v2
        
        hard_sudoku=self.arr
        print(np.sum(hard_sudoku!=0))
        print(hard_sudoku)
        
        
        if difficulty=='expert':
            #Remove a few more tiles to challenge the sudoku experts
            locations=np.where(self.arr!=0) #remaining nonzero values
            locations=[i for i in zip(locations[0],locations[1])] #(x,y) format
            
            np.random.shuffle(locations)
            
            #Iteratively remove any locations that can be removed
            for loc in locations:
                v1=self.arr[loc[::-1]]
                
                self.arr[loc[::-1]]=0
                static_arr=sudoku(self.arr)
                static_arr.pair_by_pair()
                            
                if static_arr.percent()!=100:
                    self.arr[loc[::-1]]=v1
                    
        expert_sudoku=self.arr
        
        print(np.sum(expert_sudoku!=0))
            
        
        


    def possible_values_at(self,x,y):
        '''
        returns a list of all possible values for a given square:
        
            In:  possible_values_at(3,4)
            Out: [1,3,6,7,8,9]
        '''        
        
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
        if self.print:
            print(intersecting_values)
        return intersecting_values
    

def complete_intelligent_history(history_intelligent,solved_sudoku):
    '''
    When backtracking is used the history of the game solution
    gets scrambled and must be reconstructed
    
    h=complete_intelligent_history(s.history_intelligent,solved_sudoku)
    
    where solved_sudoku is a global instance of the class sudoku
        - solved_sudoku.arr has full solution
        - solved_sudoku.history has missing history
        
        -s.history_intelligent has the remaining history of the game
        
    h=[((x,y),value),((x,y),value),...] in sequential order of the tiles played
    
    as always, x is column and y is row
    '''   
    history_arr=history_intelligent
    count=np.max(history_arr)+1
    for data in solved_sudoku.history:
        x,y=data[0]
        history_arr[y,x]=count
        count+=1
    
    print(history_arr)
    
    history=[]
    
    #load history smallest count number first
    history_arr-=np.max(history_arr)
    while np.sum(history_arr==1)<81:
        idx=np.argmin(history_arr)
        x,y=idx%9,idx//9
        history.append(((x,y),solved_sudoku.arr[y,x]))
        history_arr[y,x]=1
    
    return history
    
if __name__=='__main__':
    import time
    #load array as allinteger values
    arr=np.ndarray.astype(np.genfromtxt('./puzzles/sudoku_inkala.txt',delimiter=' '),'int')
    
    '''
    #create sudoku object using array
    s=sudoku(arr)
    print(s.percent())
    s.show()
    #s.pair_by_pair(highest_pair=3)
    t0=time.time()
    s.solve_intelligent(s.arr)
    t1=time.time()
    print(1000*(t1-t0))
    s.show()
    print(s.percent())
    
    print(s.pair_difficulty)
    '''
    '''
    #Generate Full Sudoku
    while True:
        s=sudoku()
        s.generate_full_sudoku()
        print(s.arr)
        print('Valid Sudoku:',s.valid())
        if s.valid():
            break

    #Remove random mirrored tiles and check if sudoku is solvable until none can be removed
    '''
    
    s=sudoku()
    s._generate_full_sudoku()
    t0=time.time()
    s.create_puzzle('hard')
    t1=time.time()
    print(1000*(t1-t0))
    s.show()
