# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:21:53 2020

@author: Logan Rowe
"""
if __name__=='__main__':
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