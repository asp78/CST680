import numpy

def accountPage(user, auc):
    retstr = "<!DOCTYPE html><meta charset=\"utf-8\"><html><head><style>table, th, td {border: 1px solid black;}</style><script src=\"https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min.js\"></script></head><body><div><h1>AUCTION_TITLE_HERE</h1><hr><h2>USERNAME_HERE Details</h2><h3>Balance: BALANCE_HERE</h3></div><div><h3>Current bid placement</h3>BIDS_TABLE_HERE</div><div><h3>Bid History</h3><div style=\"width: 50%; height: 300px;\"><canvas id=\"myChart\"></canvas></div><script>var ctx=document.getElementById('myChart').getContext('2d');var chart = new Chart(ctx, {type: 'line', data: {labels: [DATA_LABELS_HERE],datasets: [DATA_SETS_HERE]},options: {}});</script></div></body></html>"

    retstr = retstr.replace("AUCTION_TITLE_HERE", "{}".format(auc.name))
    retstr = retstr.replace("USERNAME_HERE", "{}".format(user.username))
    retstr = retstr.replace("BALANCE_HERE", "{}".format(user.balance))
    retstr = retstr.replace("BIDS_TABLE_HERE", "{}".format(getUserBidsTable(user, auc)))
    retstr = retstr.replace("DATA_LABELS_HERE", getDataLabels(user))
    retstr = retstr.replace("DATA_SETS_HERE", getDatasets(user, auc))

    print retstr

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
