
# coding: utf-8

# # A3: A\*, IDS, and Effective Branching Factor

# Claire Goldstein 

# For this assignment, implement the Recursive Best-First Search implementation of the A\* algorithm given in class.  Name this function `aStarSearch`. 
# 
# Include `iterativeDeepeningSearch` functions from A2 implemented with Node Class
# 
# 
# 
# Defined a new function named `ebf` that returns an estimate of the effective
# branching factor for a search algorithm applied to a search problem.
# 

# In[1346]:


class Node:
    def __init__(self, state, f=0, g=0 ,h=0):
        self.state = state 
        self.f = f # estimated cost of the solution path through node n
        self.g = g # the sum of the step costs so far from the start node to this node
        self.h = h # the sum of the step costs so far from the start node to this node
        
    def __repr__(self):
        return "Node(" + repr(self.state) + ", f=" + repr(self.f) +                ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"


# In[1347]:


global nodes
nodes = 0


# In[1389]:


def depthLimitedSearch(state, goalState, actionsF, takeActionF, depthLimit):
    #global nodes
    
    if state == goalState :
        return []
    if depthLimit == 0:
        return 'cutoff'
    cutoffOccurred = False

    for action in actionsF(state):
       # nodes += 1 
        childState,cost = takeActionF(state, action) #actionsF(state) returns [('b', 1), (NextState, cost)] can only take the nextState
        result = depthLimitedSearch(childState, goalState, actionsF, takeActionF, depthLimit-1)
        if result == 'cutoff':
            cutoffOccurred = True
        elif result != 'failure':
            result.insert(0, childState)
            return result
        
    if cutoffOccurred == True:
        return 'cutoff'
    else:
        return 'failure'
    
def iterativeDeepeningSearch(startState, goalState, actionsF, takeActionF, maxDepth):
    for depth in range(maxDepth):
        result = depthLimitedSearch(startState, goalState, actionsF, takeActionF, depth)
        if result == 'failure':
            return 'failure'
        if result != 'cutoff':
            result.insert(0, startState) #Add startState to front of solution path, in result, returned by depthLimitedSearch 
            return result
    return 'cutoff'   


# In[1388]:


def aStarSearch(startState, actionsF, takeActionF, goalTestF, hF):
    h = hF(startState)
    startNode = Node(state=startState, f=0+h, g=0, h=h)
    return aStarSearchHelper(startNode, actionsF, takeActionF, goalTestF, hF, float('inf'))


def aStarSearchHelper(parentNode, actionsF, takeActionF, goalTestF, hF, fmax):
    #global nodes
   
    
    if goalTestF(parentNode.state):
        return ([parentNode.state], parentNode.g)
    
    ## Construct list of children nodes with f, g, and h values
    actions = actionsF(parentNode.state)
    if not actions:
        return ("failure", float('inf'))
    children = []
    for action in actions:
        #nodes += 1 
        
        (childState,stepCost) = takeActionF(parentNode.state, action)
        h = hF(childState)
        g = parentNode.g + stepCost
        f = max(h+g, parentNode.f)
        childNode = Node(state=childState, f=f, g=g, h=h)
        children.append(childNode)
    while True:
        # find best child
        children.sort(key = lambda n: n.f) # sort by f value
        bestChild = children[0]
        if bestChild.f > fmax:
            return ("failure",bestChild.f)
        # next lowest f value
        alternativef = children[1].f if len(children) > 1 else float('inf')
        # expand best child, reassign its f value to be returned value
        result,bestChild.f = aStarSearchHelper(bestChild, actionsF, takeActionF, goalTestF,
                                            hF, min(fmax,alternativef))
        if result is not "failure":               
            result.insert(0,parentNode.state)      
            return (result, bestChild.f)
        
        


# Here is a simple example using our usual simple graph search.

# In[1350]:


def actionsF_simple(state):
    succs = {'a': ['b', 'c'], 'b':['a'], 'c':['h'], 'h':['i'], 'i':['j', 'k', 'l'], 'k':['z']}
    return [(s, 1) for s in succs.get(state, [])]

def takeActionF_simple(state, action):
    return action

def goalTestF_simple(state, goal):
    return state == goal

def h_simple(state, goal):
    return 1


# In[1351]:


actions = actionsF_simple('a')
actions


