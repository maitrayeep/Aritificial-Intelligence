# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
	
	score = successorGameState.getScore()	
	
	foodlist = newFood.asList()
        foodDistance = []
	noOfNewFood = successorGameState.getNumFood()

	if successorGameState.isWin():	
            return float("inf")
	      
        if newPos in successorGameState.getCapsules():
            score += 10

        if action == Directions.STOP:
            score -= 5
	
	for food in foodlist:
            foodDistance.append(util.manhattanDistance(food,newPos))
	score -= min(foodDistance)

        for ghost in newGhostStates:
            ghostDistance = util.manhattanDistance(ghost.getPosition(), newPos)
            if(ghostDistance >2):
	    	score += ghostDistance

        score -= 10*noOfNewFood

        
        return score
	
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
	
	def minimiser(gameState, depth, agent):
		min_value = float('inf') 
		
		if(gameState.isWin() or gameState.isLose() or (depth == 0)):
			return self.evaluationFunction(gameState)
		
		if(agent == noOfGhosts):
			for action in gameState.getLegalActions(agent):
				value = maximiser(gameState.generateSuccessor(agent,action),depth-1,0)
				min_value = min(min_value,value)
		else:
			for action in gameState.getLegalActions(agent):
				value = minimiser(gameState.generateSuccessor(agent,action),depth,agent+1)
		 		min_value = min(min_value,value)
		return min_value	
	
	def maximiser(gameState, depth, agent):
		max_value = -(float('inf')) 

		if(gameState.isWin() or gameState.isLose() or (depth == 0)):
			return self.evaluationFunction(gameState)

		for action in gameState.getLegalActions(agent):
			value = minimiser(gameState.generateSuccessor(0,action),depth,1)
			max_value = max(max_value,value)
		return max_value
	
		
	noOfGhosts = gameState.getNumAgents() - 1
	actionAndValue = []		
	
	for action in gameState.getLegalActions(0):
		actionAndValue.append((minimiser(gameState.generateSuccessor(0,action),self.depth,1),action))
	
	action = max(actionAndValue)
	return action[1]

		
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

	def minimiser(gameState, depth, agent, alpha_value, beta_value):
		min_value = float('inf') 

		if(gameState.isWin() or gameState.isLose() or (depth == 0)):
			return self.evaluationFunction(gameState)
		
		if(agent == noOfGhosts):
			for action in gameState.getLegalActions(agent):
				value = maximiser(gameState.generateSuccessor(agent,action),depth-1,0,alpha_value, beta_value)
				min_value = min(min_value,value)
				if(alpha_value > min_value):
					return min_value
				beta_value = min(min_value,beta_value)
		else:
			for action in gameState.getLegalActions(agent):
				value = minimiser(gameState.generateSuccessor(agent,action),depth,agent+1,alpha_value, beta_value)
				min_value = min(min_value,value)
		 		if(alpha_value > min_value):
					return min_value
				beta_value = min(min_value,beta_value)	
		return min_value	

	def maximiser(gameState, depth, agent, alpha_value, beta_value):
				
		max_value = -(float('inf')) 
		
		if(gameState.isWin() or gameState.isLose() or (depth == 0)):
			return self.evaluationFunction(gameState)

		for action in gameState.getLegalActions(agent):
			value = minimiser(gameState.generateSuccessor(0,action),depth,1, alpha_value, beta_value)
			max_value = max(max_value, value)
			if(beta_value < max_value):
				return max_value
			alpha_value = max(max_value,alpha_value)
	
		return max_value		

	noOfGhosts = gameState.getNumAgents() - 1
	actionAndValue = []
	
	alpha_value = -(float('inf'))
	beta_value = float('inf')
	
	for action in gameState.getLegalActions(0):
		value = minimiser(gameState.generateSuccessor(0,action),self.depth,1,alpha_value,beta_value)
		actionAndValue.append((value,action))
		if(beta_value<value):
			return action
		alpha_value = max(value,alpha_value)
		
	action = max(actionAndValue)
	return action[1]

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

	def expecti(gameState, depth, agent):
		 
		value = 0
		if(gameState.isWin() or gameState.isLose() or (depth == 0)):
			return self.evaluationFunction(gameState)
		
		if(agent == noOfGhosts):
			for action in gameState.getLegalActions(agent):
				value += maximiser(gameState.generateSuccessor(agent,action),depth-1,0)
		else:
			for action in gameState.getLegalActions(agent):
				value += expecti(gameState.generateSuccessor(agent,action),depth,agent+1)
		return (value/len(gameState.getLegalActions(agent)))	
	
	def maximiser(gameState, depth, agent):
		max_value = -(float('inf')) 

		if(gameState.isWin() or gameState.isLose() or (depth == 0)):
			return self.evaluationFunction(gameState)

		for action in gameState.getLegalActions(agent):
			value = expecti(gameState.generateSuccessor(0,action),depth,1)
			max_value = max(max_value,value)
		return max_value
	
		
	noOfGhosts = gameState.getNumAgents() - 1
	actionAndValue = []		
	
	for action in gameState.getLegalActions(0):
		actionAndValue.append((expecti(gameState.generateSuccessor(0,action),self.depth,1),action))
	
	action = max(actionAndValue)
	return action[1]

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
	
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    
    score = currentGameState.getScore()	
	
    listOfFood = food.asList()
    foodDistance = []

    if currentGameState.isWin():	
       return float("inf")
    elif currentGameState.isLose():
	return -float("inf")

    if position in currentGameState.getCapsules():
       score += 100
    score -= 10*(len(currentGameState.getCapsules()))
	
    for food in listOfFood:
       foodDistance.append(util.manhattanDistance(food,position))
    score -= max(foodDistance)
    
       
    for ghost in ghostStates:
       ghostDistance = util.manhattanDistance(ghost.getPosition(), position)
       if(ghostDistance > 3):
	   score += ghostDistance
       else:
	   score -= 25*ghostDistance
        
    return score
		
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

