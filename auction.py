from account import account
from htmlMaker import accountPage, auctionPage

import numpy
import lsmr
import operator
import time, datetime

def canSell(position, bid):
    for i in xrange(bid.size):
        if position[i] + bid[i] < 0:
            return False
    return True

class auction:
    '''
    An object to encompass an entire auction

    '''
    def __init__(self, name, n, labels):
        self.name = name
        self.numBins = n
        self.labels = labels
        self.prices = numpy.array([1.0/n] * n)
        self.state = numpy.array([0] * n)
        self.isRegistrationOpen = True
        self.isAuctionOpen = True
        self.accounts = []
        self.winningIndex = None
        self.balance = 0
        self.initFiles()

    def initFiles(self):
        self.printPrices()
        with open('trades.txt', 'a') as tradefile:
            line = "{}\n".format(self.getTimeStamp())
            tradefile.write(line)


    def printPrices(self):
        with open('prices.txt', 'a') as outfile:
            line = "{},".format(self.getTimeStamp())
            for x in xrange(0, self.numBins):
                line += "{},".format(self.prices[x])

            line = line[:-1] + '\n'
            outfile.write(line)

    # time, name, payment, state
    def printState(self, user, payment):
        with open('states.txt', 'a') as outfile:
            line = "{},{},{},".format(self.getTimeStamp(), user.name, payment)

            for x in xrange(0, self.numBins):
                line += "{},".format(self.state[x])

            line = line[:-1] + '\n'
            outfile.write(line)

    # time,name,bid
    def printTrade(self, user, bid, payment):
        with open('trades.txt', 'a') as outfile:
            bidstr = ""
            for x in xrange(0, self.numBins):
                bidstr += "{},".format(bid[x])

            bidstr = bidstr[:-1]

            line = "{},{},{},{}\n".format(self.getTimeStamp(), user.name, payment, bidstr)
            outfile.write(line)

    def printAccounts(self):
        with open('accounts.txt', 'w') as outfile:
            outfile.write('File Write @:{}\n'.format(datetime.datetime.now()))
            for a in self.accounts:
                outfile.write(str(a)+'\n')

    def getTimeStamp(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def closeAuction(self):
        self.isAuctionOpen = False
        return "The auction is now closed."

    def closeRegistration(self):
        self.isRegistrationOpen = False
        return "User registration is now closed."

    def winningOutcome(self, i):
        retstr = 'Auction is open, cannot set outcome.'
        if not self.isAuctionOpen:
            self.winningIndex = int(i)
            retstr = auctionPage(self)
        return retstr

    def getStatus(self, userId):
        retval = "User {} does not exist".format(userId)
        user = self.getAccount(userId)
        if user:
            retval = accountPage(user, self)
        return retval

    def getAccount(self, userId):
        retval = None

        for x in self.accounts:
            if x.id == userId:
                retval = x
                break

        return retval

    def getPrices(self):
        return str(self.prices)

    def getCost(self, bid):
        try:
            bid = numpy.array(map(int, bid.split(',')))
        except ValueError:
            print "CLOSE ONE"
            return "An error occurred."
        retval = "Invalid bid size, include all states even if they are zeros."

        if bid.size == self.state.size:
            retval = lsmr.getTotalPrice(self.state, bid)

        return retval

    def makeTrade(self, userId, bid):
        try:
            bid = numpy.array(map(int, bid.split(',')))
        except ValueError:
            print "CLOSE ONE"
            return "An error occurred."

        retval = "User {} does not exist".format(userId)
        # If the bidder has enough money to make the trade
        user = self.getAccount(userId)

        if not self.isAuctionOpen:
            retval = "Auction is closed"
        elif bid.size != self.state.size:
            retval = "Invalid bid size, include all states even if they are zeros."
        elif user:
            tradeCost = lsmr.getTotalPrice(self.state, bid)
            if user.balance < tradeCost:
                retval = "{} does not have enough money to buy {} for {}.".format(user.name, bid, tradeCost)
            elif not canSell(user.bids, bid):
                retval = "{} does not own the nesscary contracts to sell {}.".format(user.name, bid)
            else:
                self.state, self.prices = lsmr.doTrade(self.state, self.prices, bid)

                user.updateBalance(-tradeCost)
                self.balance += tradeCost
                user.updateBids(bid)
                retval = "<h2>Success</h2><button type=\"button\" onClick=\"goBack()\">Return</button><script>function goBack(){var url=window.location.href;url=url.substring(0, url.lastIndexOf(\"/\"));url=url.substring(0, url.lastIndexOf(\"/\"));url=url.replace(\"makeTrade\",\"status\");window.location.href=url;}</script>"

                self.printTrade(user, bid, tradeCost)
                self.printState(user, tradeCost)
                self.printPrices()
                self.printAccounts()

        return retval

    def addUser(self, userId, userName):
        retval = "User {} exists".format(userId)

        if not self.isAuctionOpen:
            retval = "Auction is closed"
        elif not self.isRegistrationOpen:
            retval = "Registration is closed"
        elif not self.isUserInAccounts(userId, userName):
            self.accounts.append(account(userId, userName, self.numBins))
            retval = "User Added: {}".format(userId)

        return retval

    def isUserInAccounts(self, userId, userName):
        retbool = False

        for x in self.accounts:
            if x.id == userId:
                retbool = True
                break
            if x.name == userName:
                retbool = True
                break

        return retbool

    def getNetWorth(self, outcome):
        sortedNames = []
        for x in sorted(self.accounts, key=lambda x: x.name):
            sortedNames.append(x.name)
        states = []
        state = [10.0] * len(sortedNames)

        with open('trades.txt', 'r') as infile:
            initTime = next(infile).strip()
            states.append((initTime, list(state)))
            for line in infile:
                linesplit = line.split(',')
                time = linesplit[0]
                username = linesplit[1]
                cost = float(linesplit[2])
                winBid = int(linesplit[3+int(outcome)])
                index = sortedNames.index(username)
                state[index] -= cost
                state[index] += winBid
                states.append((time, list(state)))

        return sortedNames, states
