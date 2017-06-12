import numpy
from random import randint
import os.path
from datetime import datetime

def accountPage(user, auc):
    retstr = "<!DOCTYPE html><meta charset=\"utf-8\"><html><head><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\"><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script><script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script></head><body><div class=\"container\"><div><h1>AUCTION_TITLE_HERE</h1><hr><h2>USERNAME_HERE Account Status</h2><h3>Balance: BALANCE_HERE</h3></div><div><h3>Current bid placement</h3>BIDS_TABLE_HERE</div><div><h3>Place a new bet</h3>BET_FORM_HERE</div><div><h3>Bid History</h3><div style=\"width: 90%; height: 25%;\"><canvas id=\"myChart\"></canvas></div><script>var ctx=document.getElementById('myChart').getContext('2d');var chart = new Chart(ctx, {type: 'line', data: {labels: [DATA_LABELS_HERE],datasets: [DATA_SETS_HERE]},options: {scales:{yAxes:[{ticks:{stepSize:1}}]}}});</script></div></div></body></html>"

    retstr = retstr.replace("AUCTION_TITLE_HERE", "{}".format(auc.name))
    retstr = retstr.replace("USERNAME_HERE", "{}".format(user.name))
    retstr = retstr.replace("BALANCE_HERE", "{}".format("%.5f" % float(user.balance)))
    retstr = retstr.replace("BIDS_TABLE_HERE", "{}".format(getUserBidsTable(user, auc)))
    retstr = retstr.replace("DATA_LABELS_HERE", getDataLabels(user))
    retstr = retstr.replace("DATA_SETS_HERE", getUserDatasets(user, auc))
    retstr = retstr.replace("BET_FORM_HERE", getBetForm(user, auc))

    return retstr

def getBetForm(user, auc):
    retstr = "<table class=\"table\"><thead><tr><th>Bin</th>"

    for x in auc.labels:
        retstr += "<th>{}</th>".format(x)

    retstr += "</tr></thead><tbody><tr><th></th>"

    for x in range(0, auc.numBins):
        retstr += "<th><input id=\"trade{}\" type=\"text\" name=\"{}\" style=\"width: 80%;\" value=\"0\"></th>".format(x,x)

    retstr += "</tr></tbody></table><div class=\"btn-group\" role=\"group\" aria-label=\"...\"><button type=\"button\" class=\"btn btn-default\" onClick=\"makeTrade()\">Trade</button><script>function makeTrade(){if (CONDITION_HERE){var url=window.location.href;url=url.replace(\"status\",\"makeTrade\"); url += GET_ELEMENTS_HERE;$.ajax({url: url, success: function(result){window.location.reload(true);}});}}</script><button type=\"button\" class=\"btn btn-default\" onClick=\"checkPrice()\">Check Price</button><script>function checkPrice(){var url=window.location.href; url=url.substring(0,url.lastIndexOf(\"/\"));url=url.substring(0,url.lastIndexOf(\"/\"));url=url.replace(\"status\",\"getCost\");url+= \"/\" + GET_ELEMENTS_HERE;$.ajax({url: url, success: function(result){$(\"#tradeCost\").html('Checked Price: ' + result);}});}</script><span class=\"btn btn-primary\" disabled id=\"tradeCost\">Checked Price: </span></div>"

    getstr = ""

    for x in range(0, auc.numBins):
        getstr += "document.getElementById(\"trade{}\").value + ',' + ".format(x)

    getstr = getstr[:-9]

    condstr = "! ("

    for x in range(0, auc.numBins):
        condstr += "document.getElementById(\"trade{}\").value == 0 && ".format(x)

    condstr = condstr[:-4]
    condstr += ")"

    retstr = retstr.replace("GET_ELEMENTS_HERE", getstr)
    retstr = retstr.replace("GET_ELEMENTS_HERE", getstr)
    retstr = retstr.replace("CONDITION_HERE", condstr)

    return retstr

def getUserBidsTable(user, auc):
    retstr = "<table class=\"table\"><thead><tr><th>Bin</th>"

    for x in auc.labels:
        retstr += "<th>{}</th>".format(x)

    retstr += "</tr></thead><tbody><tr><th>Count</th>"

    for x in user.bids:
        retstr += "<th>{}</th>".format(x)

    retstr += "</tr></tbody></table>"

    return retstr

def getDataLabels(user):
    retstr = ""

    labels = range(0, len(user.bidHistory))

    for x in labels:
        retstr += "\"{}\",".format(x)

    retstr = retstr[:-1]

    return retstr

