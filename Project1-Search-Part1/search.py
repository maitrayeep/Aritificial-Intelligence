# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    """
     Variables used in the code:
    visited -> It stores a set of nodes which have been visited
    stack   -> A stack is used to get the nodes which are to be explored
    node    -> Every node popped from the stack is stored here to be access anywhere in the code.
    successor -> Each node's successor is stored in this
    
    FUNCTION:
    Every node is popped out from a stack and checked if its a goal state. If not, its successors are found and pushed over stack. While doing 	   this we add the action to reach the parent to that of the child. Thus, wherever we find a goal state we will have a complete path to reach 	   that goal node.  
    """
    visited = [];
    stack = util.Stack();
    stack.push((problem.getStartState(),[],0));
    
    while not stack.isEmpty():
	node = stack.pop();
        if(problem.isGoalState(node[0])): 
	   return node[1];
	if(node[0] not in visited):
	   visited.append(node[0]);
	   successors = problem.getSuccessors(node[0]);
	   for successor in successors:
		stack.push((successor[0],node[1]+[successor[1]],successor[2]));
    return None
		

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    """
     Variables used in the code:
    visited -> It stores a set of nodes which have been visited
    queue   -> A queue is used to get the nodes which are to be explored
    node    -> Every node popped from the stack is stored here to be access anywhere in the code.
    successor -> Each node's successor is stored in this
    
    FUNCTION:
    Every node is popped out from a queue and checked if its a goal state. If not, its successors are found and pushed over queue. While doing 	   this we add the action to reach the parent to that of the child. Thus, wherever we find a goal state we will have a complete path to reach 	   that goal node.  
    """
    visited = [];
    queue = util.Queue();
    queue.push((problem.getStartState(),[],0));
    
    while not queue.isEmpty():
	node = queue.pop();
        if(problem.isGoalState(node[0])): 
	   return node[1];
	if(node[0] not in visited):
	   visited.append(node[0]);
	   successors = problem.getSuccessors(node[0]);
	   for successor in successors:
		queue.push((successor[0],node[1]+[successor[1]],successor[2]));
    return None
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    """
    Variables used in the code:
    visited -> It stores a set of nodes which have been visited
    parent  -> It is used to store parent of each node. It is a dictionary storing in key,value pair.
    pqueue  -> A priority queue is used to store the nodes with a tuple having: coordinates, direction, cost and priority of the node  
    queue   -> A queue is used to get a path to the goal
    node    -> Every node popped from the priority queue is stored here to be access anywhere in the code.
    successor -> Each node's successor is stored in this
    newCost -> New cost of reaching the successor from the parent

    FUNCTION:
    
    The following function uses a priority queue to reach to the goal. When the queue is not empty, a node is popped out and checked if it is 
    the goal state. If not, its successors are found and pushed over the queue. Here, the cost needed to reach the successor is recalculated 	
    and attached to the each successor. Also, a dictionary is used to have track of every node's parent. If any successor node is already in    
    the queue, then it is updated if at all it has higher priority than the one currently in queue.
    
    """
    visited=set();
    parent = {};
    queue = util.Queue();
    pqueue = util.PriorityQueue();
    pqueue.push((problem.getStartState(),"",0),0);
    
    while not pqueue.isEmpty():
	node = pqueue.pop();
	
	if(problem.isGoalState(node[0])): 
	   print "goal", node;
	   while node[1]!="" :
                queue.push(node[1]);
		node = parent[node];
	   return queue.list;
        
        if(node[0] not in visited):
	   visited.add(node[0]);
	   for successor in problem.getSuccessors(node[0]):
		newCost = node[2]+successor[2];
		successor = (successor[0],successor[1],newCost);		
		if successor[0] not in visited:		
		    parent[successor] = node;
		pqueue.update(successor,newCost);
	   
    return None;
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """
    Variables used in the code:
    visited -> It stores a set of nodes which have been visited
    parent  -> It is used to store parent of each node. It is a dictionary storing in key,value pair.
    pqueue  -> A priority queue is used to store the nodes with a tuple having: coordinates, direction, cost and priority of the node  
    queue   -> A queue is used to get a path to the goal
    node    -> Every node popped from the priority queue is stored here to be access anywhere in the code.
    successor -> Each node's successor is stored in this
    newCost -> New cost of reaching the successor from the parent
    heuritic() -> Gives the heuristic to reach the node.

    FUNCTION
    
    The following function uses a priority queue to reach to the goal. When the queue is not empty, a node is popped out and checked if it is 
    the goal state. If not, its successors are found and pushed over the queue. Here, the cost needed to reach the successor is recalculated by 
    taking heuristics into consideration and attached to the each successor. Also, a dictionary is used to have track of every node's parent. 
    If any successor node is already in the queue, then it is updated if at all it has higher priority than the one currently in queue.  
    """
    visited= set();
    parent = {};
    start = problem.getStartState();
    queue = util.Queue();
    pqueue = util.PriorityQueue();
    pqueue.push((start,"",0),0);
    
    while not pqueue.isEmpty():
	node = pqueue.pop();
	if(problem.isGoalState(node[0])): 
	   while node[1]!="" :
                queue.push(node[1]);
		node = parent[node];
	   return queue.list;
        
	if(node[0] not in visited):
	   visited.add(node[0]);
	   for successor in problem.getSuccessors(node[0]):
		if successor[0] not in visited:	
		    newCost = node[2]+successor[2]+heuristic(successor[0],problem);
		    if(node is start):
			successor = (successor[0],successor[1],newCost);			    	
		    else:
	   		successor = (successor[0],successor[1],newCost-heuristic(node[0],problem));
		    parent[successor] = node;
		    pqueue.update(successor,successor[2]);
    return None;
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
