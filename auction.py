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
    def __init__(self):
        self.prices = numpy.array([0.2,0.2,0.2,0.2,0.2])
        self.state = numpy.array([0, 0, 0, 0, 0])
        self.isRegistrationOpen = True
        self.isAuctionOpen = True
        self.accounts = dict()
        self.winningIndex = None
        self.balance = 0

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
            retval = "<h1>Auction Results</h1><hr>"

            # Payout to each bidder
            self.payout()

            retval += "<h3>Instantaneous Prices: {}</h3>".format(str(self.prices))
            retval += "<h3>Market Maker Balance: {}</h3><hr>".format(str(self.balance))
            retval += "<h4>Ordered Bidder Outcomes</h4>"

            # Order by balance
            for s in sorted(self.accounts.iteritems(), key=lambda (x,y): y['balance'], reverse=True):
                retval += "<p>User: {}</br>Position: {}</br>Balance: {}</br></br></p>".format(s[0],
                    s[1].get('bids'),
                    s[1].get('balance'))

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

        return retval

    def addUser(self, userId):
        retval = "User {} exists".format(userId)

        if not self.isAuctionOpen:
            retval = "Auction is closed"
        elif userId not in self.accounts:
            self.accounts[userId] = {'bids': numpy.array([0,0,0,0,0]), 'balance': 10.00}
            retval = "User Added: {}".format(userId)

        return retval
