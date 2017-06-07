from account import account
from htmlMaker import accountPage

import numpy
import lsmr
import operator

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
        self.printPrices()
        self.printState()
        self.isRegistrationOpen = True
        self.isAuctionOpen = True
        self.accounts = []
        self.winningIndex = None
        self.balance = 0

    def printPrices(self):
        with open('prices.txt', 'a') as outfile:
            line = ""
            for x in xrange(0, self.numBins):
                if x < self.numBins - 1:
                    line += "{},".format(self.prices[x])
                else:
                    line += "{}".format(self.prices[x])

            line += "\n"
            outfile.write(line)

    def printState(self):
        with open('state.txt', 'a') as outfile:
            line = ""

            for x in xrange(0, self.numBins):
                if x < self.numBins - 1:
                    line += "{},".format(self.state[x])
                else:
                    line += "{}".format(self.state[x])

            line += "\n"
            outfile.write(line)

    def closeAuction(self):
        self.isAuctionOpen = False
        return "The auction is now closed."

    def closeRegistration(self):
        self.isRegistrationOpen = False
        return "User registration is now closed."

    def winningOutcome(self, i):
        self.winningIndex = int(i)
        return self.auctionResults()

    def getStatus(self, userId):
        retval = "User {} does not exist".format(userId)
        user = self.getAccount(userId)
        if user:
            retval = accountPage(user, self)
        return retval

    def getAccount(self, userId):
        retval = None

        for x in self.accounts:
            if x.username == userId:
                retval = x
                break

        return retval

    def auctionResults(self):
        retval = "The auction is still open! Check back later."

        if not self.isAuctionOpen:
            retval = "<html><head><style>table,th,td{border: 1px solid black;}</style></head><body><h1>Auction Results</h1><hr>"

            # Payout to each bidder
            self.payout()

            retval += "<h3>Winning Outcome: {}</h3>".format(chr(ord('A') + self.winningIndex))
            retval += "<h3>Instantaneous Prices: {}</h3>".format(str(self.prices))
            retval += "<h3>Market Maker Balance: {}</h3><hr>".format(str(self.balance))
            retval += "<h4>Ordered Bidder Outcomes</h4>"
            retval += "<table><tr><th>UserId</th><th>Position</th><th>Balance</th></tr>"

            # Order by balance
            self.accounts.sort(key=lambda x: x.balance, reverse=True)


            for a in self.accounts:
                retval += "<tr><th>{}</th><th>{}</th><th>${}</th></tr>".format(a.username,
                        a.bids, str(round(a.balance, 2)))

            retval += "</table></body></html>"

        return retval
        
    def payout(self):
        for x in self.accounts:
            x.updateBalance(x.bids[self.winningIndex])

    def getPrices(self):
        return str(self.prices)

    def getCost(self, bid):
        bid = numpy.array(map(int, bid.split(',')))
        retval = 'The auction is closed.'

        if bid.size != self.state.size:
            retval = "Invalid bid size, include all states even if they are zeros."
        elif self.isAuctionOpen:
            retval = str(lsmr.getTotalPrice(self.state, bid))

        return retval

    def makeTrade(self, userId, bid):
        bid = numpy.array(map(int, bid.split(',')))
        tradeCost = lsmr.getTotalPrice(self.state, bid)
        retval = "User {} does not exist".format(userId)
        # If the bidder has enough money to make the trade
        user = self.getAccount(userId)

        if not self.isAuctionOpen:
            retval = "Auction is closed"
        elif bid.size != self.state.size:
            retval = "Invalid bid size, include all states even if they are zeros."
        elif user:
            if user.balance < tradeCost:
                retval = "{} does not have enough money to buy {} for {}.".format(user.username, bid, tradeCost)
            elif not canSell(user.bids, bid):
                retval = "{} does not own the nesscary contracts to sell {}.".format(user.username, bid)
            else:
                self.state, self.prices = lsmr.doTrade(self.state, self.prices, bid)

                user.updateBalance(-tradeCost)
                self.balance += tradeCost
                user.updateBids(bid)
                retval = "<h2>Success</h2><button type=\"button\" onClick=\"goBack()\">Return</button><script>function goBack(){var url=window.location.href;url=url.substring(0, url.lastIndexOf(\"/\"));url=url.substring(0, url.lastIndexOf(\"/\"));url=url.replace(\"makeTrade\",\"status\");window.location.href=url;}</script>"

                self.printPrices()

        return retval

    def addUser(self, userId):
        retval = "User {} exists".format(userId)

        if not self.isAuctionOpen:
            retval = "Auction is closed"
        elif not self.isRegistrationOpen:
            retval = "Registration is closed"
        elif not self.isUserInAccounts(userId):
            self.accounts.append(account(userId, self.numBins))
            retval = "User Added: {}".format(userId)

        return retval

    def isUserInAccounts(self, userId):
        retbool = False

        for x in self.accounts:
            if x.username == userId:
                retbool = True
                
        return retbool
