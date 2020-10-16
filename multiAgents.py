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
        foods = newFood.asList()
        score = successorGameState.getScore()
        DisAmount = 0
        disArr = []
        disArrr = []

        for i in newGhostStates:
          posGhost = i.getPosition()
          disGhost = util.manhattanDistance(posGhost,newPos)
          disArrr.append(disGhost)
          
          

        for i in foods:
          distance = util.manhattanDistance(newPos,i)
          disArr.append(distance)
        if(len(disArr)!=0):
          score -= min(disArr)
        if(util.manhattanDistance(newPos,posGhost) <= 1):
            return -999999
        else:
          if(len(disArrr)!=0):
            score += min(disArrr)


        "*** YOUR CODE HERE ***"
        
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
        def minimax(state, depth, agent):
            
            #If we found the bottom nodes or we don't have any moves or we won or lost: Call evaluation function and return the result
            if depth == self.depth or state.getLegalActions(agent) == 0 or state.isWin() or state.isLose():            
                return (self.evaluationFunction(state), None)

            minfinity = float("-inf")
            val = minfinity
            #If agent is pacman
            if (agent is 0):
                for a in state.getLegalActions(agent):
                    (v1, a1) = minimax(state.generateSuccessor(agent, a), depth, (agent + 1) % state.getNumAgents())
                    #Find the maximum value
                    if(v1 > val):
                        val = v1
                        maxa = a
            #Return the value and the action from which we found max
            if val is not minfinity:
                return (val, maxa)  
 
            infinity = float("inf")
            val = infinity
            #If agent is ghost            
            if (agent is not 0):
                for a in state.getLegalActions(agent):
                    
                    #If it isn't the last ghost keep the same depth
                    if(((agent + 1) % state.getNumAgents()) is not 0):
                        (v1, a1) = minimax(state.generateSuccessor(agent, a), depth, (agent + 1) % state.getNumAgents())
                    #else if it is next_depth = depth + 1
                    else:
                        (v1, a1) = minimax(state.generateSuccessor(agent, a), depth + 1, (agent + 1) % state.getNumAgents())
                    #Find the minimum value
                    if(v1 < val):
                        val = v1
                        mina = a
                      
            #Return the value and the action from which we found min
            if val is not infinity:
                return (val, mina)
        
       
        return minimax(gameState, 0, 0)[1]
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
        def alpha_beta(state, depth, agent, A, B):
            
            #If we found the bottom nodes or we don't have any moves or we won or lost: Call evaluation function and return the result
            if depth == self.depth or state.getLegalActions(agent) == 0 or state.isWin() or state.isLose():            
                return (self.evaluationFunction(state), None)

            minfinity = float("-inf")
            val = minfinity
            #If agent is pacman
            if (agent is 0):
                for a in state.getLegalActions(agent):
                    (v1, a1) = alpha_beta(state.generateSuccessor(agent, a), depth, (agent + 1) % state.getNumAgents(), A, B)
                    
                    #Find the maximum value
                    if(v1 > val):
                        val = v1
                        maxa = a
                    A = max(A, val)

                    if B < A:
                        return (val, maxa)
                             
                        
            #Return the value and the action from which we found max
            if val is not minfinity:
                return (val, maxa)  
 
            infinity = float("inf")
            val = infinity
            #If agent is ghost            
            if (agent is not 0):
                for a in state.getLegalActions(agent):
                    #If it isn't the last ghost keep the same depth
                    if(((agent + 1) % state.getNumAgents()) is not 0):
                        (v1, a1) = alpha_beta(state.generateSuccessor(agent, a), depth, (agent + 1) % state.getNumAgents(), A, B)
                    #else if it is next_depth = depth + 1
                    else:
                        (v1, a1) = alpha_beta(state.generateSuccessor(agent, a), depth + 1, (agent + 1) % state.getNumAgents(), A, B)
                    
                    #Find the minimum value
                    if(v1 < val):
                        val = v1
                        mina = a
                    
                    B = min(B, val)

                    if B < A:
                        return (val, mina)
                    
                        
            #Return the value and the action from which we found min
            if val is not infinity:
                return (val, mina)
        
      
        
        return alpha_beta(gameState, 0, 0, float("-inf"), float("inf"))[1]
        

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
        def expectimax( curr_depth, agent_index, gameState):
          if agent_index >= gameState.getNumAgents():
              agent_index = 0
              curr_depth += 1
          
          if curr_depth == self.depth:
              return None, self.evaluationFunction(gameState)
          
          best_score, best_action = None, None
          if agent_index == 0:  
              for action in gameState.getLegalActions(agent_index):  
                  
                  next_game_state = gameState.generateSuccessor(agent_index, action)
                  _, score = expectimax(curr_depth, agent_index + 1, next_game_state)
                  
                  if best_score is None or score > best_score:
                      best_score = score
                      best_action = action
          else:  
              ghostActions = gameState.getLegalActions(agent_index)
              if len(ghostActions) is not 0:
                  prob = 1.0 / len(ghostActions)
              for action in gameState.getLegalActions(agent_index):  
                  next_game_state = gameState.generateSuccessor(agent_index, action)
                  _, score = expectimax(curr_depth, agent_index + 1, next_game_state)

                  if best_score is None:
                      best_score = 0.0
                  best_score += prob * score
                  best_action = action
          
          if best_score is None:
              return None, self.evaluationFunction(gameState)
          return best_action, best_score  
        action, score = expectimax(0, 0, gameState)  
        return action  
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    
    foodList = newFood.asList()
       
    score = currentGameState.getScore()
    foodDistances = []   
        
    ghostDistances = []
       
    
    for x in foodList: 
        foodDistances.append(manhattanDistance(newPos, x))
    
    for x in newGhostStates:
        ghostDistances.append(manhattanDistance(newPos, x.getPosition()))
        if x.scaredTimer > 0:
            score = score
        else:
            if len(newGhostStates) is not 0:
                score += min(ghostDistances) 
            if len(foodDistances) is not 0:
                score -= min(foodDistances) 
    
       
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

