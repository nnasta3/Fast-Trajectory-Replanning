import numpy as np
from graphics import *
import math
import pandas as pd
import random

DrawGrid=True
WallPercentage=30
height=900
width=900
cols=101
rows=101

w=height/rows
h=width/cols


## Manhattan Distance Formula. 
def heuristic(a,b): 
    return (abs(a.horizontal-b.horizontal) + abs(a.vertical-b.vertical))

class State:
    def __init__(self, horizontal, vertical):
        self.horizontal = horizontal
        self.vertical = vertical
        
        # f, g, s, and h values for A*
        self.f = None #g cost + h cost
        self.g = None #distance from starting node
        self.h = None #heuristic 
        self.s = 0 #search value
        self.shape=None

        #States that can be reached from current state
        self.neighbors = None
        self.neighboringWalls = None

        #Tree pointer
        self.Parent = None

        #Blocked status of a state
        self.isBlocked = False

    def draw(self,window,color):
        if self.shape:
            self.shape.setFill(color)
        else:
            self.shape = Rectangle(Point(self.horizontal*w,self.vertical*h),Point((self.horizontal+1)*w,(self.vertical+1)*h))
            self.shape.setFill(color)
            self.shape.draw(window)


    def addNeighbors(self,grid):
        self.neighbors=[]
        self.neighboringWalls=[]

        if self.vertical<cols-1:
            self.neighbors.append(grid[self.horizontal][self.vertical+1])

        if self.vertical>0:
            self.neighbors.append(grid[self.horizontal][self.vertical-1])

        if self.horizontal>0:self.neighbors.append(grid[self.horizontal-1][self.vertical])
        if self.horizontal<rows-1: self.neighbors.append(grid[self.horizontal+1][self.vertical])

class MinHeap:

    #Insert to end of list and bubble up if necessary
    def push(self,node,window):
        #bubbles up smaller values
        def bubbleUp(self,i):
            k=math.floor(i/2) 
            while i > 0 and self[i].f < self[k].f:
                hold = self[k]
                self[k] = self[i]
                self[i]=hold
                i=k
                k=math.floor(i/2)
                

        self.append(node)
        
        #Color the Neighbor that was just visited
        #self[self.__len__()-1].draw(window,'green') 
        #update(100000)
        #if self.__len__() >1:
        bubbleUp(self,self.__len__()-1)
            

    
    #Returns the Min value and balances the heap
    def pop(self,big):
        #use larger g values to break ties
        if big == True:
            if self.__len__() > 1:
                
                #Check for ties
                largest = 0
                dupIndexes = []
                for i in range(self.__len__()):
                    if self[i].g > self[largest].g and self[i].f == self[largest].f:
                        largest = i
                        dupIndexes.clear()
                    elif self[i].g == self[largest].g and self[i].f == self[largest].f:
                        dupIndexes.append(i)

                #No duplicate g values so pop largest
                if dupIndexes.__len__() == 0:
                    hold = self[largest]
                    self[largest] = self[self.__len__()-1]
                    self[self.__len__()-1] = hold
                    retVal = self[self.__len__()-1]

                    self.remove(self[self.__len__()-1])
                    MinHeap.siftDown(self,largest)

                    return retVal
                #Select a random index from dup values
                else:
                    index = random.randint(0,dupIndexes.__len__()-1)
                    hold = self[index]
                    self[index] = self[self.__len__()-1]
                    self[self.__len__()-1] = hold
                    retVal = self[self.__len__()-1]

                    self.remove(self[self.__len__()-1])
                    MinHeap.siftDown(self,index)

                    return retVal
                
            elif self.__len__() == 1:
                retVal = self[0]
                self.remove(self[0])
                return retVal

            elif self.__len__()==0:
                return None

        #use smaller g values to break ties        
        else:
            if self.__len__() >1:

                #Check for ties
                smallest = 0
                dupIndexes = []
                for i in range(self.__len__()):
                    if self[i].g < self[smallest].g and self[i].f == self[smallest].f:
                        smallest = i
                        dupIndexes.clear()
                    elif self[i].g == self[smallest].g and self[i].f == self[smallest].f:
                        dupIndexes.append(i)

                #No duplicate g values so pop largest
                if dupIndexes.__len__() == 0:
                    hold = self[smallest]
                    self[smallest] = self[self.__len__()-1]
                    self[self.__len__()-1] = hold
                    retVal = self[self.__len__()-1]

                    self.remove(self[self.__len__()-1])
                    MinHeap.siftDown(self,smallest)

                    return retVal
                #Select a random index from dup values
                else:
                    index = random.randint(0,dupIndexes.__len__()-1)
                    hold = self[index]
                    self[index] = self[self.__len__()-1]
                    self[self.__len__()-1] = hold
                    retVal = self[self.__len__()-1]

                    self.remove(self[self.__len__()-1])
                    MinHeap.siftDown(self,index)

                    return retVal  
            elif self.__len__() == 1:
                retVal = self[0]
                self.remove(self[0])
                return retVal

            elif self.__len__()==0:
                return None
        
    #rebalances the heap, takes a heap and an index to sift down from
    def siftDown(self,i):
        smallest = i
        leftChild = 2*i
        rightChild = (2*i)+1
        if leftChild < self.__len__() and  self[i].f > self[leftChild].f:
            smallest=leftChild

        if rightChild < self.__len__() and self[i].f > self[rightChild].f:
            smallest=rightChild

        if smallest != i:
            hold = self[i]
            self[i] = self[smallest]
            self[smallest] = hold

            MinHeap.siftDown(self,smallest)

    def deleteNode(self,targetNode):
        for i in range(self.__len__()):
            if self[i] is targetNode:
                #self[i] = self[self.__len__()-1]
                self.remove(self[i])
                MinHeap.siftDown(self,i)
                break
            else:
                continue
    
    def peek(self):
        return self[0]

    def isEmpty(self):
        if self.__len__() == 0:
            return True
        else:
            return False

