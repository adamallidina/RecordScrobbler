###############################################################################
#
# Echo Nest module for RecordScrobbler
# Identifies unknown song
#
###############################################################################

import subprocess, requests
from ConfigParser import SafeConfigParser

test_code  = 'eJyNklGS4yAMBa-EkMD4OAbM_Y-wrx0ztT9TmaTyChF3CzApfT5NPyMy4UQQpSoqo4NoxElcRA_FYDSJm1gKw2f4DJ_hM3xWCHyGz_AZPsNnncBn-AyfrUuLSoQRmcCX8eVCWQl8uTHCly9GncCX8WV8GZ_jc3yOz50IAp_j84PA5_gcn-PzQUziJvAFvsAX-IL1Bb7AF_iC9QW-OAl8IZ_PPrwW85irrjRVTz9mz3dRHdT9VK1Nr3rfxfVQW7NbSSKz6_8Smnz4WdI3XvMP78LPeHj1l_eP_Tdv1TZf2uZntd94L2Ovfx6atHTNvsrQMHLf60_X5s3vzcfqLz_93rzXuvl5bn7V-pXXXYDXfkbqD6_9qIL_nOfDq8_m1efl9d39Rez-4t_-__Hf-ufVdv_O5MPfq_301019eT33nr_W-fP-ytjnP4-8318Zdq3P-ZvVLj6P0XQL1z-QbA2I'
test_code2 = 'eJwtUIuRBSEIawnko5bjovZfwku82xkDJERwRf6-hdMc4I3AshfgS0CR21QPBFUhHICxDGYDfco-vbC1jqwVsw3BDC3mA7CY8WIrZpscHa5vNmxucPhbxZkl1fmWYsmFvDDXT179MNLV5leohwI0GtdyxPCBOiN8gkScEc1MEDNgrdIX84J8UXnP_o9HLV6tNnyzxdyPRRRJ6Du6Ca5T-yJkZil0PLHFB3KWnDHTpGcn2b10z2oz5wbZ5K5Y3a1s2Jkpa105crVLW1-ZDokCKR4pIE22agzR1MIeeEjF6CBDxgWJEeEg4ZMzAxb-R1s_PM1zFg=='


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

  def identify(self, code):
    """
    The identify method will read a songs fingerprint and send it to the Echo
    Nest servers for analysis
    Parameters: a string, the song fingerprint
       Returns: a string, the name of the song
                a string, the songs artist
    """
    url     = 'http://developer.echonest.com/api/v4/song/identify?api_key='
    url     = url + self.api_key + '&code=' + code
    r       = requests.get(url)
    json    = r.json
    #title   = json['response']['songs'][0]['title']
    #artist  = json['response']['songs'][0]['artist_name']
    return json


def test():
  test = en_session()
  print "API KEY: ", test.api_key
  print test.identify(test_code2)

