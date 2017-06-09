import numpy

class account:
    def __init__(self, id, name, n):
        self.id = id
        self.name = name
        self.balance = 10.00
        self.netWorth = 10.00
        self.bids = numpy.array([0] * n)
        self.bidHistory = [list(self.bids)]
        self.maxBidSize = 0

    def __str__(self):
        return '{},{},{},{}'.format(self.id, self.name, self.balance, self.bids)

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
        html += "<h2>{}</h2>".format(self.name)
        html += "<h3>Balance: {}</h3>".format(self.balance)
        html += "<h3>Current Bids: {}</h3>".format(self.bids)

    def updateMaxBidSize(self):
        for x in self.bids:
            if x > self.maxBidSize:
                self.maxBidSize = x
