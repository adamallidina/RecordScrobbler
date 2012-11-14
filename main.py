###############################################################################
#
# Main Module for RecordScrobbeler
#
###############################################################################

import lastfm, audio, echonest, time, ast
from subprocess import check_output, check_call

def main():
  # Make our object instances
  scrobbler = lastfm.session()
  identifer  = echonest.en_session()
  state     = True
  if scrobbler.dataP():
    scrobbler.get_data()
  else:
    scrobbler.auth()
    scrobbler.save_data()
  while state:
    try:
      # TODO Main application loop
      audio.grab_audio('input.wav')
      out      = check_output(['./echoprint-codegen ' 'my_test.wav'], shell=True)
      toparse  = ast.literal_eval(out)
      code     = parse(toparse)
      response = identifier.identify(code)
      title    = response['response']['songs'][0]['title']
      artist   = response['response']['songs'][0]['artist_name']
      scrobbler.scrobble(artist, title)
      print "Scrobbled %s by %s" % (title, artist)
    except:
      # Errors break the program
      state = False

def parse(input):
  """
  Parse will take the string which echoprint-codegen outputs and
  will parse it for the code
  Parameters: a string, output from echoprint-codegen
     Returns: a string, the code from echoprint-codegen
  """
  try:
    code = input[0]['code']
  except:
    


def test():
  # Start a session with last.fm
  last_session = lastfm.session()
  last_session.get_data()
  # Make an song fingerprint object 
  song_id = echonest.en_session()
  print "Audio recording will begin in five seconds"
  time.sleep(5)
  print "Grabbing audio for 20 seconds"
  audio.grab_audio('my_test.wav')
  print "Audio has been grabbed"
  #audio.export_to_raw('my_test.wav', 'my_test.raw')
  out = check_output(['./echoprint-codegen ' 'my_test.wav'], shell=True)
  toparse = ast.literal_eval(out)
  code = toparse[0]['code']
  found = song_id.identify(code)
  song_title = found['response']['songs'][0]['title']
  song_artist = found['response']['songs'][0]['artist_name']
  print song_title
  print song_artist
  last_session.scrobble(song_artist, song_title)

test()
