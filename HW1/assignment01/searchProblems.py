# searchProblems.py
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
In searchProblems.py, you will implement generic search problems which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Actions, Directions


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

    def getNextStates(self, state):
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


class PositionSearchProblem(SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn=lambda x: 1, goal=(1, 1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None:
            self.startState = start

        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize

        if warn and (len(gameState.data.layout.goals) == 0):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes, DO NOT CHANGE!
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):  # @UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist)  # @UndefinedVariable

        return isGoal

    def getNextStates(self, state):
        """
        Returns next states, the actions they require, and a cost of 1.
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for display purposes
        self._expanded += 1  # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x, y))

        return cost


class CounterClockwiseFoodProblem(SearchProblem):
    """
    Q4:
    This search problem finds paths through all foods and final goal location of map layout

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState, goal=(1, 1)):
        """
        Stores the walls, pacman's starting position and foods.
        """
        self.goal = goal  # # DO NOT CHANGE; this attribute is read from the layout file.
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        self.foods = startingGameState.getFood().deepCopy()
        self._expanded = 0  # DO NOT CHANGE; Number of search nodes expanded

        """
        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:

        print self.goal
        print self.foods
        print self.walls
        """

        # Please add any code here which you would like to use
        # in initializing the problem, it's okey if you don't have any additional code
        "*** YOUR CODE HERE ***"
        self.start = (self.startingPosition, Directions.STOP, self.foods)

    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state space)
        """
        "*** YOUR CODE HERE ***"
        return self.start

    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        return (state[0] == self.goal) & (state[2].count() == 0)

    def getNextStates(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in searchProblems.py:
            For a given state, this should return a list of triples,
            (successor,action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """
        next_states = []
        x, y = state[0]
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # Add a next state to the next_states list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall, or hit a food:
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]
            #   hitsFood = self.foods[nextx][nexty]
            "*** YOUR CODE HERE ***"
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                next_food = state[2].copy()
                next_food[nextx][nexty] = False
                if state != self.start:
                    previous_action = state[1]
                    if previous_action != None:
                        if action == Directions.RIGHT[previous_action]: 
                            continue
                        if action == Directions.REVERSE[previous_action]:
                            continue
                        
                next_state = (nextx, nexty)
                cost = 1
                next_states.append(((next_state, action, next_food), action, cost))
        
        self._expanded += 1  # DO NOT CHANGE
        return next_states

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


class ScaryProblem(PositionSearchProblem):
    """
        This search problem finds paths through map layout while avoids dangerous zones

        You must select a suitable state space and successor function
    """

    def __init__(self, gameState, goal=(1, 1), start=None, warn=True, visualize=True):
        PositionSearchProblem.__init__(self, gameState, self.cost_function, goal, start, warn, visualize)
        self.ghosts = gameState.getGhostPositions()

        """
        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:

        print self.goal
        print self.walls
        print self.ghosts
        """

        # Please add any code here which you would like to use
        # in initializing the problem, it's okey if you don't have any additional code
        "*** YOUR CODE HERE ***"

    def cost_function(self, state):
        """
        Cost of entering this state, should return higher cost if state is in a dangerous zone

        :param state: tuple (x,y)
        :return: int
        """

        "*** YOUR CODE HERE ***"
        if not self.walls[state[0]][state[1]]:
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    for ghost in self.ghosts:
                        x, y = ghost
                        nextx, nexty = int(x + dx), int(y + dy)
                        if (state[0], state[1]) == (nextx, nexty):
                            return 10 # Ghosts neighbors cost
            return 1
        else:
            return 999999
    
    def getNextStates(self, state):
        next_states = PositionSearchProblem.getNextStates(self, state)
        forbidden_action_index = None
        for i in range(len(next_states)):
            for ghost in self.ghosts:
                if next_states[i][0] == ghost:
                    forbidden_action_index = i
        if forbidden_action_index != None:
            next_states.remove(next_states[forbidden_action_index])
        return next_states