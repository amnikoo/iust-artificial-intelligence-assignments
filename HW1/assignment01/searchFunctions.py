import util
from game import Directions

UNREACHABLE_GOAL_STATE = [Directions.STOP]


def tinyMazeSearch(problem):
    """
    Run to get familiar with directions.
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    Run this function to get familiar with how navigations works using Directions enum.
    """

    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    to_goal_easy_directions = [s, s, w, s, w, w, s, w]
    return to_goal_easy_directions


def simpleMazeSearch(problem):
    """
    Q1:
    Search for the goal using right-hand or left-hand method explained in docs.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getNextStates(problem.getStartState())
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    actions = []
    current_state = start_state

    next_actions = []
    next_states = problem.getNextStates(current_state)
    for next_state, action, _ in next_states:
        next_actions.append(action)
    
    if Directions.NORTH in next_actions:
        if Directions.EAST not in next_actions:
            next_action = Directions.NORTH
        elif Directions.SOUTH not in next_actions:
            next_action = Directions.EAST
        elif Directions.WEST not in next_actions:
            next_action = Directions.SOUTH
        else:
            next_action = Directions.NORTH
    elif Directions.WEST in next_actions:
        next_action = Directions.WEST
    elif Directions.SOUTH in next_actions:
        next_action = Directions.SOUTH
    elif Directions.EAST in next_actions:
        next_action = Directions.EAST
    else:
        return UNREACHABLE_GOAL_STATE

    # Stick to wall, first.
    for i in range(9999):

        if problem.isGoalState(current_state):
            return actions
        
        next_states = problem.getNextStates(current_state)
        for next_state, action, _ in next_states:
            if action == next_action:
                current_state = next_state
                actions += [action]
            else:
                break
    
    next_actions = []
    for next_state, action, _ in next_states:
        next_actions.append(action)
    if Directions.WEST in next_actions:
        next_action = Directions.WEST
    elif Directions.SOUTH in next_actions:
        next_action = Directions.SOUTH
    elif Directions.EAST in next_actions:
        next_action = Directions.EAST

    # Go until reach goal while sticking to wall with right-hand
    for i in range(99999):
        
        if problem.isGoalState(current_state):
            return actions
        
        next_actions = []
        next_states = problem.getNextStates(current_state)
        for next_state, action, _ in next_states:
            next_actions.append(action)
        
        if Directions.RIGHT[next_action] in next_actions:
            next_action = Directions.RIGHT[next_action]
        elif next_action not in next_actions:
            next_action = Directions.LEFT[next_action]
        
        for next_state, action, _ in next_states:
            if action == next_action:
                current_state = next_state
                actions += [action]

    return UNREACHABLE_GOAL_STATE

    "*** YOUR EXPLANATION HERE***"
    """
    No, Because in this approach we always move while sticking to wall 
    if Goal is in the middle of layout (not near the wall) 
    then we can't reach goal.
    """


def dfs(problem):
    """
    Q2:
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal.
    Make sure to implement a graph search algorithm.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    actions = []
    current_depth = 0
    expanded_states = []

    fringe = util.PriorityQueue()
    fringe.update( (start_state, actions), current_depth )

    while not fringe.isEmpty():
        current_state, actions = fringe.pop()
        current_depth = -len(actions) # Priority is higher if priority is more negative (deeper nodes)

        if problem.isGoalState(current_state):
            return actions

        next_states = problem.getNextStates(current_state)

        for next_state, action, _ in next_states:
            if next_state not in expanded_states:
                fringe.update( (next_state, actions + [action] ), current_depth - 1)
                expanded_states.append(next_state)


    return UNREACHABLE_GOAL_STATE

    "*** YOUR EXPLANATION HERE***"
    """
    The approach is what we have expected from dfs.
    Pacman searches the deepest nodes in the search tree first 
    and checks all places in those branches and leaves.
    If Pacman reaches goal there, he doesn't need to check all places of the layout.
    If there is no path to goal, we heve an error.
    We solve it by saying Pacman to stop.
    """


