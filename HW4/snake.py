import numpy as np
from ple import PLE
from ple.games.snake import Snake
import random


def getReward(env, state, action):
    return(env.act(action))

agent = Snake(width=360, height=360)
Q = {}
gama = 0.9
alpha = 0.1
explore = 0.75

env = PLE(agent, fps=15, force_fps=False, display_screen=True)

env.init()

for i in range(100000):

    if explore != 0.25:
        if i % 30000 == 0:
            explore -= 0.25

    if env.game_over():
        env.reset_game()

    state = env.getGameState()
    
    del(state["snake_body_pos"])
    state["snake_head_x"] = int(state["snake_head_x"]/10)
    state["snake_head_y"] = int(state["snake_head_y"]/10)
    state["food_x"] = int(state["food_x"]/10)
    state["food_y"] = int(state["food_y"]/10)
    for i in range(len(state["snake_body"])):
        state["snake_body"][i] = int(state["snake_body"][i]/4)
    
    qState = str(state)
    actions = env.getActionSet()
    
    if qState not in Q:
        Q[qState] = {}
        for i in range(4):
            Q[qState][actions[i]] = 10
    
    # Explore
    if random.random() < explore:
        action = actions[np.random.randint(0, len(actions)-1)]
    # Exploit
    else:
        action = max(actions[0:4], key = lambda x: Q[qState][x])
     
    sample = getReward(env, state, action) + gama * max(Q[qState].values())
    Q[qState][action] = (1 - alpha) * Q[qState][action] + alpha * sample        
    
    