def main():
    sumNodesAdaptiveSuccess = 0
    sumNodesAdaptiveFailure = 0

    sumNodesForwardBigTieSuccess = 0
    sumNodesForwardBigTieFailure = 0

    sumNodesForwardSmallTieSuccess = 0
    sumNodesForwardSmallTieFailure = 0

    sumNodesBackwardSmallTieSuccess = 0
    sumNodesBackwardSmallTieFailure = 0

    sumNodesBackwardBigTieSuccess =0
    sumNodesBackwardBigTieFailure = 0

    successCount =0
    failCount= 0

    for worldNum in range(50):
        #Create the gridworld
        grid = [[State(horizontal,vertical) for vertical in range(cols)] for horizontal in range(rows)]
        for horizontal in range(rows):
            for vertical in range(cols):
                grid[horizontal][vertical].addNeighbors(grid)

        window = GraphWin("A* Search Comparisons World %d" %worldNum, height, width,autoflush=False)

        #Generate random blocked states
        for vertical in range(cols):
            for horizontal in range(rows):
                if random.randint(0, 100)<WallPercentage: grid[horizontal][vertical].isBlocked=True

        #Draw the grid once
        for j in range(cols):
            for i in range(rows):
                grid[i][j].draw(window,'dark gray')
                if grid[i][j].isBlocked:grid[i][j].draw(window,'black')

        #Random start (or just start at [0][0]) and endpoints and set start and end to not be a blocked state
        StartNode=grid[0][0]
        EndNode=grid[random.randint(0,100)][random.randint(0,100)]

        StartNode.isBlocked=False
        EndNode.isBlocked=False

        print("WORLD %d" % worldNum)
        #PART 2 EFFECT OF TIES AND PART 3 FORWARD AND BACKWARD###################################################
        #FORWARD
        EndNode.draw(window, 'Orange')
        update(30000)
        StartNode.draw(window, 'light green')
        update(30000)
        successOrFail,avgNumNodesExpanded = RepeatedAstar(grid,window,StartNode,EndNode, True, True)
        
        if successOrFail == True:
            successCount+=1
            print("Repeated Forward A* With Tie Breaking Using Larger G Value")
            print("Target Reached, Average Number of Expanded %d Nodes" %  avgNumNodesExpanded)
            sumNodesForwardBigTieSuccess += avgNumNodesExpanded
        else:
            failCount+=1
            print("Repeated Forward A* With Tie Breaking Using Larger G Value")
            print("Target Cannot Be Reached, Expanded %d Nodes" %  avgNumNodesExpanded)
            sumNodesForwardBigTieFailure += avgNumNodesExpanded

        EndNode.draw(window, 'Orange')
        update(30000)
        StartNode.draw(window, 'light green')
        update(30000)
        successOrFail,avgNumNodesExpanded = RepeatedAstar(grid,window,StartNode,EndNode, True, False)
        
        if successOrFail == True:
            print("Repeated Forward A* With Tie Breaking Using Smaller G Value")
            print("Target Reached, Average Number of Expanded %d Nodes" %  avgNumNodesExpanded)
            sumNodesForwardSmallTieSuccess+=avgNumNodesExpanded
        else:
            print("Repeated Forward A* With Tie Breaking Using Smaller G Value")
            print("Target Cannot Be Reached, Expanded %d Nodes" %  avgNumNodesExpanded)
            sumNodesForwardSmallTieFailure+=avgNumNodesExpanded

        #BACKWARD
        hold = StartNode
        StartNode = EndNode
        EndNode = hold
        StartNode.draw(window, 'orange')
        update(30000)
        EndNode.draw(window, 'light blue')
        update(30000)
        successOrFail,avgNumNodesExpanded = RepeatedAstar(grid,window,StartNode,EndNode, False, True)
        
        if successOrFail == True:
            print("Repeated Backward A* With Tie Breaking Using Larger G Value")
            print("Target Reached, Average Number of Expanded %d Nodes" %  avgNumNodesExpanded)
            sumNodesBackwardBigTieSuccess+=avgNumNodesExpanded
        else:
            print("Repeated Backward A* With Tie Breaking Using Larger G Value")
            print("Target Cannot Be Reached, Expanded %d Nodes" %  avgNumNodesExpanded)
            sumNodesBackwardBigTieFailure+=avgNumNodesExpanded

        StartNode.draw(window, 'orange')
        update(30000)
        EndNode.draw(window, 'light blue')
        update(30000)
        successOrFail,avgNumNodesExpanded = RepeatedAstar(grid,window,StartNode,EndNode, False, False)
        
        if successOrFail == True:
            print("Repeated Backward A* With Tie Breaking Using Smaller G Value")
            print("Target Reached, Average Number of Expanded %d Nodes" %  avgNumNodesExpanded)
            sumNodesBackwardSmallTieSuccess += avgNumNodesExpanded
        else:
            print("Repeated Backward A* With Tie Breaking Using Smaller G Value")
            print("Target Cannot Be Reached, Expanded %d Nodes" %  avgNumNodesExpanded)
            sumNodesBackwardSmallTieFailure += avgNumNodesExpanded
        ##############################################################################

       #PART 3 FORWARD VS BACKWARD###################################################
        #FORWARD
        '''hold = StartNode
        StartNode = EndNode
        StartNode.draw(window, 'light green')
        update(30000)
        EndNode = hold
        EndNode.draw(window, 'Orange')
        update(30000)
        successOrFail,avgNumNodesExpanded = RepeatedAstar(grid,window,StartNode,EndNode, True, True)
        if successOrFail == True:
            print("Repeated Forward A* With Tie Breaking Using Larger G Value")
            print("Target Reached, Average Number of Expanded %d Nodes" %  avgNumNodesExpanded)
        else:
            print("Repeated Forward A* With Tie Breaking Using Larger G Value")
            print("Target Cannot Be Reached, Expanded %d Nodes" %  avgNumNodesExpanded)
        #BACKWARD
        hold = StartNode
        StartNode = EndNode
        EndNode = hold
        StartNode.draw(window, 'orange')
        update(30000)
        EndNode.draw(window, 'light blue')
        update(30000)
        successOrFail,avgNumNodesExpanded = RepeatedAstar(grid,window,StartNode,EndNode, False, True)
        if successOrFail == True:
            print("Repeated Backward A* With Tie Breaking Using Larger G Value")
            print("Target Reached, Average Number of Expanded %d Nodes" %  avgNumNodesExpanded)
        else:
            print("Repeated Backward A* With Tie Breaking Using Larger G Value")
            print("Target Cannot Be Reached, Expanded %d Nodes" %  avgNumNodesExpanded)'''
        ##############################################################################

        #ADAPTIVE A* #################################################################
        hold = StartNode
        StartNode = EndNode
        StartNode.draw(window, 'blue')
        update(30000)
        EndNode = hold
        EndNode.draw(window, 'Orange')
        update(30000)
        successOrFail,avgNumNodesExpanded = AdaptiveAstar(grid,window,StartNode,EndNode)
        if successOrFail == True:
            print("Adaptive A* With Tie Breaking Using Larger G Value")
            print("Target Reached, Average Number of Expanded %d Nodes" %  avgNumNodesExpanded)
            sumNodesAdaptiveSuccess+=avgNumNodesExpanded
        else:
            print("Adaptive A* With Tie Breaking Using Larger G Value")
            print("Target Cannot Be Reached, Expanded %d Nodes" %  avgNumNodesExpanded)
            sumNodesAdaptiveFailure+=avgNumNodesExpanded
        ###############################################################################
        window.close()


    #PRINT TOTALS BELOW ###############################################################
    
    if failCount >0 and successCount == 0:
        sumNodesAdaptiveSuccess = 0
        sumNodesAdaptiveFailure = sumNodesAdaptiveFailure/failCount

        sumNodesForwardBigTieSuccess = 0
        sumNodesForwardBigTieFailure = sumNodesForwardBigTieFailure/failCount

        sumNodesForwardSmallTieSuccess = 0
        sumNodesForwardSmallTieFailure = sumNodesForwardSmallTieFailure/failCount

        sumNodesBackwardSmallTieSuccess = 0
        sumNodesBackwardSmallTieFailure = sumNodesBackwardSmallTieFailure/failCount

        sumNodesBackwardBigTieSuccess = 0
        sumNodesBackwardBigTieFailure = sumNodesBackwardBigTieFailure/failCount

    elif failCount ==0 and successCount > 0:
        sumNodesAdaptiveSuccess = sumNodesAdaptiveSuccess/successCount
        sumNodesAdaptiveFailure = 0

        sumNodesForwardBigTieSuccess = sumNodesForwardBigTieSuccess/successCount
        sumNodesForwardBigTieFailure = 0

        sumNodesForwardSmallTieSuccess = sumNodesForwardSmallTieSuccess/successCount
        sumNodesForwardSmallTieFailure = 0

        sumNodesBackwardSmallTieSuccess = sumNodesBackwardSmallTieSuccess/successCount
        sumNodesBackwardSmallTieFailure = 0

        sumNodesBackwardBigTieSuccess =sumNodesBackwardBigTieSuccess/successCount
        sumNodesBackwardBigTieFailure = 0
    else:
        sumNodesAdaptiveSuccess = sumNodesAdaptiveSuccess/successCount
        sumNodesAdaptiveFailure = sumNodesAdaptiveFailure/failCount

        sumNodesForwardBigTieSuccess = sumNodesForwardBigTieSuccess/successCount
        sumNodesForwardBigTieFailure = sumNodesForwardBigTieFailure/failCount

        sumNodesForwardSmallTieSuccess = sumNodesForwardSmallTieSuccess/successCount
        sumNodesForwardSmallTieFailure = sumNodesForwardSmallTieFailure/failCount

        sumNodesBackwardSmallTieSuccess = sumNodesBackwardSmallTieSuccess/successCount
        sumNodesBackwardSmallTieFailure = sumNodesBackwardSmallTieFailure/failCount

        sumNodesBackwardBigTieSuccess =sumNodesBackwardBigTieSuccess/successCount
        sumNodesBackwardBigTieFailure = sumNodesBackwardBigTieFailure/failCount

    print("NUMBER OF SUCCESSES %d"% successCount)
    print("AVERAGE NODES EXPANDED ON SUCCESS USING FORWARD REPEATED A* AND LARGER G VALUES %d" % sumNodesForwardBigTieSuccess)
    print("AVERAGE NODES EXPANDED ON SUCCESS USING FORWARD REPEATED A* AND SMALLER G VALUES %d" % sumNodesForwardSmallTieSuccess)
    print("AVERAGE NODES EXPANDED ON SUCCESS USING BACKWARD REPEATED A* AND LARGER G VALUES %d" % sumNodesBackwardBigTieSuccess)
    print("AVERAGE NODES EXPANDED ON SUCCESS USING BACKWARD REPEATED A* AND SMALLER G VALUES %d" % sumNodesBackwardSmallTieSuccess)
    print("AVERAGE NODES EXPANDED ON SUCCESS USING ADAPTIVE A* AND LARGER G VALUES %d" % sumNodesAdaptiveSuccess)
    print("NUMBER OF FAILURES %d" % failCount)
    print("AVERAGE NODES EXPANDED ON FAILURE USING FORWARD REPEATED A* AND LARGER G VALUES %d" % sumNodesForwardBigTieFailure)
    print("AVERAGE NODES EXPANDED ON FAILURE USING FORWARD REPEATED A* AND SMALLER G VALUES %d" % sumNodesForwardSmallTieFailure)
    print("AVERAGE NODES EXPANDED ON FAILURE USING BACKWARD REPEATED A* AND LARGER G VALUES %d" % sumNodesBackwardBigTieFailure)
    print("AVERAGE NODES EXPANDED ON FAILURE USING BACKWARD REPEATED A* AND SMALLER G VALUES %d" % sumNodesBackwardSmallTieFailure)
    print("AVERAGE NODES EXPANDED ON FAILURE USING ADAPTIVE A* AND LARGER G VALUES %d" % sumNodesAdaptiveFailure)

