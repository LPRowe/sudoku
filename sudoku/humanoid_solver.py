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
from location_value_tree import SudokuTree, ValNode, LocNode
from itertools import product

class sudoku(object):
    def __init__(self, arr=np.full((9,9),0)):
        self.arr=np.array(arr)
        
        #Track the history of how the sudoku was solved
        self.history=[]
        
        #Track the history of how the sudoku was generated
        self.generation=[]
        
        #Track the most complex human pair system used to solve the puzzle 
        #i.e: {2,3,4}, {2,3,4}, {2,3,4,5}, {2,3,4}, {2,3,4,5,6} --> square 3 is 5 and square 5 is 6
        #self.pair_difficulty=3 because triple-bonded pairs were used to solve the puzzle
        self.pair_difficulty=1
        
        #Remember how the array looked before solving
        self._locked_arr=self.arr
        
        #turn on print for debugging
        self.print=False
        
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
        Helper function for pair by pair
        
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
                self.updated_possible_values[key]=new_col_dict[key]
    

    def pair_by_pair(self,highest_pair=8):
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
            
    def guess_and_check(self):
        
        def sort_children(names):
            
            return int(name[-1])
        
        constrained_squares=[k for k in self.updated_possible_values if self.updated_possible_values[k]==min(self.updated_possible_values.values(),key=len)]
        
        #Create a sudoku tree for each start location
        root_count=0 #number of trees
        roots=[]
        for idx,location in enumerate(constrained_squares):
            roots.append(SudokuTree(location,constrained_squares[location]))
            root_count+=1
        
        #cycle through all possible solutions stemming from each start guess
        for root in roots:
            
            #When all paths from a node do not lead to a solution that node dies (i.e. node.alive=False)
            while root.alive==True:
                #create a temporary instance of current array
                temp=sudoku(self.arr)
                
                
                temp.arr[root.value[::-1]]=root.child0
                
                pass

        
        
    
    def grind(self):
        '''
        This should only be called if two conditions are met:
            1) pair by pair does not find any solutions, even after looking for 
               doulble-bound through octuple-bound pairs (max_pair=2 through 8)
            2) s.updated_possible_values has no empty values (i.e. (3,2):{} )
               this would signify a previous error was made
        
        1) Set a attempt_count to zero
    
        while solution not found:
            2) temp_count=attempt_count
            3) Find the most constrained square
                i.e. the shortest value in s.updated_possible_values
                     if there is a tie choose the one that occurs first in the dictionary
            4) Guess a value for that square as:
                if len(s.updated_possible_values[(x,y)])>temp_count:
                    temp.arr[y,x]=s.updated_possible_values[(x,y)][temp_count]
                    temp_count=0
                else:
                    temp.arr[y,x]=s.updated_possible_values[(x,y)][-1]
                    temp_count-=len(s.updated_possible_values[(x,y)])
            
                This will ensure that a different combination of guesses is tried each attempt
            
            5) check if puzzle is solved
                if int(s.percent)==100:
                    #puzzle is solved!
                    break
                else:
                    step 6
                        
            6) Check if a solution is still viable
                check=min(s.updated_possible_values_possible_values.values(),key=len)!=0
                if check==False:
                    loop back to step 3
                else:
                    attempt_count+=1
                    loop back to step 2
        '''
        return 
    
        attempt_count=0
        
        while True:
            print(attempt_count)
            
            #used to ensure a new path of guesses is chosen each attempt
            temp_count=attempt_count
            
            constrained_squares=[k for k in self.updated_possible_values if self.updated_possible_values[k]==min(self.updated_possible_values.values(),key=len)]
            
            #Find which square and value to try based on temp_count
            
    
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
        
    
    def generate_complete_sudoku(self):

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
        
        print('puzzle fully generated')
        
        
    
    def generate_sudoku_puzzle(self,difficulty):
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
            print('Difficulty must be in ["easy","medium","hard","expert"]')
            return None
        
        return None
        
        


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
    


    
if __name__=='__main__':
    #load array as allinteger values
    arr=np.ndarray.astype(np.genfromtxt('./puzzles/sudoku_inkala.txt',delimiter=' '),'int')
    
    '''
    #create sudoku object using array
    s=sudoku(arr)
    print(s.percent())
    s.show()
    s.square_by_square()
    s.pair_by_pair()
    s.show()
    print(s.percent())
    
    print(s.pair_difficulty)
    '''
    
    '''
    s=sudoku()
    s.generate_complete_sudoku()
    print(s.arr)
    print('Valid Sudoku:',s.valid())
    
    '''
    
    s=sudoku(arr=arr)
    s.pair_by_pair()
    
    def sort_children(names):
        return ['child{}'.format(i) for i in range(len(names))]
    
    
    temp=sudoku(s.arr)
    temp.pair_by_pair()
    
    constrained_squares=[k for k in temp.updated_possible_values if temp.updated_possible_values[k]==min(temp.updated_possible_values.values(),key=len)]
    
    #Create a sudoku tree for each start location
    root_count=0 #number of trees
    roots=[]
    for idx,location in enumerate(constrained_squares):
        roots.append(SudokuTree(location,temp.updated_possible_values[location],temp.arr))
        root_count+=1
    
    
    root=roots[0].root
                
    def build_and_prune(root):
        curr=root
        print('b')
        #if all child nodes are dead move up to parent node
        if np.sum([eval('curr.{}.alive'.format(child)) for child in [name for name in dir(curr) if 'child' in name]])==0:
            curr.alive=False
            print('a')
            print([eval('curr.{}.alive'.format(child)) for child in [name for name in dir(curr) if 'child' in name]])
            try:
                build_and_prune(curr.parent)
            except:
                pass
            print('Dead branch.')
            return curr.parent.arr
        else:
            #At least one child is alive
            #Check if the current node is a location node
            if type(curr.value)==tuple:
                print('c')
                for child in sort_children([name for name in dir(curr) if 'child' in name]):
                    kid=eval('curr.{}'.format(child))
                    if kid.alive:
                        #Child is alive and is an integer: add to array
                        #temp.arr[curr.value[::-1]]=eval('curr.{}.value'.format(child))
                        curr.arr[curr.value[::-1]]=kid.value
                        
                        temp=sudoku(curr.arr)
                        temp.pair_by_pair()
                        if temp.percent()==100:
                            print(temp.show())
                            return temp.arr
                        curr.arr=temp.arr
                        #Generate grand children that are locations (x,y)
                        constrained_squares=[k for k in temp.updated_possible_values if temp.updated_possible_values[k]==min(temp.updated_possible_values.values(),key=len)]
                        
                        #If the child will produce no children and the sudoku is not solved kill the child node
                        if len(constrained_squares)==100:
                            kid.alive=False
                            continue
                        else:
                            #Remake the child value node so that it contains children as well
                            kid=ValNode(curr,kid.value,constrained_squares,curr.arr)
                            build_and_prune(kid)
                        
            #Check if the current node is a value node
            elif type(curr.value)==int:
                print('d')
                for child in sort_children([name for name in dir(curr) if 'child' in name]):
                    kid=eval('curr.{}'.format(child))
                    if kid.alive:
                        #No need to upate the array when on a value node since single value entries are handled in LocNode loop
                        
                        temp=sudoku(curr.arr)
                        temp.pair_by_pair()
                        if temp.percent()==100:
                            print(temp.show())
                            return temp.arr
                        curr.arr=temp.arr
                        
                        print(temp.updated_possible_values)
                        #generate grandchildren that are values
                        try:
                            grandchildren=temp.updated_possible_values[kid.value]
                        except:
                            kid.alive=False
                            continue
                        print('grandchildren')
                        print(grandchildren)
                        print(temp.updated_possible_values)
                        if len(grandchildren)==0:
                            kid.alive=False
                            continue
                        else:
                            #Remake child value node so that it contains children as well
                            kid=LocNode(curr,kid.value,list(grandchildren),curr.arr)
                            build_and_prune(kid)

            else:
                print('e')
                curr=curr.parent
                build_and_prune(curr)
                

    build_and_prune(root)
                
    '''
    #cycle through all possible solutions stemming from each start guess
    for root in roots:
        
        #When all paths from a node do not lead to a solution that node dies (i.e. node.alive=False)
        while root.alive==True:
            #create a temporary instance of current array
            temp=sudoku(self.arr)
            
            
            temp.arr[root.value[::-1]]='child'
            
            pass
    '''