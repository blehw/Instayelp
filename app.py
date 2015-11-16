import urllib2,json,module
import argparse
import pprint
import sys
import urllib
import oauth2

from instagram import client, subscriptions

from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)

###################### YELP ##########################

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

CONSUMER_KEY = "4UflM-LI7bHtQCXO1mKyBA"
CONSUMER_SECRET = "xVusSoHSNz8ryufxsgWqCJmqv-c"
TOKEN = "M0JTrZ1-LTJHy9QKcCoKUVdxKi8p2WpW"
TOKEN_SECRET = "-cIRMwr9TDs17AO4PahF2HB2bDM"


def requestf(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response


def search(term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return requestf(API_HOST, SEARCH_PATH, url_params=url_params)


def get_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return requestf(API_HOST, business_path)

@app.route("/", methods=["GET","POST"])
def index():
	"""
	Main Page of Website
 	Prompts the user to chose a food and location
	"""
	if request.method=="POST":
            button = request.form['button']
            food = request.form['type']
            location =request.form['location']
            if button=="Find":
		return query_api(term=food, location=location);
            else:
                return "bye"
   	else:
            return render_template("home.html")

@app.route("/<term>/<location>")

def query_api(term="tacos", location="brooklyn"):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query. Will return JSON from Instagram of posts tagged with this term.
        location (str): The location of the business to query.
    """
    message = ""
    if "business_at_location" not in session:
    	session['business_at_location'] = True
	if not session['business_at_location']:
		message = "No business at this location"
		session["business_at_location"] = True
    response = search(term, location)
	#response = search("pizza", "krpslpo");
    businesses = response.get('businesses')
	
    #Yelp part:
    if not businesses:
        print u'No businesses for {0} in {1} found.'.format(term, location)
        session["bussiness_at_location"] = False
        return render_template("tacos.html")
    business_id = businesses[0]['id']

    print u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id)
    response = get_business(business_id)

    print u'Result for business "{0}" found:'.format(business_id)
    
    #Instagram part:
    access_token = session['insta_access_token']
    api = client.InstagramAPI(access_token = access_token, client_secret = CONFIG['client_secret'])
    tag_search, next_tag = api.tag_search(q = term)
    tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)
    photos = []
    for tag_media in tag_recent_media:
        photos.append(tag_media.get_standard_resolution_url())
    return render_template("tacos.html", r=response, m=message, c=photos, t=term, l=location)


####################  INSTAGRAM  #######################
###Instagram Keys

CONFIG = {
    'client_id': '1500207b59d34a87a53120d33e56c041',
    'client_secret': '41ede89cba7e44ecb604fce95f444672',
    'redirect_uri': 'http://localhost:8000/oauth',
}
api = client.InstagramAPI(**CONFIG)

@app.route('/instagram')
def instagram():
    '''To receive instagram access code'''
    if 'insta_access_token' not in session:
        return redirect('/conn')
    else:
        return redirect('/')

@app.route('/conn')
def main():
    '''Redirect from /instagram to get access code'''
    url = api.get_authorize_url(scope=["likes", "comments"])
    return redirect(url)

@app.route('/oauth')
def oauth():
    code = request.args.get('code')
    access_token, user = api.exchange_code_for_access_token(code)
    if not access_token:
        return 'no access token'
    app.logger.debug('got an access token')
    app.logger.debug(access_token)

    session['insta_access_token'] = access_token
    session['insta_user'] = user
    return redirect('/')

if __name__=="__main__":
    app.secret_key = "My name is Taco"
    app.debug=True
    app.run(host='0.0.0.0',port=8000)
