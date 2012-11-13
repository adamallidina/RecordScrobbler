###############################################################################
#
# Main Module for RecordScrobbeler
#
###############################################################################

import lastfm, audio, echonest, time
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
  print "Grabbing audio for 30 seconds"
  audio.grab_audio('my_test.wav')
  print "Audio has been grabbed"
  audio.export_to_mp3('my_test.wav', 'my_test.mp3')
  audio.make_raw('my_test.mp3', 'my_test.raw')
  code = check_output(['./CODEGEN ' 'my_test.raw'], shell=True)
  found = song_id.identify(code)
  print found

def test2():
  song_id = echonest.en_session()
  code = check_output(['./CODEGEN ' 'billie.raw'], shell=True)
  found = song_id.identify(code)
  print found

test()


