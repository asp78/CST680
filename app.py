from flask import Flask
from auction import auction
from htmlMaker import helpPage
from htmlMaker import auctionPage

import lsmr
import traceback

app = Flask(__name__)

## Auction variables
auctionName = "CST680 Prediction Market for Final"
numberOfBins = 10
binLabels = ['100-90','89-85','84-80','79-75','74-70','69-65','64-60','59-55','54-50','49-0']

a = auction(auctionName, numberOfBins, binLabels)

@app.route('/')
def home_page():
    return auctionPage(a)

@app.route('/getPrices/', methods=['GET'])
def getPrices():
    try:
        return a.getPrices()
    except Exception as e:
        print e
        return "An error occurred."

@app.route('/getCost/<bid>/', methods=['GET'])
def getCost(bid):
    try:
        return a.getCost(bid)
    except Exception as e:
        print e
        return "An error occurred."

@app.route('/makeTrade/<userId>/<bid>/', methods=['GET'])
def makeTrade(userId, bid):
    try:
        return a.makeTrade(userId, bid)
    except Exception as e:
        print e
        return "An error occurred."

@app.route('/addUser/<userId>/', methods=['GET'])
def addUser(userId):
    try:
        return a.addUser(userId)
    except Exception as e:
        print e
        return "An error occurred."

@app.route('/status/<userId>/', methods=['GET'])
def getStatus(userId):
    try:
        return a.getStatus(userId)
    except Exception as e:
        print e
        print traceback.print_exc()
        return "An error occurred."

@app.route('/closeRegistration/', methods=['GET'])
def closeRegistration():
    try:
        return a.closeRegistration()
    except Exception as e:
        print e
        return "An error occurred."

@app.route('/closeAuction/', methods=['GET'])
def closeAuction():
    try:
        return a.closeAuction()
    except Exception as e:
        print e
        return "An error occurred."

@app.route('/winningOutcome/<index>/', methods=['GET'])
def winningOutcome(index):
    try:
        return a.winningOutcome(index)
    except Exception as e:
        print e
        return "An error occurred."

@app.route('/auctionResults/', methods=['GET'])
def auctionResults():
    try:
        return a.auctionResults()
    except Exception as e:
        print e
        return "An error occurred."

@app.route('/help/', methods=['GET'])
def help():
    return helpPage(a)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=False, threaded=True)
    except Exception as e:
        print "{}".format(e)
