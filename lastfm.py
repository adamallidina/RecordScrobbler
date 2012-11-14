###############################################################################
#
# LastFM Module for RecordScrobbler
# Used for scrobbling identified tracks to last.fm
#
###############################################################################

import requests, webbrowser, hashlib, time, shelve
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

  def get_signature(self, tosort):
    """
    The get_signature method is used to generate the md5 version of the
    application signature; which is used to sign all last.fm api requests.

    Parameters: a dictionary of all keys and values to be put into the string
       Returns: a string containing the md5 hexadecimal hash of our signature
                string; this is what we sign requests with
    """
    # Get secret key from config file
    parser  = SafeConfigParser()
    parser.read('config.txt')
    secret  = parser.get('secret', 'key')
    # We need to produce the string which needs to be hashed
    # The string must be an alphabetized version of the request will be sending
    # to the last.fm api
    list = tosort.items()
    list.sort()
    tohash = ""
    while list != []:
      tup    = list.pop(0)
      tohash = tohash + tup[0] + tup[1]
    # Now we hash the string
    tohash  = tohash + secret
    hashobj = hashlib.md5(tohash)
    return hashobj.hexdigest()

  def web_auth(self):
    """
    The web_auth method simply opens the users web browser to the last.fm
    permissions page. Will be made much more robust after basic all basic
    functionaliy is implemented
    Parameters: none
       Returns: none
    """
    print "We need your permission to continue"
    print "Opening your default web browser..."
    url = "http://www.last.fm/api/auth/?api_key="
    webbrowser.open(url + self.apiKey + "&token=" + self.token)
    time.sleep(10)

  def auth(self):
    """
    The auth method is called in order to authenticate a session with a user
    Sets self.session_key to a session key obtained from last.fm after
    the user gives the app permission
    Parameters: none
       Returns: none
    """
    self.web_auth()
    # Get the signature of our request for auth.getSession
    sig_dict = {'api_key': self.apiKey, 'method': 'auth.getSession', 'token': self.token}
    signature = self.get_signature(sig_dict)
    # Now we need to grab a session key
    call     = self.predicate + "auth.getSession&api_key=" + self.apiKey
    call     = call + "&token=" + self.token + "&api_sig=" + signature
    call     = call + "&format=json"
    response = requests.get(call)
    json     = response.json
    session_key      = json['session']['key']
    self.session_key = session_key

  def save_data(self):
    """
    The save_data method stores all the information needed to make last.fm api
    calls without reauthenticating every time. 
    Parameters: none
       Returns: none
    """
    storage = shelve.open('data')
    # All we need to store is the session key
    storage['0'] = self.session_key
    storage.close()

  def get_data(self):
    """
    The get_data method will retrieve the data stored by shelf and set our
    class instance self.session_key to what has been stored. To be used
    after auth() has been run sucessfully at least once
    Parameters: none
       Returns: none
    """
    storage          = shelve.open('data')
    self.session_key = storage['0']
    storage.close()

  def scrobble(self, artist, track):
    """
    The scrobble method scrobbles a song to last.fm
    Parameters: a string, name of the artist being scrobbled
                a string, name of the track being scrobbled
       Returns: none
    """
    # Setup all the required info
    root          = "http://ws.audioscrobbler.com/2.0/"
    timestamp     = int(time.time())
    str_timestamp = str(timestamp)
    sig_dict      = {'api_key': self.apiKey, 'method': 'track.scrobble',
                     'artist': artist, 'track': track,
                     'timestamp': str_timestamp, 'sk': self.session_key}
    sig           = self.get_signature(sig_dict)
    # Contents of the POST request to last.fm
    payload  = {'method': 'track.scrobble', 'artist': artist, 'track': track,
                'timestamp': timestamp, 'api_key': self.apiKey,
                'api_sig': sig, 'sk': self.session_key}
    # Away we go!
    requests.post(root, data=payload)