def getUserDatasets(user, auc):
    data = []
    retstr = ""

    for x in xrange(0, user.bids.size):
        data.append([item[x] for item in user.bidHistory])

    for x in xrange(0, user.bids.size):
        retstr += "{{label: \"{}\", fill:false, steppedLine: true, borderColor: 'rgb({})',data: [{}]}},".format(auc.labels[x], getLineColor(x), getDataString(data, x))

    retstr = retstr[:-1]

    return retstr

def netWorth(auc, outcome):
    retstr = ''
    if os.path.isfile('trades.txt'):
        retstr = "<canvas id=\"netWorthChart\"></canvas></div><script>var ctx=document.getElementById('netWorthChart').getContext('2d');var chart = new Chart(ctx, {type: 'line', data: {labels: [DATA_LABELS_HERE],datasets: [DATA_SETS_HERE]},"
        retstr += "options: { scales: { xAxes: [{ type: 'time', time: { format: 'YYYY-MM-DD HH:mm:ss', tooltipFormat: 'll HH:mm:ss'}}]}}});</script>"

        datastr, start, end = getNetWorthDataAndStartEnd(auc, outcome)

        retstr = retstr.replace("DATA_LABELS_HERE", getNetWorthDataLabels(start, end))
        retstr = retstr.replace("DATA_SETS_HERE", datastr)
    return retstr

def getNetWorthDataLabels(start, end):
    retstr = '"{}", "{}"'.format(start, end) #return them comma seperated

    return retstr

def getNetWorthDataAndStartEnd(auc, outcome):
    sortedNames, states = auc.getNetWorth(outcome)
    retstr = ""
    colors = getRandomColors(len(sortedNames))

    for x in xrange(0, len(sortedNames)):
        retstr += "{{label: \"{}\", fill:false, steppedLine: true, borderColor: 'rgb({})',data: [{}]}},".format(sortedNames[x], colors[x], getNetWorthDataString(states, x))

    retstr = retstr[:-1]

    return retstr, states[0][0], states[len(states)-1][0]

def getDataString(data, n):
    retstr = ""

    for x in data[n]:
        retstr += "{},".format(x)

    retstr = retstr[:-1]

    return retstr

def getNetWorthDataString(states, n):
    retstr = ""

    for s in states:
        retstr += '{'
        retstr += ' x:"{}", y:{}'.format( s[0], "%.5f" % float(s[1][n]))
        retstr += '},'

    retstr = retstr[:-1]

    return retstr

def getRandomColors(count):
    colors = []
    for i in xrange(count):
        colors.append('{},{},{}'.format(randint(0,255), randint(0,255), randint(0,255)))
    return colors

def getLineColor(n):
    colors = ["255,99,132", "120,120,120", "5,36,182", "84,161,83", "63,157,208", "9,76,11", "112,25,125", "149,79,105", "120,237,207", "119,100,10"]

    return colors[n]

def auctionPage(auc):
    retstr = "<!DOCTYPE html><meta charset=\"utf-8\"><html><head><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\"><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script><script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script>"
    retstr += "</head><body><div class=\"container\"><div><h1>AUCTION_TITLE_HERE</h1><hr></div>CLOSED_INFO_HERE<div><h2>Market Status</h2>STATUS_HERE</div><div><h2>Leaderboard</h2>LEADERBOARD_HERE<div>OUTCOME_SELECT OUTCOME_GRAPH</div></div></div></body></html>"

    retstr = retstr.replace("AUCTION_TITLE_HERE", "{}".format(auc.name))
    retstr = retstr.replace("CLOSED_INFO_HERE", getClosedInfo(auc))
    retstr = retstr.replace("STATUS_HERE", getStatusTable(auc))
    retstr = retstr.replace("LEADERBOARD_HERE", getLeaderboardTable(auc))
    outcomeIndex = auc.winningIndex if auc.winningIndex is not None else 0
    retstr = retstr.replace("OUTCOME_SELECT", getOutcomeSelect(auc.labels, outcomeIndex))
    retstr = retstr.replace("OUTCOME_GRAPH", netWorth(auc, outcomeIndex))

    return retstr

def getClosedInfo(auc):
    retstr = '<h4>Auction Is Open</h4>'
    if auc.winningIndex is not None:
        payouts = 0
        for a in auc.accounts:
            payouts += a.bids[auc.winningIndex]

        retstr = '<h3>Winning Outcome: {}</h3>'.format(auc.labels[auc.winningIndex])
        retstr += '<h3>Market Maker Balance: {}</h3>'.format("%.5f" % float(auc.balance - payouts))
    return retstr

