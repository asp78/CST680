##

import math
import numpy

state = numpy.array([0,0])
prices = numpy.array([.5, .5])

## Cost function
def C(S):
    sum = 0
    for s in S:
        sum += math.exp(s)
    return math.log(sum) # Natural Log

def getTotalPrice(S):
    return C(S) - C(state)

def doTrade(S):
    global state
    global prices

    state = state + S
    sum = 0
    for o in state:
        sum += math.exp(o)
    
    for i in xrange(0, S.size):
        prices[i] = math.exp(state[i]) / sum

def printState():
    global state
    global prices
    print "state = {}\nprices = {}".format(state, prices)

def getPrices():
    global prices
    return prices

def makeTrade(userId, bid):
    doTrade(numpy.array(map(int, bid.split(','))))
    return ""

'''
newstate = numpy.array([1,0])
print getTotalPrice(newstate)
printState()
makeTrade(newstate)

newstate = numpy.array([2,0])
print getTotalPrice(newstate)
printState()
makeTrade(newstate)

newstate = numpy.array([0,1])
print getTotalPrice(newstate)
printState()
makeTrade(newstate)

newstate = numpy.array([-1, 0])
print getTotalPrice(newstate)
printState()
makeTrade(newstate)

printState()
'''
