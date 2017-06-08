from flask import Flask, send_file
from auction import auction
from htmlMaker import helpPage
from htmlMaker import auctionPage
from htmlMaker import netWorth

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
        print traceback.print_exc()
        return "An error occurred."

@app.route('/getNetWorth/<outcome>/')
def getNetWorth(outcome):
    try:
        return netWorth(a, outcome)
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/getPriceLogs/', methods=['GET'])
def getPriceLogs():
    try:
        return send_file('prices.txt')
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/getStateLogs/', methods=['GET'])
def getStateLogs():
    try:
        return send_file('states.txt')
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/getTradeLogs/', methods=['GET'])
def getTradeLogs():
    try:
        return send_file('trades.txt')
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/getCost/<bid>/', methods=['GET'])
def getCost(bid):
    try:
        return str(a.getCost(bid))
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/makeTrade/<userId>/<bid>/', methods=['GET'])
def makeTrade(userId, bid):
    try:
        return a.makeTrade(userId, bid)
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/addUser/<userId>/', methods=['GET'])
def addUser(userId):
    try:
        return a.addUser(userId)
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/status/<userId>/', methods=['GET'])
def getStatus(userId):
    try:
        return a.getStatus(userId)
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/closeRegistration/', methods=['GET'])
def closeRegistration():
    try:
        return a.closeRegistration()
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/closeAuction/', methods=['GET'])
def closeAuction():
    try:
        return a.closeAuction()
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/winningOutcome/<index>/', methods=['GET'])
def winningOutcome(index):
    try:
        return a.winningOutcome(index)
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/auctionResults/', methods=['GET'])
def auctionResults():
    try:
        return a.auctionResults()
    except Exception as e:
        print traceback.print_exc()
        return "An error occurred."

@app.route('/help/', methods=['GET'])
def help():
    return helpPage(a)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=False, threaded=True)
    except Exception as e:
        print "{}".format(e)