def getStatusTable(auc):
    retstr = "<div class=\"row\"><div class=\"col-md-4\">"
    retstr +="<table class=\"table\"><thead><tr><th>Contract</th><th>Price</th><th># Owned</th></tr></thead><tbody>"
    for i in xrange(auc.numBins):
        retstr += "<tr><th>{}</th>".format(auc.labels[i])
        retstr += "<th>{}</th>".format("%.5f" % float(auc.prices[i]))
        retstr += "<th>{}</th></tr>".format(auc.state[i])

    retstr += "</tbody></table></div><div class=\"col-md-4\"><h3>Prices</h3><canvas id=\"pricesChart\"/><script>var ctx=document.getElementById('pricesChart').getContext('2d');var chart = new Chart(ctx, { type: 'doughnut', data: {labels: [PRICES_LABELS_HERE], datasets: [{data :[PRICES_DATA_HERE], backgroundColor : [PRICES_COLORS_HERE], label: 'data1'}],options: {responsive: true,legend: { position: 'top'}, animation: {animateScale: true, animateRotate: true}}}});</script></div><div class=\"col-md-4\"><h3>State</h3><canvas id=\"stateChart\"/><script>var ctx=document.getElementById('stateChart').getContext('2d');var chart = new Chart(ctx, { type: 'doughnut', data: {labels: [STATE_LABELS_HERE], datasets: [{data :[STATE_DATA_HERE], backgroundColor : [STATE_COLORS_HERE], label: 'data1'}],options: {responsive: true,legend: { position: 'top'}, animation: {animateScale: true, animateRotate: true}}}});</script></div></div>"

    retstr = retstr.replace("PRICES_LABELS_HERE", getAuctionLabels(auc))
    retstr = retstr.replace("PRICES_DATA_HERE", getPricesData(auc))
    retstr = retstr.replace("PRICES_COLORS_HERE", getPricesColors(auc))

    retstr = retstr.replace("STATE_LABELS_HERE", getAuctionLabels(auc))
    retstr = retstr.replace("STATE_DATA_HERE", getStateData(auc))
    retstr = retstr.replace("STATE_COLORS_HERE", getPricesColors(auc))

    return retstr

def getAuctionLabels(auc):
    retstr = ""
    for x in auc.labels:
        retstr += "\"{}\",".format(x)

    retstr = retstr[:-1]

    return retstr

def getPricesData(auc):
    retstr = ""
    for x in auc.prices:
        retstr += "{},".format("%.5f" % float(x))

    retstr = retstr[:-1]
    return retstr

def getStateData(auc):
    retstr = ""
    for x in auc.state:
        retstr += "{},".format(x)

    retstr = retstr[:-1]
    return retstr

def getPricesColors(auc):
    retstr = ""
    colors = getRandomColors(auc.prices.size);

    for x in colors:
        retstr += "'rgba({}, 0.5)',".format(x)

    retstr = retstr[:-1]
    return retstr

def getLeaderboardTable(auc):
    retstr = "<div class=\"row\"><div class=\"col-xs-12\">"
    retstr += "<table class=\"table table-hover\"><thead><tr><th>User</th><th>Balance</th>"

    if auc.isAuctionOpen:
        retstr += "<th>Balance + Contracts Sold</th>"
    elif auc.winningIndex is not None:
        retstr += "<th>Networth</th>"

    for x in auc.labels:
        retstr += "<th>{}</th>".format(x)

    retstr += "</tr></thead><tbody><div><div>"

    for a in auc.accounts:
        if auc.isAuctionOpen:
            bidStr = ''
            for b in a.bids:
                bidStr += "-{},".format(b)
            bidStr = bidStr[:-1]
            cost = auc.getCost(bidStr)
            a.networth = a.balance - cost
        elif auc.winningIndex is not None:
            a.networth = a.balance + a.bids[auc.winningIndex]

    auc.accounts.sort(key=lambda a: a.networth, reverse=True)

    for a in auc.accounts:

        retstr += "<tr><th>{}</th>".format(a.name)
        retstr += "<th>{}</th>".format("%.5f" % float(a.balance))
        if auc.isAuctionOpen or auc.winningIndex is not None:
            retstr += "<th>{}</th>".format("%.5f" % float(a.networth))

        for y in a.bids:
            retstr += "<th>{}</th>".format(y)

        retstr += "</tr>"

    retstr += "</tbody></table>"

    return retstr

