import urllib2,json,module
from flask import Flask, render_template

app = Flask(__name__)

CONSUMER_KEY = "4UflM-LI7bHtQCXO1mKyBA"
CONSUMER_SECRET = "xVusSoHSNz8ryufxsgWqCJmqv-c"
TOKEN = "M0JTrZ1-LTJHy9QKcCoKUVdxKi8p2WpW"
TOKEN_SECRET = "-cIRMwr9TDs17AO4PahF2HB2bDM"

@app.route("/<tag")
def search(tag=""):
    url = """
