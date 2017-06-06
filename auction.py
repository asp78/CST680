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
        self.accounts = dict()
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
        user = self.accounts.get(userId)
        if user:
            retval = "User: {}\nPosition: {}\nBalance: {}".format(userId,
                       user.get('bids'),
                       user.get('balance'))
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
            for s in sorted(self.accounts.iteritems(), key=lambda (x,y): y['balance'], reverse=True):
                retval += "<tr><th>{}</th><th>{}</th><th>${}</th></tr>".format(s[0],
                        s[1].get('bids'),
                        str(round(s[1].get('balance'), 2)))

            retval += "</table></body></html>"

        return retval
        
    def payout(self):
        for key,value in self.accounts.iteritems():
            value['balance'] += value['bids'][self.winningIndex]
            self.balance -= value['bids'][self.winningIndex]

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
        user = self.accounts.get(userId)

        if not self.isAuctionOpen:
            retval = "Auction is closed"
        elif bid.size != self.state.size:
            retval = "Invalid bid size, include all states even if they are zeros."
        elif user:
            if user.get('balance') < tradeCost:
                retval = "{} does not have enough money to buy {} for {}.".format(userId, bid, tradeCost)
            elif not canSell(user.get('bids'), bid):
                retval = "{} does not own the nesscary contracts to sell {}.".format(userId, bid)
            else:
                self.state, self.prices = lsmr.doTrade(self.state, self.prices, bid)\

                user['balance'] -= tradeCost
                self.balance += tradeCost
                user['bids'] += bid
                retval = "User: {}\nPosition: {}\nBalance: {}".format(userId,
                           user.get('bids'),
                           user.get('balance'))

                self.printPrices()

        return retval

    def addUser(self, userId):
        retval = "User {} exists".format(userId)

        if not self.isAuctionOpen:
            retval = "Auction is closed"
        elif userId not in self.accounts:
            self.accounts[userId] = {'bids': numpy.array([0] * self.numBins), 'balance': 10.00}
            retval = "User Added: {}".format(userId)

        return retval
