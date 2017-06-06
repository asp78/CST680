from flask import Flask
from auction import auction

import lsmr

app = Flask(__name__)

## Auction variables
auctionName = "CST680 Prediction Market for Final"
numberOfBins = 10
binLabels = ['100-90','89-85','84-80','79-75','74-70','69-65','64-60','59-55','54-50','49-0']

a = auction(auctionName, numberOfBins, binLabels)

@app.route('/')
def home_page():
    return help()

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
    helpstr = "<style>table,th,td{border: 1px solid black;}</style><h1>Help Page for LSMR Auction</h1><p>This page tells your how to participate in the class auction.<br>Firstly, everything is done using URL commands. This means if you would like to make a trade you would type 'http://69.242.79.111:5000/userId/makeTrade/#,#,#,#,#,#,#,#,#,#' into the URL bar. This is the essence of most commands detailed below.</p><p>The only parameters you ever give are a userId which is just some string, and a bid which is of the format '#,#,#,#,#,#,#,#,#,#' (without the 's) where each # is an integer representing the amount of dollars you would like to recieve if a certain outcome occurred.</p><p>For example, to place 1 trade for outcome '90-85' and 2 for outcome '85-80', you would type '69.242.79.111:5000/makeTrade/userId/0,1,2,0,0,0,0,0,0,0' into your URL bar.</p><p><strong>NOTE: You must include all 10 fields in your bid, even if they are 0 - ie '0,1,2' is NOT a valid bid</strong></p><p>Each field in a bid correspond to the following ranges</p><table><tr><th>100-90</th><th>89-85</th><th>84-80</th><th>79-75</th><th>74-70</th><th>69-65</th><th>64-60</th><th>59-55</th><th>54-50</th><th>49-0</th></tr></table><hr>"

    helpstr += "<h3>Commands</h3>"
    helpstr += "<p><strong>/help</strong> - Displays this help page</p>"
    helpstr += "<p><strong>/getPrices</strong> - Returns the instantaneous prices of the auction. These represent the markets <em>probability</em> that each event will occur, not the cost of trading.</p>"
    helpstr += "<p><strong>/getCost/&lt;bid&gt;</strong> - Returns the cost you would incur if you wanted to place a certain bid.</p>"
    helpstr += "<p><strong>/makeTrade/&lt;userId&gt;/&lt;bid&gt;</strong> - Performs a trade unless you do not have the money to make the trade.</p>"
    helpstr += "<p><strong>/getStatus/&lt;userId&gt;</strong> - Returns the current bids and balance of a user.</p>"
    helpstr += "<p><strong>/auctionResults</strong> - Once the auction is complete, this page displays the results of the auction.</p>"
    helpstr += "<hr><h3>Example of use:</h3>"
    helpstr += "<p><em>http://69.242.79.111:5000/addUser/asp78</em> Adds a user 'asp78' to the system.</p>"
    helpstr += "<p><em>http://69.242.79.111:5000/getCost/0,1,1,1,0,0,0,0,0,0</em> Shows the cost of making a trade for 1 of each outcome '90-85', '85-80', and '80-75'.</p>"
    helpstr += "<p><em>http://69.242.79.111:5000/makeTrade/asp78/0,1,1,1,0,0,0,0,0,0</em> Makes the trade for 1 of each outcome '90-85', '85-80', and '80-75'.</p>"
    helpstr += "<p><em>http://69.242.79.111:5000/getStatus/asp78</em> Displays 'asp78's balance and bids</p>"
    return helpstr

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=False, threaded=True)
    except Exception as e:
        print "{}".format(e)
