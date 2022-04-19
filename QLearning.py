#Harris Collier, Jack Valladares

import numpy

# Different methods of the Q-Learning program
# s(playerPose + applePose + size + trail) = state of the current position relative to the apple and tail
# act(s) = best action so far given s
# rew = instant reward of taking this step
# s'(s, act) = new state
# Q(s, act) = update Q-Table value q of state s and action a

# Our Q-Table! It will have four columns to represent each of the possible actions: up, down, left, and right.
Q = numpy.zeros([100000, 4])

# Since we will use states as our indexes for our Q-Table, but we cannot use the objects themselves as indexes,
# this dictionary will define integer versions of states for our Q-Table to access.
stateIntegers = {}

learningRate = 0.85 # percentage of how much a new value overrides an old value
discountFactor = 0.9 # importance between immediate rewards and future rewards
randomChance = 0.05 #percent of time a random action will happen instead of the desired action

class State:
    def __init__(self, applePosX, applePosY, tailPosX, tailPosY):
        self.applePosX = applePosX
        self.applePosY = applePosY
        self.tailPosX = tailPosX
        self.tailPosY = tailPosY


# obtain new state based on previous state
def newState(player, apple):
    headX = player.x[0]
    headY = player.y[0]
    appleX = apple.x
    appleY = apple.y
    appleRelativeX = appleX - headX
    appleRelativeY = appleY - headY

    tailIndex = player.length - 1
    tailX = player.x[tailIndex]
    tailY = player.y[tailIndex]
    tailRelativeX = tailX - headX
    tailRelativeY = tailY - headY

    state = State(appleRelativeX, appleRelativeY, tailRelativeX, tailRelativeY)

    return state




# determine optimal (most positive) action at s's position of the Q-Table
# returns the index with the highest value
def bestAction(s):
    return numpy.argmax(Q[stateToNumber(s), :])

# returns a unique number for the state passed, then put into the stateIntegers dictionary
def stateToNumber(s):
    # create a unique number for the state based on the values of its relative positions
    appleXNum = s.applePosX
    if(appleXNum < 0):
        appleXNum += 4815
    appleYNum = s.applePosY
    if(appleYNum < 0):
        appleYNum += 4815
    tailXNum = s.tailPosX
    if(tailXNum < 0):
        tailXNum += 4815
    tailYNum = s.tailPosY
    if(tailYNum < 0):
        tailYNum += 4815
    
    stateNum = int(str(appleXNum) + str(appleYNum) + str(tailXNum) + str(tailYNum))

    if stateNum in stateIntegers:
        return stateIntegers[stateNum]
    else:
        if len(stateIntegers):
            maximum = max(stateIntegers, key=stateIntegers.get)
            stateIntegers[stateNum] = stateIntegers[maximum] + 1
        else:
            stateIntegers[stateNum] = 1
    return stateIntegers[stateNum]


def updateQTable(state, newState, reward, action):
    newValue = reward + discountFactor * numpy.max(Q[stateToNumber(newState), :] - numpy.max(Q[stateToNumber(state), action]))
    Q[stateToNumber(state), action] += learningRate * newValue