def RepeatedAstar(grid,window,StartNode,EndNode, forward, breakBig):

    if forward == True:
        #create openset and closedset
        OpenSet=[]
        ClosedSet=[]

        counter = 0
        colorChange = 0

        numNodesExpanded = 0
        #Reset grid Values
        for j in range(cols):
            for i in range(rows):
                grid[i][j].s = 0
                grid[i][j].f = None
                grid[i][j].g = None
                temp = heuristic(grid[i][j],EndNode)
                grid[i][j].h = temp
                grid[i][j].Parent = None

        StartNode.g=0
        StartNode.h=heuristic(StartNode,EndNode)
        StartNode.f=StartNode.h+StartNode.g
        CurrentNode = StartNode

        while CurrentNode != EndNode:
            counter +=1

            #Initialize current Node
            CurrentNode.g = 0
            CurrentNode.s = counter
            
            EndNode.g = 20000
            EndNode.s = counter

            OpenSet.clear()
            ClosedSet.clear()

            #Insert currentNode into openset
            MinHeap.push(OpenSet, CurrentNode,window)

            computePath(CurrentNode,OpenSet,ClosedSet,EndNode,CurrentNode,window,counter,forward,colorChange,breakBig)
        
            if MinHeap.isEmpty(OpenSet) == True:
                
                return False,ClosedSet.__len__()

            previous=EndNode
            previous.draw(window,"white")
            update(100000)

            while previous.Parent != CurrentNode:  
                previous=previous.Parent 
                previous.draw(window,"white")
                update(100000)           
                
            CurrentNode = previous
            CurrentNode.draw(window,'light green')
            update(100000)

            EndNode.draw(window,'Orange')
            update(100000)

            if colorChange == 1:
                colorChange = 0
            else:
                colorChange = 1

            numNodesExpanded += ClosedSet.__len__()
                
    else:
        
        #create openset and closedset
        OpenSet=[]
        ClosedSet=[]

        counter = 0
        
        
        colorChange = 0

        numNodesExpanded = 0

        #Reset grid Values
        for j in range(cols):
            for i in range(rows):
                grid[i][j].s = 0
                grid[i][j].f = None
                grid[i][j].g = None
                temp = heuristic(grid[i][j],EndNode)
                grid[i][j].h = temp
                grid[i][j].Parent = None

        StartNode.g=0
        StartNode.h=heuristic(StartNode,EndNode)
        StartNode.f=StartNode.h+StartNode.g
        CurrentNode = StartNode
        while CurrentNode != EndNode:
            counter +=1

            #Initialize current Node
            CurrentNode.g = 0
            CurrentNode.s = counter

            EndNode.g = 20000
            EndNode.s = counter

            OpenSet.clear()
            ClosedSet.clear()

            #Insert currentNode into openset
            MinHeap.push(OpenSet, CurrentNode,window)

            computePathBackWard(CurrentNode,OpenSet,ClosedSet,EndNode,StartNode,window,counter,forward,colorChange,breakBig)
            #update(100000)
            if MinHeap.isEmpty(OpenSet) == True:
                print("Target Cannot Be Reached, Expanded %d Nodes" %  ClosedSet.__len__())
                return False,ClosedSet.__len__()

            previous=EndNode

            #Move the EndNode Forward
            previous=previous.Parent
            EndNode = previous

            #Updates the current path
            while previous.Parent != None:  
                previous=previous.Parent 
                previous.draw(window,"white")
                update(100000)           

            EndNode.draw(window,'light blue')
            update(100000)

            if colorChange == 1:
                colorChange = 0
            else:
                colorChange = 1
            
            numNodesExpanded += ClosedSet.__len__()

    avgNumNodesExpanded = numNodesExpanded/50
    

    return True,avgNumNodesExpanded


