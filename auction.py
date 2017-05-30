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
        self.prices = numpy.array([0.5, 0.5])
        self.state = numpy.array([0, 0])
        self.isRegistrationOpen = True
        self.isAuctionOpen = True
        self.accounts = dict()
        self.winningIndex = None

    def closeAuction(self):
        self.isAuctionOpen = False
        return "Auction is closed"

    def closeRegistration(self):
        self.isRegistrationOpen = False
        return "Registration is closed"

    def winningOutcome(self, i):
        self.winningIndex = int(i)
        self.getFinalState()

    def getFinalState(self):
        # Payout
        self.payout()

        # Order by balance
        sortedAs = sorted(self.accounts.items(), key=operator.itemgetter(1)['balance'])

        # return pretty string
        return sortedAs

    def payout(self):
        for a in accounts:
            a['balance'] += a['bids'][self.winningIndex]

    def getPrices(self):
        return str(self.prices)

    def getCost(self, bid):
        bid = numpy.array(map(int, bid.split(',')))
        retval = 'The auction is closed.'

        if self.isAuctionOpen:
            retval = str(lsmr.getTotalPrice(self.state, bid))

        return retval

    def makeTrade(self, userId, bid):
        bid = numpy.array(map(int, bid.split(',')))
        tradeCost = lsmr.getTotalPrice(self.state, bid)
        retval = "User does not exist"
        # If the bidder has enough money to make the trade
        user = self.accounts.get(userId)

        if not self.isAuctionOpen:
            retval = "Auction is closed"
        elif user:
            if user.get('balance') < tradeCost:
                retval = "{} does not have enough money to buy {} for {}.".format(userId, bid, tradeCost)
            elif not canSell(user.get('bids'), bid):
                retval = "{} does not own the nesscary contracts to sell {}.".format(userId, bid)
            else:
                self.state, self.prices = lsmr.doTrade(self.state, self.prices, bid)\

                user['balance'] -= tradeCost
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
            self.accounts[userId] = {'bids': numpy.array([0,0]), 'balance': 20.00}
            retval = "User Added: {}".format(userId)

        return retval
