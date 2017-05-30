from flask import Flask
from auction import auction

import lsmr

app = Flask(__name__)

a = auction()

@app.route('/')
def home_page():
    return 'LMSR FLASK APP'

@app.route('/getPrices/', methods=['GET'])
def getPrices():
    return a.getPrices()

@app.route('/getCost/<bid>/', methods=['GET'])
def getCost(bid):
    return a.getCost(bid)

@app.route('/makeTrade/<userId>/<bid>/', methods=['GET'])
def makeTrade(userId, bid):
    return a.makeTrade(userId, bid)

@app.route('/addUser/<userId>/', methods=['GET'])
def addUser(userId):
    return a.addUser(userId)

@app.route('/status/<userId>/', methods=['GET'])
def getStatus(userId):
    return a.getStatus(userId)

@app.route('/closeRegistration/', methods=['GET'])
def closeRegistration():
    return a.closeRegistration()

@app.route('/closeAuction/', methods=['GET'])
def closeAuction():
    return a.closeAuction()

@app.route('/winningOutcome/<index>/', methods=['GET'])
def winningOutcome(index):
    return a.winningOutcome(index)

@app.route('/auctionResults/', methods=['GET'])
def auctionResults():
    return a.auctionResults()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=False, threaded=True)
    except Exception as e:
        print "{}".format(e)
