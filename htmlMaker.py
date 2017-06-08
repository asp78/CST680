import numpy
from random import randint

def accountPage(user, auc):
    retstr = "<!DOCTYPE html><meta charset=\"utf-8\"><html><head><style>table, th, td {border: 1px solid black;}</style><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\"><script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script></head><body><div class=\"container\"><div><h1>AUCTION_TITLE_HERE</h1><hr><h2>USERNAME_HERE Details</h2><h3>Balance: BALANCE_HERE</h3></div><div><h3>Current bid placement</h3>BIDS_TABLE_HERE</div><div><h3>Place a new bet</h3>BET_FORM_HERE</div><div><h3>Bid History</h3><div style=\"width: 90%; height: 25%;\"><canvas id=\"myChart\"></canvas></div><script>var ctx=document.getElementById('myChart').getContext('2d');var chart = new Chart(ctx, {type: 'line', data: {labels: [DATA_LABELS_HERE],datasets: [DATA_SETS_HERE]},options: {scales:{yAxes:[{ticks:{stepSize:1}}]}}});</script></div></div></body></html>"

    retstr = retstr.replace("AUCTION_TITLE_HERE", "{}".format(auc.name))
    retstr = retstr.replace("USERNAME_HERE", "{}".format(user.username))
    retstr = retstr.replace("BALANCE_HERE", "{}".format(user.balance))
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
    #labels = range(0, 8)

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
        retstr += "{{label: \"{}\", fill:false, borderColor: 'rgb({})',data: [{}]}},".format(auc.labels[x], getLineColor(x), getDataString(data, x))

    retstr = retstr[:-1]

    return retstr

def netWorth(auc, outcome):
    retstr = "<!DOCTYPE html><meta charset=\"utf-8\"><html><head><style>table, th, td {border: 1px solid black;}</style><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\"><script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script></head><canvas id=\"netWorthChart\"></canvas></div><script>var ctx=document.getElementById('netWorthChart').getContext('2d');var chart = new Chart(ctx, {type: 'line', data: {labels: [DATA_LABELS_HERE],datasets: [DATA_SETS_HERE]},options: {}});</script>"

    length, datastr = getNetWorthDatasets(auc, outcome)

    retstr = retstr.replace("DATA_LABELS_HERE", getNetWorthDataLabels(length))
    retstr = retstr.replace("DATA_SETS_HERE", datastr)

    print retstr

    return retstr

def getNetWorthDataLabels(length):
    retstr = ""

    data = range(0, length)

    for x in data:
        retstr += "\"{}\",".format(x)

    retstr = retstr[:-1]

    return retstr

def getNetWorthDatasets(auc, outcome):
    sortedNames, states = auc.getNetWorth(outcome)
    retstr = ""
    data = []

    for x in xrange(0, len(sortedNames)):
        data.append([item[x] for item in states])

    for x in xrange(0, len(sortedNames)):
        retstr += "{{label: \"{}\", fill:false, borderColor: 'rgb({})',data: [{}]}},".format(sortedNames[x], getLineColor(x), getDataString(data, x))

    retstr = retstr[:-1]

    return len(data[0]), retstr

def getDataString(data, n):
    retstr = ""

    for x in data[n]:
        retstr += "{},".format(x)

    retstr = retstr[:-1]

    return retstr

def getRandomColors(count):
    colors = []
    for i in xrange(count):
        colors.append('{},{},{}'.format(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    return colors

def getLineColor(n):
    colors = ["255,99,132", "120,120,120", "5,36,182", "84,161,83", "63,157,208", "9,76,11", "112,25,125", "149,79,105", "120,237,207", "119,100,10"]

    return colors[n]

def auctionPage(auc):
    retstr = "<!DOCTYPE html><meta charset=\"utf-8\"><html><head><style>table, th, td {border: 1px solid black;}</style><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\"><script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script></head><body><div class=\"container\"><div><h1>AUCTION_TITLE_HERE</h1><hr></div><div><h2>Leaderboard</h2>LEADERBOARD_HERE</div></div></body></html>"

    retstr = retstr.replace("AUCTION_TITLE_HERE", "{}".format(auc.name))
    retstr = retstr.replace("LEADERBOARD_HERE", getLeaderboardTable(auc))

    return retstr

def getLeaderboardTable(auc):

    retstr = "<table class=\"table table-hover\"><thead><tr><th>User</th><th>Balance</th>"

    if auc.isAuctionOpen:
        retstr += "<th>Balance + All Contracts Sold</th>"

    for x in auc.labels:
        retstr += "<th>{}</th>".format(x)

    retstr += "</tr></thead><tbody>"

    for a in auc.accounts:

        bidStr = ''
        for b in a.bids:
            bidStr += "-{},".format(b)
        bidStr = bidStr[:-1]

        cost = auc.getCost(bidStr)

        a.networth = a.balance - cost

    auc.accounts.sort(key=lambda a: a.networth, reverse=True)

    for a in auc.accounts:

        retstr += "<tr><th>{}</th>".format(a.username)
        retstr += "<th>{}</th>".format(a.balance)
        if auc.isAuctionOpen:
            retstr += "<th>{}</th>".format(a.networth)

        for y in a.bids:
            retstr += "<th>{}</th>".format(y)

        retstr += "</tr>"

    retstr += "</tbody></table>"

    return retstr

def helpPage(auc):
    retstr = "<!DOCTYPE html><meta charset=\"utf-8\"><html><head><style>table, th, td {border: 1px solid black;}</style><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\"><script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script></head><body><div class=\"container\"><div><h1>AUCTION_TITLE_HERE</h1></div><hr><div><h2>Help Page</h2><p>Shove a new helpful guide here.</p></div></div></body></html>"

    retstr = retstr.replace("AUCTION_TITLE_HERE", "{}".format(auc.name))

    return retstr
