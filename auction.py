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
        retval = "{} does not have enough money to buy {} for {}.".format(userId, bid, tradeCost)

        # If the bidder has enough money to make the trade
        user = self.accounts.get(userId)

        if user is None:
            retval = "User does not exist"
        elif user.get('balance') >= tradeCost:
            self.state, self.prices = lsmr.doTrade(self.state, self.prices, bid)\

            user['balance'] -= tradeCost
            user['bids'] += bid
            retval = "User: {}\nPosition: {}\nBalance: {}".format(userId,
                       user.get('bids'),
                       user.get('balance'))

        return retval

    def addUser(self, userId):
        retval = "User {} exists".format(userId)

        if userId not in self.accounts:
            self.accounts[userId] = {'bids': numpy.array([0,0]), 'balance': 20.00}
            retval = "User Added: {}".format(userId)

        return retval