def computePathBackWard(CurrentNode,OpenSet,ClosedSet,EndNode,StartNode,window,counter,forward,colorChange,breakBig):             
    peekHeap = MinHeap.peek(OpenSet)
    temp = heuristic(peekHeap,EndNode)
    temp +=peekHeap.g
    while EndNode.g > temp and EndNode not in ClosedSet:

        #Remove smallest f value from OpenSet     
        #True is larger g value, false is smaller                  
        CurrentNode = MinHeap.pop(OpenSet,breakBig)

        #Add State to ClosedSet
        ClosedSet.append(CurrentNode)
        
        
        #Color the expanded Node
        if ClosedSet[ClosedSet.__len__()-1] is not None:          
            if forward == False and colorChange == 0:
                ClosedSet[ClosedSet.__len__()-1].draw(window, 'blue')
                #update(100000)
                #StartNode.draw(window, 'Orange')
                #update(100000)
            else:
                ClosedSet[ClosedSet.__len__()-1].draw(window, 'dark blue')
                #update(100000)
                #StartNode.draw(window, 'Orange')
                #update(100000)
        else:
            break

        #Check each action
        for i in range(len(CurrentNode.neighbors)):
            if CurrentNode.neighbors[i].isBlocked == False:
                if CurrentNode.neighbors[i] in ClosedSet:
                    continue
                    
                if CurrentNode.neighbors[i].s < counter:
                    CurrentNode.neighbors[i].g = 20000
                    CurrentNode.neighbors[i].s = counter
                    #CurrentNode.neighbors[i].h = temp

                temp2 = CurrentNode.g + 1
                if CurrentNode.neighbors[i].g > temp2:
                    CurrentNode.neighbors[i].g = CurrentNode.g + 1
                    CurrentNode.neighbors[i].Parent = CurrentNode
                    if CurrentNode.neighbors[i] in OpenSet:
                        MinHeap.deleteNode(OpenSet, CurrentNode.neighbors[i])
                    CurrentNode.neighbors[i].f = CurrentNode.neighbors[i].g + CurrentNode.neighbors[i].h 
                    MinHeap.push(OpenSet, CurrentNode.neighbors[i],window)


