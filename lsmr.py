import math
import numpy

beta = 3.0

## Cost function
def C(state):
    sum = 0.0
    for s in state:
        sum += math.exp(s / beta)
    return beta * math.log(sum) # Natural Log

def getTotalPrice(currentState, bid):
    newState = bid + currentState
    return C(newState) - C(currentState)

def doTrade(currentState, prices, bid):
    newState = currentState + bid
    sum = 0.0
    for outcome in newState:
        sum += math.exp(outcome / beta)

    for i in xrange(0, bid.size):
        prices[i] = math.exp(newState[i] / beta) / sum

    return newState, prices
