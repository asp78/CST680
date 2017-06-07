import numpy

def accountPage(user, auc):
    retstr = "<!DOCTYPE html><meta charset=\"utf-8\"><html><head><style>table, th, td {border: 1px solid black;}</style><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script></head><body><div><h1>AUCTION_TITLE_HERE</h1><hr><h2>USERNAME_HERE Details</h2><h3>Balance: BALANCE_HERE</h3></div><div><h3>Current bid placement</h3>BIDS_TABLE_HERE</div><div><h3>Place a new bet</h3>BET_FORM_HERE</div><div><h3>Bid History</h3><div style=\"width: 50%; height: 300px;\"><canvas id=\"myChart\"></canvas></div><script>var ctx=document.getElementById('myChart').getContext('2d');var chart = new Chart(ctx, {type: 'line', data: {labels: [DATA_LABELS_HERE],datasets: [DATA_SETS_HERE]},options: {scales:{yAxes:[{ticks:{stepSize:1}}]}}});</script></div></body></html>"

    retstr = retstr.replace("AUCTION_TITLE_HERE", "{}".format(auc.name))
    retstr = retstr.replace("USERNAME_HERE", "{}".format(user.username))
    retstr = retstr.replace("BALANCE_HERE", "{}".format(user.balance))
    retstr = retstr.replace("BIDS_TABLE_HERE", "{}".format(getUserBidsTable(user, auc)))
    retstr = retstr.replace("DATA_LABELS_HERE", getDataLabels(user))
    retstr = retstr.replace("DATA_SETS_HERE", getDatasets(user, auc))
    retstr = retstr.replace("BET_FORM_HERE", getBetForm(user, auc))

    return retstr

def getBetForm(user, auc):
    retstr = "<table><tr><th>Bin</th>"

    for x in auc.labels:
        retstr += "<th>{}</th>".format(x)

    retstr += "</tr><tr><th></th>"

    for x in range(0, auc.numBins):
        retstr += "<th><input id=\"trade{}\" type=\"text\" name=\"{}\" style=\"width:20px;\" value=\"0\"></th>".format(x,x)

    retstr += "</tr></table><button type=\"button\" onClick=\"makeTrade()\">Trade</button><script>function makeTrade(){if (CONDITION_HERE){var url=window.location.href;url=url.replace(\"status\",\"makeTrade\"); url += GET_ELEMENTS_HERE;$.ajax({url: url, success: function(result){window.location.reload(true);}});}}</script><button type=\"button\" onClick=\"checkPrice()\">Check Price</button><script>function checkPrice(){var url=window.location.href; url=url.substring(0,url.lastIndexOf(\"/\"));url=url.substring(0,url.lastIndexOf(\"/\"));url=url.replace(\"status\",\"getCost\");url+= \"/\" + GET_ELEMENTS_HERE;$.ajax({url: url, success: function(result){$(\"#tradeCost\").html('Cost: ' + result);}});}</script><p id=\"tradeCost\">Cost: </p>"

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
    retstr = "<table><tr><th>Bin</th>"

    for x in auc.labels:
        retstr += "<th>{}</th>".format(x)

    retstr += "</tr><tr><th>Count</th>"

    for x in user.bids:
        retstr += "<th>{}</th>".format(x)

    retstr += "</tr></table>"

    return retstr

def getDataLabels(user):
    retstr = ""

    labels = range(0, len(user.bidHistory))
    #labels = range(0, 8)

    for x in labels:
        retstr += "\"{}\",".format(x)

    retstr = retstr[:-1]

    return retstr

def getDatasets(user, auc):
    data = []
    retstr = ""

    for x in xrange(0, user.bids.size):
        data.append([item[x] for item in user.bidHistory])

    for x in xrange(0, user.bids.size):
        retstr += "{{label: \"{}\", fill:false, borderColor: 'rgb({})',data: [{}]}},".format(auc.labels[x], getLineColor(x), getDataString(data, x))

    retstr = retstr[:-1]

    return retstr

def getDataString(data, n):
    retstr = ""

    for x in data[n]:
        retstr += "{},".format(x)

    retstr = retstr[:-1]

    return retstr

def getLineColor(n):
    colors = ["255,99,132", "120,120,120", "5,36,182", "84,161,83", "63,157,208", "9,76,11", "112,25,125", "149,79,105", "120,237,207", "119,100,10"]

    return colors[n]

def auctionPage(auc):
    retstr = "<!DOCTYPE html><meta charset=\"utf-8\"><html><head><style>table, th, td {border: 1px solid black;}</style><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script></head><body><div><h1>AUCTION_TITLE_HERE</h1></div><div><h2>Leaderboard</h2>LEADERBOARD_HERE</div><hr></body></html>"

    retstr = retstr.replace("AUCTION_TITLE_HERE", "{}".format(auc.name))
    retstr = retstr.replace("LEADERBOARD_HERE", getLeaderboardTable(auc))

    return retstr

def getLeaderboardTable(auc):
    retstr = "<table><tr><th>User</th><th>Balance</th>"

    for x in auc.labels:
        retstr += "<th>{}</th>".format(x)

    retstr += "</tr>"

    for x in auc.accounts:
        retstr += "<tr><th>{}</th>".format(x.username)
        retstr += "<th>{}</th>".format(x.balance)

        for y in x.bids:
            retstr += "<th>{}</th>".format(y)

        retstr += "</tr>"

    retstr += "</table>"

    return retstr

def helpPage(auc):
    retstr = "<!DOCTYPE html><meta charset=\"utf-8\"><html><head><style>table, th, td {border: 1px solid black;}</style><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script></head><body><div><h1>AUCTION_TITLE_HERE</h1></div><hr><div><h2>Help Page</h2><p>Shove a new helpful guide here.</p></div></body></html>"

    retstr = retstr.replace("AUCTION_TITLE_HERE", "{}".format(auc.name))

    return retstr
