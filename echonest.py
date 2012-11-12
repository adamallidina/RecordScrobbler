###############################################################################
#
# Echo Nest module for RecordScrobbler
# Identifies unknown song
#
###############################################################################

import subprocess, requests
from ConfigParser import SafeConfigParser

test_code = eJwzMAACY2OT5BQgAQATRALs


class en_session(object):
  """
  An en_session instance is an authenticated session to Echo Nest. It allows
  for the fingerprinting of abitrary songs
  """

  def __init__(self):
    # Grab api key and secret key from config.txt
    parser = SafeConfigParser()
    parser.read('config.txt')
    self.secret  = parser.get('echonest', 'secret')
    self.api_key = parser.get('echonest', 'api_key')

  def identify(code):
    """
    The identify method will read a songs fingerprint and send it to the Echo
    Nest servers for analysis
    Parameters: a string, the song fingerprint
       Returns: a string, the name of the song
                a string, the songs artist
    """
    url     = 'http://developer.echonest.com/api/v4/song/identify'
    query   = '@json_string.json'
    payload = {'api_key=': self.api_key, 'query=': query, 'code=': song}
    r       = requests.get(url, data=payload)
    print r.text


def test():
  test = en_session()

