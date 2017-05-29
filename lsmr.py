import math
import numpy

## Cost function
def C(state):
    sum = 0
    for s in state:
        sum += math.exp(state)
    return math.log(sum) # Natural Log

def getTotalPrice(currentState, bid):
    return C(bid) - C(currentState)

def doTrade(currentState, prices, bid):
    newState = currentState + bid
    sum = 0
    for outcome in newState:
        sum += math.exp(outcome)

    for i in xrange(0, bid.size):
        prices[i] = math.exp(newState[i]) / sum

    return newState, prices

# def makeTrade(userId, bid):
#     doTrade(numpy.array(map(int, bid.split(','))))
#     return
