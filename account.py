import numpy

class account:
    def __init__(self, name, n):
        self.username = name
        self.balance = 10.00
        self.bids = numpy.array([0] * n)
        self.bidHistory = [list(self.bids)]
        self.maxBidSize = 0

    def updateBids(self, bid):
        self.bids += bid
        self.updateMaxBidSize()
        self.updateBidHistory()

    def updateBidHistory(self):
        self.bidHistory.append(list(self.bids))

    def updateBalance(self, x):
        self.balance += x

    def getUserPage(self):
        html = "<html><head></head><body>"
        html += "<h2>{}</h2>".format(self.username)
        html += "<h3>Balance: {}</h3>".format(self.balance)
        html += "<h3>Current Bids: {}</h3>".format(self.bids)

    def updateMaxBidSize(self):
        for x in self.bids:
            if x > self.maxBidSize:
                self.maxBidSize = x
