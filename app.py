from flask import Flask
from flask import Response

from lsmr import lsmr

app = Flask(__name__)

@app.route('/')
def home_page():
    return 'LMSR FLASK APP'

@app.route('/getPrices/', methods=['GET'])
def getPrices():
    status = 200
    return lsmr.getPrices()