def computePath(CurrentNode,OpenSet,ClosedSet,EndNode,StartNode,window,counter,forward,colorChange,breakBig): 
    peekHeap = MinHeap.peek(OpenSet)
    temp = heuristic(peekHeap,EndNode)
    temp +=peekHeap.g
    while EndNode.g > temp and EndNode not in ClosedSet:

        #Remove smallest f value from OpenSet     
        #True is larger g value, false is smaller                  
        CurrentNode = MinHeap.pop(OpenSet,breakBig)

        #Add State to ClosedSet
        ClosedSet.append(CurrentNode)
        
        
        #Color the expanded Node
        if ClosedSet[ClosedSet.__len__()-1] is not None: 
            if forward == True and colorChange ==0:
                ClosedSet[ClosedSet.__len__()-1].draw(window, 'red')
                #update(100000)
                #StartNode.draw(window, 'light green')
                #update(100000)
            elif forward == True and colorChange ==1:
                ClosedSet[ClosedSet.__len__()-1].draw(window, 'dark red')
                #update(100000)
                #StartNode.draw(window, 'light green')
                #update(100000)
        else:
            break

        #Check each action
        for i in range(len(CurrentNode.neighbors)):
            if CurrentNode.neighbors[i].isBlocked == False:
                if CurrentNode.neighbors[i] in ClosedSet:
                    continue
                    
                if CurrentNode.neighbors[i].s < counter:
                    CurrentNode.neighbors[i].g = 20000
                    CurrentNode.neighbors[i].s = counter
                    #CurrentNode.neighbors[i].h = temp

                temp2 = CurrentNode.g + 1
                if CurrentNode.neighbors[i].g > temp2:
                    CurrentNode.neighbors[i].g = CurrentNode.g + 1
                    CurrentNode.neighbors[i].Parent = CurrentNode
                    if CurrentNode.neighbors[i] in OpenSet:
                        MinHeap.deleteNode(OpenSet, CurrentNode.neighbors[i])
                    CurrentNode.neighbors[i].f = CurrentNode.neighbors[i].g + CurrentNode.neighbors[i].h 
                    MinHeap.push(OpenSet, CurrentNode.neighbors[i],window)
                    
