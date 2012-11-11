###############################################################################
#
# LastFM Module for RecordScrobbler
# // todo description
#
###############################################################################

import requests, webbrowser, hashlib, time
from ConfigParser import SafeConfigParser

class session(object):

  """
  An instance of a session object represents all facilities needed in order for
  the program to scrobble music to last.fm via their api
  """

  def __init__(self):
    """
    The __init__ method sets all required variables for authentication and
    requests to the last.fm api
    """
    self.apiKey      = "021ab74b3f5405138a23c42b8ff1c746"
    self.predicate   = "http://ws.audioscrobbler.com/2.0/?method="
    self.token       = self.get_token()
    self.signature   = self.get_signature("auth.getSession")
    self.session_key = None

  def get_token(self):
    """
    The get_token method makes a request to the last.fm api and fetches an
    authentication token in json format.

    Parameters: none
       Returns: a string containing the token, which has been parsed from the
                json response
    """
    url       = self.predicate + "auth.gettoken&api_key="
    url       = url + self.apiKey + "&format=json"
    response  = requests.get(url)
    json      = response.json
    token     = json['token']
    return token

  def get_signature(self, method):
    """
    The get_signature method is used to generate the md5 version of the
    application signature; which is used to sign all last.fm api requests.

    Parameters: a string containing the name of the last.fm api request 
                which will be signed
       Returns: a string containing the md5 hexadecimal hash of our signature
                string; this is what we sign requests with
    """
    # Get secret key from config file
    parser  = SafeConfigParser()
    parser.read('config.txt')
    secret  = parser.get('secret', 'key')
    # The string that needs to be hashed, as specified by last.fm docs
    tohash  = "api_key" + self.apiKey + "method" + method
    tohash  = tohash + "token" + self.token + secret
    hashobj = hashlib.md5(tohash)
    return hashobj.hexdigest()

  def auth(self):
    """
    The auth method is called in order to authenticate a session with a user
    Sets self.session_key to a session key obtained from last.fm after
    the user gives the app permission
    Parameters: none
       Returns: none
    """
    # Open up users default web browser to last.fm authentication page
    url = "http://www.last.fm/api/auth/?api_key="
    webbrowser.open(url + self.apiKey + "&token=" + self.token)
    time.sleep(10)
    # Now we need to grab a session key
    call     = self.predicate + "auth.getSession&api_key=" + self.apiKey
    call     = call + "&token=" + self.token + "&api_sig=" + self.signature
    call     = call + "&format=json"
    response = requests.get(call)
    json     = response.json
    session_key      = json['session']['key']
    self.session_key = session_key

def test():
  test_session = session()
  test_session.auth()

