#!/usr/bin/python
# -*- coding: UTF-8 -*-

## Implmentation based on the paper:
## Othman, Abraham, and Tuomas Sandholm. "Profit-charging market makers with
## bounded loss, vanishing bid/ask spreads, and unlimited market depth."
## Proceedings of the 13th ACM Conference on Electronic Commerce. ACM, 2012.

import numpy
import math

## Payout Vector - Defined as x ∈ Rn where xi is the cumulative amount the
## market maker must pay out to traders if the future state of the world ωi is
## realized. states ω = ['A', 'B', 'C', 'D', 'F']
x = numpy.array([0, 0, 0, 0, 0])
## We made the assumption that initially the market maker had 0 payout costs

## Barrier Utility Function - Defined as including all positive values. A
## strictly increasing, concave function such that lim(x->0). u(x) = -∞.
## log(x) and 1/x are given as examples
def u(x):
    return math.log(x)

## Probability vector - pi is defined as the market maker's (subjective)
## probability that ωi will occur. Our understanding is that these values don't
## change as contracts are sold, but instinctually this seems wrong?
p = numpy.array([0.20, 0.20, 0.20, 0.20, 0.20])

## Bounded Loss Limit - Let C be a constant-utility cost function that employs
## a barrier utility function. If pi > 0 for every i, the cost function-based
## market maker using C loses at most x0
x0 = 100
## x0 is one of the variables we don't think we understand fully

## Liquidity Function - Defined as: non-decreasing function R+ → R f(0)=0
def f(x):
    return x

## Profit Function - Defined as: non-decreasing function R+ → R g(0)=0
def g(x):
    return x

## Distance Function (metric) - Defined as: Rn X Rn → R+. We assumed this
## should return the euclidean distance between the 2 vectors x and y.
def d(x, y):
    return numpy.linalg.norm(x - y)

## Internal scalar initialized to 0 - Defined as the measure of the cumulative
## volume transacted in the market. If a bet is taken, the state changes:
# s ← s + d(x, y) (see line 112)
s = 0

## When a trader wishes to place a bet that would move the market maker from
## payout vector x to payout vector y:

## The cost function C(y) is solved implicitly for:
## Σ[i = 0 -> n-1](pi * u(C(y) - yi + f(s + d(x,y)))) = u(x0 + f(s + d(x, y)))
def LHS(y, p, costGuess, s, x):
    sum = 0
    for i in xrange(0, y.size):
        sum += p[i] * u(costGuess - y[i] + f(s + d(x,y)))
    return sum

def RHS(x0, s, x, y):
    return u(x0 + f(s + d(x, y)))

## C(y) is found using binary search as recommended
def BinaryMarketMakerCostSearch(y, x, s, p, x0):
    ## We are unsure of the proper inital max and min here
    maxLimit = x0*x0
    minLimit = 0
    #print 'START SEARCH'

    guess = (maxLimit - minLimit)/2.0 + minLimit
    lhs = LHS(y, p, guess, s, x)
    rhs = RHS(x0, s, x, y)

    while (lhs != rhs):
        ##print 'LHS:', lhs, 'RHS:', rhs, 'min:', minLimit, 'max:', maxLimit
        if lhs < rhs:
            minLimit = guess
        else:
            maxLimit = guess
        guess = (maxLimit - minLimit) / 2.0 + minLimit

        lhs = LHS(y, p, guess, s, x)
        rhs = RHS(x0, s, x, y)

    return guess

## Previous cost : the cost function C(y) is saved for the next transaction
previousCy = 0

## Cost to Trader - Defined as the total cost quoted to the trader for the bet
## is the sum of the changes to the cost function, liquidity function, and
## profit function
## M(x, y) ≡ C(y) − C(x) + f(s + d(x, y)) − f(s) + g(s + d(x, y)) − g(s)
def M(y, x, s, p, x0, previousCy):
    cy = BinaryMarketMakerCostSearch(y, x, s, p, x0)
    return cy - previousCy  + f(s + d(x, y)) - f(s) + g(s + d(x, y)) - g(s)

## Helper method which quotes a price to a trader given a trade, which is a vector
## of number of bets for each outcome in ω
def quotePrice(trade, x, s, p, x0, previousCy):
    y = x+trade #the new payout vector if the trade is made
    return M(y, x, s, p, x0, previousCy)

## Helper method which executes a trade
def makeTrade(trade, x, s, p, x0):
    y = x+trade #the new payout vector
    cy = BinaryMarketMakerCostSearch(y, x, s, p, x0)
    s += d(x,y)
    x = y
    previousCy = cy
    return x, s, previousCy

print 'x:', x, 's:', s, 'previousCy:', previousCy

print
trade = numpy.array([1, 0, 0, 0, 0])
print 'Trade 1:', trade
print 'Price Quote:', quotePrice(trade, x, s, p, x0, previousCy)
x, s, previousCy = makeTrade(trade, x, s, p, x0)
print 'x:', x, 's:', s, 'previousCy:', previousCy

print
trade = numpy.array([1, 0, 0, 0, 0])
print 'Trade 2:', trade
print 'Price Quote:', quotePrice(trade, x, s, p, x0, previousCy)
x, s, previousCy = makeTrade(trade, x, s, p, x0)
print 'x:', x, 's:', s, 'previousCy:', previousCy

print
trade = numpy.array([1, 0, 0, 0, 0])
print 'Trade 3:', trade
print 'Price Quote:', quotePrice(trade, x, s, p, x0, previousCy)
x, s, previousCy = makeTrade(trade, x, s, p, x0)
print 'x:', x, 's:', s, 'previousCy:', previousCy