# In[1352]:


takeActionF_simple('a', actions[0])


# In[1353]:


goalTestF_simple('a', 'a')


# In[1354]:


h_simple('a', 'z')


# In[1355]:


iterativeDeepeningSearch('a', 'z', actionsF_simple, takeActionF_simple, 10)


# In[1356]:


aStarSearch('a',actionsF_simple, takeActionF_simple,
            lambda s: goalTestF_simple(s, 'z'),
            lambda s: h_simple(s, 'z'))


# # Effective Branching Factor

# In[1357]:


def ebf(nNodes, depth, precision=0.01):
    '''returns number of nodes expanded and depth reached during a search.'''
    if depth == 0 or nNodes ==1:
        return nNodes
    else :
        return ebfHELPER(1, nNodes, nNodes, depth, precision)
   

def ebfHELPER(low, high, nNodes, depth, precision): 
    mid  = (low + high)/2 
    guess = (1 - mid**(depth+1)) / (1 - mid)
      
    if abs(guess - nNodes) < precision :
        #print(abs(guess-nNodes))
        #print(mid)
        return mid 
        
    elif guess < nNodes  :
         return ebfHELPER(mid, high, nNodes, depth, precision)
                
    else:
         return ebfHELPER(low, mid, nNodes, depth, precision)
       


# In[1358]:


ebf(10, 3)


# In[1359]:


ebf(100, 12, 0.01)
#1.3034343719482422


# The smallest argument values should be a depth of 0, and 1 node.

# In[1360]:


ebf(1, 0)


# In[1361]:


ebf(2, 1)


# In[1362]:


ebf(2, 1, precision=0.000001)


# In[1363]:


ebf(200000, 5)


# In[1364]:


ebf(200000, 50)


# # Eight Tile Puzzel 
# 
# Apply `iterativeDeepeningSearch` and `aStarSearch` to several eight-tile sliding puzzle
# problems. For this you must include your implementations of these functions, from Assignment 2:
# 
#   * `actionsF_8p(state)`: returns a list of up to four valid actions that can be applied in `state`. With each action include a step cost of 1. For example, if all four actions are possible from this state, return [('left', 1), ('right', 1), ('up', 1), ('down', 1)].

# In[1365]:


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


def actionsF_8p(state):
    '''returns a list of up to four valid actions that can be applied in state.
    With each action include a step cost of 1. 
    For example, if all four actions are possible from this state, 
    return [('left', 1), ('right', 1), ('up', 1), ('down', 1)].'''
    returnList=[]
    blank = findBlank_8p(state)
   
    # Left or Right 
    if blank[1] == 2 or blank[1] == 1:
        returnList.append(('left',1))
    if blank[1] == 0 or blank[1] == 1:
        returnList.append(('right',1))
   # Up or Down 
    if blank[0] == 2 or blank[0] == 1:
        returnList.append(('up',1))
    if blank[0] == 0 or blank[0] == 1:
        returnList.append(('down',1))    
    return returnList
    


#  * `takeActionF_8p(state, action)`: return the state that results from applying `action` in `state` and the cost of the one step,
#   
# 

# In[1366]:


import copy

def takeActionF_8p(state, action): 
    '''return the state that results from applying action in state and the cost of the one step'''
    move, cost = action
    X = copy.copy(state)
    index = X.index(0)
    
    if (move == 'left'):
        X[index], X[index-1] = X[index-1], X[index]
        
    if (move == 'right'):
        X[index], X[index+1] = X[index+1], X[index]
        
    if (move == 'up'):
        X[index], X[index-3] = X[index-3], X[index]
        
    if (move == 'down'):
        X[index], X[index+3] = X[index+3], X[index]
          
    return (X,cost);


# plus the following function for the eight-tile puzzle:
# 
#   * `goalTestF_8p(state, goal)`
#   

# In[1367]:


def goalTestF_8p(state, goal):
    if state == goal :
        return True
    else :
        return False


# ## Heuristic Functions
# 
# For `aStarSearch` use the following two heuristic functions, plus one more of your own design, for a total of three heuristic functions.
# 
#   * `h1_8p(state, goal)`: $h(state, goal) = 0$, for all states $state$ and all goal states $goal$,
#   * `h2_8p(state, goal)`: $h(state, goal) = m$, where $m$ is the Manhattan distance that the blank is from its goal position,
#   * `h3_8p(state, goal)`: $h(state, goal) = ?$, that you define.  It must be admissible, and not constant for all states.

