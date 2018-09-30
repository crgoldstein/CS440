
# coding: utf-8

# # Assignment 2: Iterative-Deepening Search

# Claire Goldstein

# ## Overview

# Implemented the iterative-deepening search algorithm as discussed in our Week 2 lecture notes and as shown in figures 3.17 and 3.18 in our text book. Apply it to the 8-puzzle and a Tree Structure . 

# In[129]:


startState = [1, 0, 3, 4, 2, 5, 6, 7, 8]


# # printState_8p(state)
#     this method prings out our 3X3 grid for playing the the 8 puzzel game
#     

# In[130]:


import copy

def printState_8p(startState):
    X = copy.copy(startState)
    X[X.index(0)] ="-"
    print(X[0],"",X[1],"",X[2],"")
    print(X[3],"",X[4],"",X[5],"")
    print(X[6],"",X[7],"",X[8],"")
    


# # printPath_8p(state)
#     this method prings out our 3X3 grid for each move that our search algorithims found on its way to the Goal state
#     

# In[131]:


def printPath_8p(startState, goalState, path): 
    for p in path:
        print("To")
        printState_8p(p)
    


# # findBlank_8p(state)
#    return the row and column index for the location of the blank (the 0 value).

# In[132]:


def findBlank_8p(startState):
   
    index = startState.index(0)

    if(index >=0 and index<3):
        return (0,index)
        
    if(index >=3 and index<6):
        index=index-3
        return (1,index)
    
    if(index >=6 and index<9):
        index=index-6
        return (2,index)
        


# # actionsF_8p(state)
#     Returns a list of up to four valid actions that can be applied in state. 
#     Return them in the order left, right, up, down, though only if each one is a valid action.

# In[133]:


def actionsF_8p(startState):
    returnList=[]
    blank = findBlank_8p(startState)
    
    # Left or Right 
    if blank[1] == 2 or blank[1] == 1:
        returnList.append("left")
    if blank[1] == 0 or blank[1] == 1:
        returnList.append("right")
   # Up or Down 
    if blank[0] == 2 or blank[0] == 1:
        returnList.append("up")
    if blank[0] == 0 or blank[0] == 1:
        returnList.append("down")
        
    return returnList


# # takeActionF_8p(startState, move):
#     return the state that results from applying action in state.
#     

# In[134]:


def takeActionF_8p(startState, move):
    X = copy.copy(startState)
    index = X.index(0)
    if (move == 'left'):
        X[index], X[index-1] = X[index-1], X[index]
    if (move == 'right'):
        X[index], X[index+1] = X[index+1], X[index]
    if (move == 'up'):
        X[index], X[index-3] = X[index-3], X[index]
    if (move == 'down'):
        X[index], X[index+3] = X[index+3], X[index]
    return X;


# In[135]:


printState_8p(takeActionF_8p(startState, 'down'))


# In[136]:


goalState = takeActionF_8p(startState, 'down')


# In[137]:


newState = takeActionF_8p(startState, 'down')


# In[138]:


newState == goalState


# In[139]:


startState


# The reason that we are defining all of these methods because they define the 8 Puzzle. To solve the puzzle there are specific rules to solve the puzzle. Our algorithms below are defined in terms of functions. The reason that we do this is so that we can reuse the search algorithm. We want to be able to use these algorithms not only with the 8-puzzel but with other search problems such as finding the shortest path through a tree. To find a path to the goal for any specific problem we would need to define a possible actions function a take action function and a start and a end goal. 
# 

# # depthLimitedSearch 
#     This algorithm helps to preserve space and time complexity by using the same logic as breath first search but instead of having all possible levels explored.
#     Depth Limited Search helps to minimize the amount of time this searching happens 
#     

# In[140]:


def depthLimitedSearch(state, goalState, actionsF, takeActionF, depthLimit):
    if state == goalState :
        return []
    if depthLimit == 0:
        return 'cutoff'
    cutoffOccurred = False
    for action in actionsF(state):
        childState = takeActionF(state, action)
        result = depthLimitedSearch(childState, goalState, actionsF, takeActionF, depthLimit-1)
        if result == 'cutoff':
            cutoffOccurred = True
        elif result != 'failure':
            #Add childState to front of partial solution path, in result, returned by depthLimitedSearch
            result.insert(0, childState)
            return result
        
    if cutoffOccurred == True:
        return 'cutoff'
    else:
        return 'failure'


# # iterativeDeepeningSearch 
#      This algorithm builds off the Depth Limited Search. It also helps to preserve space and time complexity by using the same logic as breath first search.
#      Where Iterative Deepening Search expands is that it looks though all of the possible ranges up to the given depth provided as the parameter. 
#     

# In[141]:


def iterativeDeepeningSearch(startState, goalState, actionsF, takeActionF, maxDepth):
    for depth in range(maxDepth):
        result = depthLimitedSearch(startState, goalState, actionsF, takeActionF, depth)
        if result == 'failure':
            return 'failure'
        if result != 'cutoff':
            result.insert(0, startState) #Add startState to front of solution path, in result, returned by depthLimitedSearch 
            return result
    return 'cutoff'


# In[142]:


path = depthLimitedSearch(startState, goalState, actionsF_8p, takeActionF_8p, 3)
path


# Notice that `depthLimitedSearch` result is missing the start state.  This is inserted by `iterativeDeepeningSearch`.
# 
# But, when we try `iterativeDeepeningSearch` to do the same search, it finds a shorter path!

# In[143]:


path = iterativeDeepeningSearch(startState, goalState, actionsF_8p, takeActionF_8p, 3)
path


# Also notice that the successor states are lists, not tuples.  This is okay, because the search functions for this assignment do not

# In[144]:


startState = [4, 7, 2, 1, 6, 5, 0, 3, 8]
path = iterativeDeepeningSearch(startState, goalState, actionsF_8p, takeActionF_8p, 3)
path


# In[145]:


startState = [4, 7, 2, 1, 6, 5, 0, 3, 8]
path = iterativeDeepeningSearch(startState, goalState, actionsF_8p, takeActionF_8p, 5)
path


# Humm...maybe we can't reach the goal state from this state.  We need a way to randomly generate a valid start state.

# In[146]:


import random


# In[147]:


random.choice(['left', 'right'])


# In[148]:


def randomStartState(goalState, actionsF, takeActionF, nSteps):
    state = goalState
    for i in range(nSteps):
        state = takeActionF(state, random.choice(actionsF(state)))
    return state


# In[149]:


goalState = [1, 2, 3, 4, 0, 5, 6, 7, 8]
randomStartState(goalState, actionsF_8p, takeActionF_8p, 10)


# In[150]:


startState = randomStartState(goalState, actionsF_8p, takeActionF_8p, 50)
startState


# In[151]:


path = iterativeDeepeningSearch(startState, goalState, actionsF_8p, takeActionF_8p, 20)
path


# Let's print out the state sequence in a readable form.

# In[152]:


for p in path:
    printState_8p(p)
    print()


# Here is one way to format the search problem and solution in a readable form.

# In[153]:


printPath_8p(startState, goalState, path)


# Implement a second search problem of your choice. 
#     Apply your `iterativeDeepeningSearch` function to it.
# 
# 
# # Test 1 from A1:

# In[169]:


successors = {'a':  ['b', 'c', 'd'],
              'b':  ['e', 'f', 'g'],
              'c':  ['a','h', 'i'],
              'd':  ['j', 'z'],
              'e':  ['k', 'l'],
              'g':  ['m'],
              'k':  ['z']}
successors


# In[170]:


import copy

def successorsf(state):
    return copy.copy(successors.get(state, []))
successorsf('a')


# In[171]:


def takeActionSuccessorsf(state, action):
    if action in successorsf(state):
        return action

takeActionSuccessorsf ('a','b')   


# Now since we have defined a new functions that show us our possible actions and and the action we want to take we can run our `depthLimitedSearch` and `iterativeDeepeningSearch` to see our optimal path thorough our tree. 
# 

# In[172]:


print('path from a to a is', depthLimitedSearch('a', 'b', successorsf, takeActionSuccessorsf ,0))
print('path from a to a is', depthLimitedSearch('a', 'b', successorsf, takeActionSuccessorsf ,1))


# In[173]:


print('path from a to a is', iterativeDeepeningSearch('a', 'b', successorsf, takeActionSuccessorsf ,0))
print('path from a to b is', iterativeDeepeningSearch('a', 'b', successorsf, takeActionSuccessorsf ,2))


# With this simple tree example we can see excactly how iterativeDeepeningSearch is acting like BFS based on levels of the Tree. We see that when our depth is set to 0, we do not get the answer, we just get 'cutoff'. When we expand the depth we can look at we see the correct answers. 

# In[159]:


print('path from a to a is', iterativeDeepeningSearch('a', 'z', successorsf, takeActionSuccessorsf ,0))
print('path from a to a is', iterativeDeepeningSearch('a', 'z', successorsf, takeActionSuccessorsf , 2))
print('path from a to a is', iterativeDeepeningSearch('a', 'z', successorsf, takeActionSuccessorsf , 9))


# Now we see how the iterativeDeepeningSearch algorithm returns the optimal path becouse it is looking for the correct depth that the path is taking. 

# In[160]:


get_ipython().run_line_magic('run', '-i A2grader.py')

