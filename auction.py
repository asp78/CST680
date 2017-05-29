import numpy
import lsmr

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

    def closeAuction(self):
        self.isAuctionOpen = False

    def closeRegistration(self):
        self.isRegistrationOpen = False

    def getPrices(self, bid):
        retval = 'The auction is closed.'

        if self.isAuctionOpen:
            retval = str(self.prices)

        return retval

    def makeTrade(self, userId, bid):
        bid = numpy.array(map(int, bid.split(',')))
        tradeCost = lsmr.getTotalPrice(self.state, bid)
        print tradeCost

        self.state, self.prices = lsmr.doTrade(self.state, self.prices, bid)
        return "TRADED"

    def addUser(self, userId):
        retval = "User {} exists".format(userId)

        if userId not in self.accounts:
            self.accounts[userId] = {'bids': [0,0,0,0,0], 'balance': 1000.00}
            retval = "User Added: {}".format(userId)

        return retval
