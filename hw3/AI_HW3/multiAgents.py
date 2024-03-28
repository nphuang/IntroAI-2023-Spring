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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        """
        Using recursion to compute the minimax values of each state. The minimax function takes state, depth, agent index as arguments, 
        and returns minimax value of the state. If the state is a terminal state or the maximum depth has been reached, the function 
        returns the evaluation of the state. Otherwise, the function computes the minimax value for the current agent by either 
        maximizing or minimizing the values of the next agent's actions, depending on the current agent is pacman or a ghost. 
        Finally, the function returns the computed minimax value.
        """
        def minimax(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            if agentIndex == 0:  # maximize for pacman
                v = float('-inf')
                for action in state.getLegalActions(agentIndex):
                    v = max(v, minimax(state.getNextState(agentIndex, action), depth, agentIndex + 1))
                return v
            else:  # minimize for ghost
                v = float('inf')
                for action in state.getLegalActions(agentIndex):
                    if agentIndex == state.getNumAgents() - 1:  # next agent is pacman, depth + 1
                        v = min(v, minimax(state.getNextState(agentIndex, action), depth + 1, 0))
                    else:  #move to next ghost 
                        v = min(v, minimax(state.getNextState(agentIndex, action), depth, agentIndex + 1))
                return v
        legalMoves = gameState.getLegalActions()  # get all legal actions
        # get the score for each legal action by running minimax on the resulting state        
        scores = [minimax(gameState.getNextState(0, action), 0, 1) for action in legalMoves]
        # find the best score and choose a random action with the best score        
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
        maxValue function returns the maximum value achievable by the current agent in the current state, 
        while minValue function returns the minimum value achievable by the next agent.
        The main loop iterates through all legal actions of the current agent and calculates the value 
        of each action using the minValue function, and updates the best action accordingly. It uses 
        alpha-beta pruning to avoid exploring paths that will not lead to a better outcome.
        Finally, return the best action.
        """
        def maxValue(state, agentIndex, depth, alpha, beta):
            v = float("-inf")
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions or depth == self.depth:
                return self.evaluationFunction(state)
            for action in legalActions:
                nextState = state.getNextState(agentIndex, action)
                v = max(v, minValue(nextState, agentIndex + 1, depth, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def minValue(state, agentIndex, depth, alpha, beta):
            v = float("inf")
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions or depth == self.depth:
                return self.evaluationFunction(state)
            for action in legalActions:
                nextState = state.getNextState(agentIndex, action)
                if agentIndex == state.getNumAgents() - 1:
                    v = min(v, maxValue(nextState, 0, depth + 1, alpha, beta))
                else:
                    v = min(v, minValue(nextState, agentIndex + 1, depth, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        legalActions = gameState.getLegalActions()
        bestAction = None
        v = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        for action in legalActions:
            nextState = gameState.getNextState(0, action)
            nextValue = minValue(nextState, 1, 0, alpha, beta)
            if nextValue > v:
                v = nextValue
                bestAction = action
            if v > beta:
                return bestAction
            alpha = max(alpha, v)
        return bestAction
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
        maxValue function recursively calculates the maximum value of a given state by iterating over 
        all legal actions of the pacman player and calling the expectValue function on the resulting next state. 
        The expectValue function calculates the expected value of a given state by iterating over all legal 
        actions of the current agent and recursively calling either maxValue or expectValue on the resulting next state. 
        And returns the average of the resulting values, weighted by probability of each action. 
        Finally, the agent selects the action with the highest expected score and returns.
        """
        def maxValue(state, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            v = float('-inf')
            for action in state.getLegalActions(0):
                v = max(v, expectValue(state.getNextState(0, action), depth, 1))
            return v

        def expectValue(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            v = 0
            legalActions = state.getLegalActions(agentIndex)
            p = 1.0 / len(legalActions)
            for action in legalActions:
                if agentIndex == state.getNumAgents() - 1:
                    v += p * maxValue(state.getNextState(agentIndex, action), depth + 1)
                else:
                    v += p * expectValue(state.getNextState(agentIndex, action), depth, agentIndex + 1)
            return v
        legalMoves = gameState.getLegalActions()
        scores = []
        for action in legalMoves:
            score = expectValue(gameState.getNextState(0, action), 0, 1)
            scores.append(score)

        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    """
    The function calculates a score for a pacman game state based on the distance and proximity of ghosts to pacman, 
    the distance to the closest remaining food, and the number of remaining capsules. 
    The function prioritizes getting closer to food while avoiding ghosts, while also 
    taking into account the remaining capsules on the board.
    """
    pPos = currentGameState.getPacmanPosition()
    gDist = 0
    gProximity = 0
    for gState in currentGameState.getGhostPositions():
        dist = util.manhattanDistance(pPos, gState)
        gDist += dist
        if dist <= 1:
            gProximity += 1
     
    foodList = currentGameState.getFood().asList()
    minfoodList = min([util.manhattanDistance(pPos, foodPos) for foodPos in foodList], default=0)

    capsuleNum = len(currentGameState.getCapsules())
    return currentGameState.getScore() - (1 / (gDist+1)) - gProximity + (1 / (minfoodList+1)) - capsuleNum
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
