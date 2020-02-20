# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 17:43:15 2020

@author: Logan Rowe

Extremely difficult sudoku problems require more than just elimination by bonded pairs

This tree will map a path where every even-depth (0 being the root) node is a location on
the sudoku board, while every odd-depth node is a possible value for that node

The root node is the sudoku square with the fewest potential values (children)
If there is a tie for fewest potential values, multiple trees will be made

Each location node points to all of its children in search order (smallest value to the left)

Each value node points to the next location(s) that have the fewest possible values
in search order (x+4)**2+y where the smallest value is to the left
"""


            
class LocNode(object):
    def __init__(self,parent,value,children,arr):
        self.value=value
        self.alive=True
        self.parent=parent
        self.arr=arr
        if children:
            for idx,child in enumerate(children):
                setattr(self,'child{}'.format(idx),ValNode(self,child,None,self.arr))

class ValNode(object):
    def __init__(self,parent,value,children,arr):
        self.value=value
        self.alive=True
        self.parent=parent
        self.arr=arr
        if children:
            for idx,child in enumerate(children):
                setattr(self,'child{}'.format(idx),LocNode(self,child,None,self.arr))

class SudokuTree(object):
    def __init__(self,value,children,arr):
        self.root=LocNode(None,value,children,arr)
        
    def insert(self,parent,value,children,arr):
        if self.root==None:
            self.root=LocNode(None,value,children,arr)

