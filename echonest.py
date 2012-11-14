###############################################################################
#
# Echo Nest module for RecordScrobbler
# Used to pass song fingerprint to EchoNest api and the songs name and artist
#
###############################################################################

import subprocess, requests
from ConfigParser import SafeConfigParser

class en_session(object):
  """
  An en_session instance is an authenticated session to Echo Nest. It allows
  for the fingerprinting of abitrary songs
  """

  def __init__(self):
    # Grab api key and secret key from config.txt
    parser = SafeConfigParser()
    parser.read('config.txt')
    self.api_key = parser.get('echonest', 'api_key')

  def identify(self, code):
    """
    The identify method will read a songs fingerprint and send it to the Echo
    Nest servers for analysis
    Parameters: a string, the song fingerprint
       Returns: The json response of the request from Echo Nest
    """
    url     = 'http://developer.echonest.com/api/v4/song/identify?api_key='
    url     = url + self.api_key + '&version=4.12' + '&code=' + code
    r       = requests.get(url)
    json    = r.json
    return json

  def get_length(self, songid):
    """
    The get_length method returns the length of the song as an int
    """
    url      = 'http://developer.echonest.com/api/v4/song/profile?api_key='
    url      = url + self.api_key + '&format=json' + '&id=' + songid + '&bucket'
    url      = url + '=audio_summary'
    response = requests.get(url)
    json     = response.json
    return int(json['response']['songs'][0]['audio_summary']['duration'])