# In[1368]:


s = [2,1,3,5,4,0,6,7,8]
g = [1,2,3,4,5,6,7,8,0]


# # Simple heuristic 
# 

# In[1369]:


def h1_8p(state, goal):
    return 0;

h1_8p(s,g)


# # The Manhattan distance heuristic 
#     used for its simplicity and also because it is actually a pretty good underestimate on the number of moves required to bring a given board to the solution board. We simply compute the sum of the distances of each tile from where it belongs, completely ignoring all the other tiles.

# In[1370]:


def h2_8p(state, goal):
    """Heuristic for 8 puzzle: returns sum for each tile of manhattan
    distance between it's position in node's state and goal""" 
    distance = 0
    
    for i in state:
        position_difference = abs(goal.index(i) - state.index(i))
        if i is not 0:
            a = position_difference % 3
            b = position_difference / 3
            distance += a + int(b)

            if abs(goal.index(i) % 3 - state.index(i) % 3) == 2 and position_difference % 3 == 1:
                distance += 2
            
    return distance
  
h2_8p(s,g)


# # Claire's Heuritstic
#     My Heuritstic will add 1 if the element at a certian index is equal in the state and the goal. This will never  return a number higher than 9 there for it is immissable
#     

# In[1371]:


def h3_8p(state, goal):
    """Heuristic for 8 puzzle: 
        returns the number of tiles 'out of place'
        between a state and the goal"""
    h=0
    for i in goal:
        if (state[i] != goal[i]):
            h=h+1
    return h;
    
    
h3_8p(s,g)   


# In[1372]:


startState = [1,2,3,4,0,5,6,7,8] 
goal_0 = [1,2,3,4,0,5,6,7,8]
goal_1 = [1,2,3,4,5,8,6,0,7]
goal_2 =[1,0,3,4,5,8,2,6,7]


# # `iterativeDeepeningSearch` Testing 

# In[1373]:


print(iterativeDeepeningSearch(startState, goal_0, actionsF_8p, takeActionF_8p, 3),"\n")

print(iterativeDeepeningSearch(startState, goal_1, actionsF_8p, takeActionF_8p, 9),"\n")

print(iterativeDeepeningSearch(startState, goal_2, actionsF_8p, takeActionF_8p, 20),"\n")


# # `aStarSearch` Testing 

# ### goal_0 with h1_8p, h2_8p, and h3_8p

# In[1374]:


print(aStarSearch(startState, actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s, goal_0), lambda s: h1_8p(s, goal_0)),"\n")

print(aStarSearch(startState, actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s, goal_0), lambda s: h2_8p(s, goal_0)),"\n")

print(aStarSearch(startState, actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s, goal_0), lambda s: h3_8p(s, goal_0)),"\n")


# ### goal_1 with h1_8p, h2_8p, and h3_8p

# In[1375]:


print(aStarSearch(startState, actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s, goal_1), lambda s: h1_8p(s, goal_1)),"\n")

print(aStarSearch(startState, actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s, goal_1), lambda s: h2_8p(s, goal_1)),"\n")

print(aStarSearch(startState, actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s, goal_1), lambda s: h3_8p(s, goal_1)),"\n")


# ### goal_2 with h1_8p, h2_8p, and h3_8p

# In[1376]:


print(aStarSearch(startState, actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s, goal_2), lambda s: h1_8p(s, goal_2)),"\n")

print(aStarSearch(startState, actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s, goal_2), lambda s: h2_8p(s, goal_2)),"\n")

print(aStarSearch(startState, actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s, goal_2), lambda s: h3_8p(s, goal_2)),"\n")


# ## Comparison

# Compare their results by displayng
# solution path depth, number of nodes 
# generated, and the effective branching factor, and discuss the results.  Do this by defining the following function that prints the table as shown in the example below.
# 
#    - runExperiment(goalState1, goalState2, goalState3, [h1, h2, h3])
#    
# Define this function so it takes any number of $h$ functions in the list that is the fourth argument.

