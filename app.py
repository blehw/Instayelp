import urllib2,json,module
from flask import Flask, render_template

app = Flask(__name__)

API_HOST = 'api.yelp.com'
SEARCH_PATH = '/v2/search/'

@app.route("/tacos")
def search(tag="tacos"):

    url_params = {
    'tag':tag.replace(' ', '+'),
    }

    return module.request(API_HOST, SEARCH_PATH, url_params=url_params)

if __name__=="__main__":
    app.debug=True
    app.secret_key = "My name is Ted"
    app.run(host='0.0.0.0',port=8000)