def bfs(problem):
    """
    Q3:
    Search the shallowest nodes in the search tree first.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    actions = []
    current_depth = 0
    expanded_states = []

    fringe = util.PriorityQueue()
    fringe.update( (start_state, actions), current_depth )
    
    while not fringe.isEmpty():
        current_state, actions = fringe.pop()
        current_depth = len(actions) # Priority is higher if priority is lower (shallower nodes)
        
        if problem.isGoalState(current_state):
            return actions
        
        next_states = problem.getNextStates(current_state)
        
        for next_state, action, _ in next_states:
            if next_state not in expanded_states:
                fringe.update( (next_state, actions + [action]), current_depth + 1 )
                expanded_states.append(next_state)
        

    return UNREACHABLE_GOAL_STATE

    "*** YOUR EXPLANATION HERE***"
    """
    Bfs is optimal if action costs are all identical.
    If not bfs is not optimal for example the scary problem with non identical
    costs for ghosts areas.
    If we use bfs in this example we may move near ghosts and we may lose.
    """


def deadend(problem):
    """
    Q5: Search for all dead-ends and then go for goal state.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    actions = []
    deadends = []
    current_depth = 0
    expanded_states = []
    total_actions = []

    fringe = util.PriorityQueue()
    fringe.update( (start_state, actions), current_depth )
    
    # First find all deadends and go to them
    while not fringe.isEmpty():
        current_state, actions = fringe.pop()
        current_depth = len(actions) # Priority is higher if priority is lower (shallower nodes)
        
        next_states = problem.getNextStates(current_state)

        if len(next_states) == 1:
            if current_state not in deadends:
                deadends.append(current_state)
                total_actions += actions
                while not fringe.isEmpty():
                    fringe.pop()
                start_state = current_state
                actions = []
                current_depth = 0
                expanded_states = []
                fringe.update( (start_state, actions), current_depth )
                current_state, actions = fringe.pop()
                current_depth = len(actions)
                next_states = problem.getNextStates(current_state)
        
        for next_state, action, _ in next_states:
            if next_state not in expanded_states:
                fringe.update( (next_state, actions + [action]), current_depth + 1 )
                expanded_states.append(next_state)


    while not fringe.isEmpty():
        fringe.pop()
    actions = []
    current_depth = 0
    expanded_states = []
    fringe.update( (start_state, actions), current_depth )
    
    # Now go to goal
    while not fringe.isEmpty():
        current_state, actions = fringe.pop()
        current_depth = len(actions) # Priority is higher if priority is lower (shallower nodes)
        
        if problem.isGoalState(current_state):
            return total_actions + actions

        next_states = problem.getNextStates(current_state)
        
        for next_state, action, _ in next_states:
            if next_state not in expanded_states:
                fringe.update( (next_state, actions + [action]), current_depth + 1 )
                expanded_states.append(next_state)
    

    return UNREACHABLE_GOAL_STATE


def ucs(problem):
    """
    Q7: Search the node of least total cost first.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    actions = []
    current_cost = problem.cost_function(start_state)
    expanded_states = []

    fringe = util.PriorityQueue()
    fringe.update( (start_state, actions, current_cost), current_cost )

    while not fringe.isEmpty():
        current_state, actions, current_cost = fringe.pop()

        if current_state not in expanded_states:

            expanded_states.append(current_state)

            if problem.isGoalState(current_state):
                return actions

            next_states = problem.getNextStates(current_state)

            for next_state, action, _ in next_states:
                fringe.update( (next_state, actions+[action], 
                current_cost + problem.cost_function(next_state) ), 
                current_cost + problem.cost_function(next_state))


    return UNREACHABLE_GOAL_STATE

    "*** YOUR EXPLANATION HERE***"
    """
    If action costs are all identical, bfs and ucs are same.
    """