# Apply all four algorithms (`iterativeDeepeningSearch` plus `aStarSearch` with the three heuristic
# functions) to three eight-tile puzzle problems with start state
# 
# $$
# \begin{array}{ccc}
# 1 & 2 & 3\\
# 4 & 0 & 5\\
# 6 & 7 & 8
# \end{array}
# $$
# 
# and these three goal states.
# 
# $$
# \begin{array}{ccccccccccc}
# 1 & 2 & 3  & ~~~~ & 1 & 2 & 3  &  ~~~~ & 1 & 0 &  3\\
# 4 & 0 & 5  & & 4 & 5 & 8  & & 4 & 5 & 8\\
# 6 & 7 & 8 &  & 6 & 0 & 7  & & 2 & 6 & 7
# \end{array}
# $$

# Print a well-formatted table like the following.  Try to match this
# format. 
# 
#            [1, 2, 3, 4, 0, 5, 6, 7, 8]    [1, 2, 3, 4, 5, 8, 6, 0, 7]    [1, 0, 3, 4, 5, 8, 2, 6, 7] 
#     Algorithm    Depth  Nodes  EBF              Depth  Nodes  EBF              Depth  Nodes  EBF          
#          IDS       0      0  0.000                3     43  3.086               11 225850  2.954         
#         A*h1       0      0  0.000                3    116  4.488               11 643246  3.263         
#         A*h2       0      0  0.000                3     51  3.297               11 100046  2.733         
# 
# Of course you will have one more line for `h3`.
# 
# 
# 
# # Extra Credit
# Add a third column for each result (from running runExperiment) that is the number of seconds each search required. You may get the total run time when running a function by doing
# 
#  import time
# 
#  start_time = time.time()
# 
#  < do some python stuff >
# 
#  end_time = time.time()
#  print('This took', end_time - start_time, 'seconds.')

# In[1377]:


goalState1 = [1,2,3,4,0,5,6,7,8]
goalState2 = [1,2,3,4,5,8,6,0,7]
goalState3 = [1,0,3,4,5,8,2,6,7]


# In[1386]:


import time 

def runExperiment(goalState1, goalState2, goalState3, Hfuctions):
    global nodes
    nodes=0
    
    print('{:>9}{:^35}{:^35}{:^35}'.format(' ', str(goalState1), str(goalState2), str(goalState3)))
    print('{A:^10}{s:^5}{D:^7}{N:^7}{E:^7}{T:^7}{s:^5}{D:^7}{N:^7}{E:^7}{T:^7}{s:^5}{D:^7}{N:^7}{E:^7}{T:^7}'.format(s=' ' ,A='Algorithm', D='Depth', N='Nodes', E='EBF', T='Time'))
    
    #IDS
    print('{:<10}'.format('IDS'), end='')
    for goal in [goalState1, goalState2, goalState3]:
        
        start_time = time.time()
        idf =iterativeDeepeningSearch(startState, goal, actionsF_8p, takeActionF_8p, 12)
        end_time = time.time()
        
        idfNodes = nodes
        idfDepth = len(idf) - 1
        EBF = ebf(idfNodes,idfDepth)
        timeRun = end_time - start_time
        print('{s:^5}{D:^7}{N:^7}{E:^7.3f}{T:^7.3f}'.format(s=' ', D=idfDepth, N=idfNodes, E=EBF, T=timeRun), end='')
        nodes = 0   # reset nodes expanded for next search
    print('')  
       
    count =1
    for i in Hfuctions: 
        label = 'A*h'+str(count)
        print('{:<10}'.format(label), end='')
        for goal in [goalState1, goalState2, goalState3]: 
            start_time = time.time()
            a = aStarSearch(startState, actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s, goal), lambda s: i(s, goal))
            end_time = time.time() 
            

            aNodes= nodes
            nodes = 0
            aDepth= a[1] 
            EBF = ebf(aNodes,aDepth)
            timeRun= end_time - start_time
            print('{s:^5}{D:^7}{N:^7}{E:^7.3f}{T:^7.3f}'.format(s=' ', D=aDepth, N=aNodes, E=EBF, T=timeRun), end='')
        print()
        count +=1    
        
        


                
    


# In[1387]:


runExperiment(goalState1, goalState2, goalState3, [h1_8p, h2_8p, h3_8p])


# In[1390]:


get_ipython().run_line_magic('run', '-i A3grader.py')

