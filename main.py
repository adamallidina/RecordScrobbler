###############################################################################
#
# Main Module for RecordScrobbeler
#
###############################################################################

import lastfm, audio, echonest, time, ast
from subprocess import check_output, check_call

# FFMPEG Conversion: test.mp3 -ac 1 -ar 22050 -f s16le -t 20 -ss 10 -> test.raw

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

def test2():
  song_id = echonest.en_session()
  code = check_output(['./TEST ' 'billie.raw'], shell=True)
  found = song_id.identify(code)
  print found

test()
