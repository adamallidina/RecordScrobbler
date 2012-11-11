###############################################################################
#
# LastFM Module for RecordScrobbler
# // todo description
#
###############################################################################

import requests, webbrowser, hashlib
from ConfigParser import SafeConfigParser

class session(object):

  """
  An instance of a session object represents all facilities needed in order for
  the program to scrobble music to last.fm via their api
  """

  def __init__(self):
    self.apiKey    = "021ab74b3f5405138a23c42b8ff1c746"
    self.predicate = "http://ws.audioscrobbler.com/2.0/?method=auth.gettoken"
    self.token     = self.gettoken()
    self.signature = self.getsignature()

  def gettoken(self):
    url       = self.predicate + "&api_key=" + self.apiKey + "&format=json"
    response  = requests.get(url)
    json      = response.json
    token     = json['token']
    return token

  def getsignature(self):
    # Get secret key from config file
    parser  = SafeConfigParser()
    parser.read('config.txt')
    secret  = parser.get('secret', 'key')
    # The string that needs to be hashed, as specified by last.fm docs
    tohash  = "api_key" + self.apiKey + "methodauth.getSessiontoken" + secret
    hashobj = hashlib.md5(tohash)
    return hashobj.hexdigest()

  def auth(self):
    predicate = "http://www.last.fm/api/auth/?api_key="
    # Open up users default web browser to last.fm authentication page
    webbrowser.open(predicate + self.apiKey + "&token=" + self.token)
    # Now we need to grab a session key