def getOutcomeSelect(labels, selectedIndex):
    retstr = '<h3>Networths Over Trades</h3>'
    if os.path.isfile('trades.txt'):
        retstr = '<script>function outcomeSelected(){chart.destroy(); var index = document.getElementById("outcomeSelect").selectedIndex; var url=window.location.href;'
        retstr += ' url=url.substr(0, url.indexOf("5000")); url+="5000/getNetWorths/"+index+"/";'
        retstr += ' $.ajax({url: url, success: function(result){ $("#netWorthChart").replaceWith(result);}});}</script>'
        retstr += '<div class="col-md-4"><h3>Possible Outcomes</h3><label for="outcomeSelect">Winning Outcome (select one):</label>'
        retstr += '<select class="form-control" onchange="outcomeSelected()" id="outcomeSelect">'
        for i in xrange(len(labels)):
            selected = 'selected' if i is selectedIndex else ''
            retstr += '<option '+selected+'>'+labels[i]+'</option>'
        retstr += '</select></div>'
    return retstr

def helpPage(auc):
    url = 'http://68.82.242.210:5000/'

    retstr = '<!DOCTYPE html><meta charset=\"utf-8\"><html><head><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\"><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script><script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script></head>'
    retstr += '<body><div class=\"container\">HELP_PAGE_HERE</div></div></body></html>'

    helpPageHTML = '<div class="marketing col-md-10"><h1>AUCTION_TITLE_HERE Help Page</h1>'
    helpPageHTML += '<h3>Key Pages</h3>'
    helpPageHTML += '<p>There are two key pages: the Auction Page, where you can view the'
    helpPageHTML += ' overall status of the auction, and your Account Page, where you'
    helpPageHTML += ' can view your balance and purchased contract and can make new trades.'
    helpPageHTML += ' It is also now possible to download the price, state, and trade log files from the links below.</p>'
    helpPageHTML += '<h4>Auction Page</h4><a href="'+url+'">'+url+'</a>'
    helpPageHTML += '<h4>User Page</h4><p>'+url+'status/yourUserId</p>'
    helpPageHTML += '<h4>Price Logs</h4><a href="'+url+'getPriceLogs/" download>'+url+'getPriceLogs/</a>'
    helpPageHTML += '<h4>State Logs</h4><a href="'+url+'getStateLogs/" download>'+url+'getStateLogs/</a>'
    helpPageHTML += '<h4>Trade Logs</h4><a href="'+url+'getTradeLogs/" download>'+url+'getTradeLogs/</a>'
    helpPageHTML += '<br><h3>Key Equations</h3>'
    helpPageHTML += '<p>The market marker relies on 3 key functions to operate. C and makeTrade both use the variable B, which is a constant (in this case 3) and which allows for the adjustment of the market\'s liquidity.'
    helpPageHTML += ' The first function, C, is a cost function that computes the cost to the market maker to exist in the given state. Here a state is an array, with an index for each of the possible outcomes, containing the number of contracts that are owned for that outcome.</p>'
    helpPageHTML += '''<pre><code>def C(state):
    sum = 0
    for s in state:
        sum += math.exp(s / B)
    return B * math.log(sum)</code></pre>'''
    helpPageHTML += '<p>The second function, getTotalPrice, calculates the cost for the market maker to move from the given current state to the new state brought about by the given bid. Here a bid is is an array, with an index for each of the possible outcomes, containing the number of contracts to be bought for that outcome. The returned cost is the price a trade pays for making the bid.</p>'
    helpPageHTML += '''<pre><code>def getTotalPrice(currentState, bid):
    newState = bid + currentState
    return C(newState) - C(currentState)</code></pre>'''
    helpPageHTML += '<p>The third function, makeTrade, changes the current state to a new state given a new bid, and updates the prices for each outcome given the bid.</p>'
    helpPageHTML += '''<pre><code>def def makeTrade(currentState, prices, bid):
    newState = currentState + bid
    sum = 0
    for outcome in newState:
        sum += math.exp(outcome / B)

    for i in xrange(0, bid.size):
        prices[i] = math.exp(newState[i] / B) / sum

    return newState, prices'''

    helpPageHTML = helpPageHTML.replace("AUCTION_TITLE_HERE", "{}".format(auc.name))
    retstr = retstr.replace("HELP_PAGE_HERE", helpPageHTML)

    return retstr