def AdaptiveAstar(grid,window,StartNode,EndNode):
    
    #create openset and closedset
    OpenSet=[]
    ClosedSet=[]

    counter = 0
    deltaCounter = []
    deltaCounter.append(counter)
    numNodesExpanded = 0

    #Reset grid Values
    for j in range(cols):
        for i in range(rows):
            grid[i][j].s = 0
            grid[i][j].f = None
            grid[i][j].g = None
            temp = heuristic(grid[i][j],EndNode)
            grid[i][j].h = temp
            grid[i][j].Parent = None


    colorChange = 0
    StartNode.g=0   
    StartNode.h=heuristic(StartNode,EndNode)
    StartNode.f=StartNode.h+StartNode.g
    CurrentNode = StartNode
    
    
    while CurrentNode != EndNode:

        initializeState(CurrentNode,counter,EndNode,deltaCounter)
        initializeState(EndNode,counter,EndNode,deltaCounter)
        
        
        #Initialize current Node
        CurrentNode.g = 0
        #CurrentNode.s = counter

        #EndNode.s = counter
        #EndNode.g = 20000

        OpenSet.clear()
        ClosedSet.clear()

        #Insert startnode into openset
        MinHeap.push(OpenSet, CurrentNode,window)

        computePathAdaptive(CurrentNode,OpenSet,ClosedSet,EndNode,CurrentNode,window,counter,colorChange,grid,deltaCounter)
        update(100000)
        #for i in range(ClosedSet.__len__()-1):
            #grid[ClosedSet[i].horizontal][ClosedSet[i].vertical].h = EndNode.g - ClosedSet[i].g
            #ClosedSet[i].h = EndNode.g - ClosedSet[i].g
    
        if MinHeap.isEmpty(OpenSet) == True:
            return False,ClosedSet.__len__()

        previous=EndNode
        previous.draw(window,"purple")
        update(100000)

        while previous.Parent != CurrentNode:  
            previous=previous.Parent 
            previous.draw(window,"purple")
            update(100000)           
            
        CurrentNode = previous
        CurrentNode.draw(window,'blue')
        update(100000)

        #update g and h values for new starting node
        if CurrentNode != EndNode:
            initializeState(CurrentNode,counter,EndNode,deltaCounter)
            if CurrentNode.g + CurrentNode.h < previous.g:
                CurrentNode.h = EndNode.g - CurrentNode.g
            deltaCounter.append(deltaCounter[counter] + CurrentNode.h) 
        else:
            deltaCounter.append(deltaCounter[counter]) 


        EndNode.draw(window,'Orange')
        update(100000)

        numNodesExpanded += ClosedSet.__len__()
        if colorChange == 1:
            colorChange = 0
        else:
            colorChange = 1
        
        counter +=1

    avgNumNodesExpanded = numNodesExpanded/50
    return True,avgNumNodesExpanded

