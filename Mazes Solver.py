# maze solver

import random, time 
import numpy as np
from IPython.display import clear_output

def actionName(action):
    if action == 0:
        return 'down'
    elif action == 1:
        return 'right'
    elif action == 2:
        return 'up'
    elif action == 3:
        return 'left'


def check(state, action):
    if (state == 0 and action == 2) or \
       (state == 0 and action == 5) or \
       (state == 1 and action == 1) or \
       (state == 1 and action == 3) or \
       (state == 2 and action == 3) or \
       (state == 2 and action == 5) or \
       (state == 3 and action == 1) or \
       (state == 3 and action == 3) or \
       (state == 3 and action == 5) or \
       (state == 4 and action == 2) or \
       (state == 5 and action == 3) or \
       (state == 5 and action == 4) or \
       (state == 6 and action == 1):
    #    (state == 4 and action == 5) or \
    #    (state == 5 and action == 5) or \
        return int(state * 7 + action) , True , -5
    elif (state == 4 and action == 4) :
        return int(state * 7 + action) , True , 1
    else:
        return int(state * 7 + action) , False , 0

def step(state, action):
    if(state%7 == 0 and action == 3):
        return 0 , True , -5
    elif(state<7 and action == 2):
        return 0 , True ,-5
    elif(state>41 and action == 0):
        return 0 , True , -5
    if((state+1)%7 == 0 and action == 1):
        return 0 , True , -5
    elif(action == 0):
        state += 7
    elif(action == 1):
        state += 1
    elif(action == 2):
        state -= 7
    else:
        state -= 1
    action = state%7
    state = (state - action) /7
    return check(state, action)
    


states = 49
actions= 4


done = False
num_episodes = 100000
steps_per_episode = 30;
learning_rate = 0.1
discount_rate = 0.99
reward_all_episodes = [ ]
won_count = 0


q_table = np.zeros((states, actions))


exploration_rate = 1
min_exploration_rate = 0.01
max_exploration_rate = 1
exploration_decay_rate = 0.0001

for episode in range(num_episodes):
    won = 0
    done = False
    state = 0
    
    reward_per_episode = 0
    for one in range(steps_per_episode):
        if random.uniform(0,1) > exploration_rate:
            action = np.argmax(q_table[state, :])
        else:
            action = random.randrange(0,4)
        
        new_state, done, reward = step(state, action)
        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + \
             learning_rate * (reward + (discount_rate * np.max(q_table[new_state, : ])))
        state = new_state
        if reward == 1:
            reward_per_episode += reward
        if (reward == 1):
            won = 1
        else:
            won = 0
        if done:
            break;
    
    exploration_rate =  min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)
    reward_all_episodes.append(reward_per_episode)
    won_count += won 
rewards_per_thousand_episodes = np.split(np.array(reward_all_episodes) , num_episodes/10000)
count = 10000
print('********************************* Average Reward Per Thousand Episodes ********************\n')
for r in rewards_per_thousand_episodes:
    for one in r:
        if one == 1.0:
            one = 1
        else:
            one=0
    print(count, ": " , str(sum(r)))
    count += 10000
print("\n\n************     Q-table        ***********************************\n")
print(q_table)
print(won_count)


print("\n\n************    Playin        ***********************************\n")

for episode in range(1) : 
    state = 0
    done = False
    print('################  ' + str(episode + 1) +   '  #####################')
    time.sleep(1)

    for one in range(20) :
        clear_output(wait=True)
        time.sleep(0.3)
        action = np.argmax(q_table[state, :])
      
        new_state, done, reward = step(state, action)

        print(actionName(action))
        print(int((new_state - new_state%7)/7) , new_state%7)
        time.sleep(2)
        if done == True:
            clear_output(wait=True)
            if reward == 1:
                print("'########  you reached the goal  #############')")
            time.sleep(3)
            clear_output(wait=True)
            break;
        state = new_state
