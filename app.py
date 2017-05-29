from flask import Flask

from lsmr import lsmr

app = Flask(__name__)

@app.route('/')
def home_page():
    return 'LMSR FLASK APP'

@app.route('/getPrices/', methods=['GET'])
def getPrices():
    status = 200
    return str(lsmr.getPrices())

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=False, threaded=True)
    except Exception as e:
        print "{}".format(e)