def initializeState(state,counter,EndNode,deltaCounter):
    #Init state.g if it hasnt been generated by current search or by any search
    if state.s != counter and state.s !=0:
        #update heuristic
        if state.g + state.h < state.g:
            state.h = EndNode.g - state.g
        state.h = state.h - deltaCounter[counter] - deltaCounter[state.s]
        H = heuristic(state,EndNode)
        state.h = max(state.h, H)
        state.g = 20000
    elif state.s == 0:
        H = heuristic(state,EndNode)
        state.g = 20000
        state.h = H
    state.s = counter

def computePathAdaptive(CurrentNode,OpenSet,ClosedSet,EndNode,StartNode,window,counter,colorChange,grid,deltaCounter): 
    peekHeap = MinHeap.peek(OpenSet)
    temp = heuristic(peekHeap,EndNode)
    
    while EndNode.g > peekHeap.g + temp and EndNode not in ClosedSet:
        #MinHeap.heapSort(OpenSet)
        #Remove smallest f value from OpenSet                       
        CurrentNode = MinHeap.pop(OpenSet,True)
        if CurrentNode is None:
            return
        #temp2 = heuristic(CurrentNode,EndNode)
        #CurrentNode.h=temp2
        
        
        #Add State to ClosedSet
        ClosedSet.append(CurrentNode)
        
        #Color the expanded Node
        if ClosedSet[ClosedSet.__len__()-1] is not None: 
                if colorChange == 0:
                    ClosedSet[ClosedSet.__len__()-1].draw(window, 'yellow')
                    #update(100000)
                    #StartNode.draw(window, 'pink')
                    #update(100000)
                elif colorChange == 1:
                    ClosedSet[ClosedSet.__len__()-1].draw(window, 'beige')
                    #update(100000)
                    #StartNode.draw(window, 'pink')
                    #update(100000)
        else:
            break

        #Check each action
        for i in range(len(CurrentNode.neighbors)):
            if CurrentNode.neighbors[i].isBlocked == False:
                if CurrentNode.neighbors[i] in ClosedSet:
                    continue
                    
                initializeState(CurrentNode.neighbors[i],counter,EndNode,deltaCounter)

                tempg = CurrentNode.g + 1
                if CurrentNode.neighbors[i].g > tempg :
                    CurrentNode.neighbors[i].g = CurrentNode.g + 1
                    CurrentNode.neighbors[i].Parent = CurrentNode
                    if CurrentNode.neighbors[i] in OpenSet:
                        MinHeap.deleteNode(OpenSet, CurrentNode.neighbors[i])

                    grid[CurrentNode.neighbors[i].horizontal][CurrentNode.neighbors[i].vertical].f = grid[CurrentNode.neighbors[i].horizontal][CurrentNode.neighbors[i].vertical].g + grid[CurrentNode.neighbors[i].horizontal][CurrentNode.neighbors[i].vertical].h
                    #CurrentNode.neighbors[i].f = CurrentNode.neighbors[i].g + CurrentNode.neighbors[i].h    
                    MinHeap.push(OpenSet, CurrentNode.neighbors[i],window)


if __name__ == "__main__":
    main()
    