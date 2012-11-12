###############################################################################
#
# Main function for Record Scrobbler
#
###############################################################################

import lastfm, pydub, wave, pyaudio

def grab_audio():
  """
  The grab_audio function will use the pyaudio library to record audio from
  the line in of the computer and will save it in WAVE format
  """
  # Constants needed
  CHUNK    = 1024
  FORMAT   = pyaudio.paInt16
  CHANNELS = 2
  RATE     = 44100
  LENGTH   = 30
  OUTPUT   = "out.wav"
  record   = pyaudio.PyAudio()
  stream   = record.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                         input=True, frames_per_buffer=CHUNK)
  frames   = []
  # Recording
  for i in range(0, int(RATE / CHUNK * LENGTH)):
    data = stream.read(CHUNK)
    frames.append(data)
  # Cleanup
  stream.stop_stream()
  stream.close()
  record.terminate()
  # Write to file
  file = wave.open(OUTPUT, 'wb')
  file.setnchannels(CHANNELS)
  file.setsampwidth(record.get_sample_size(FORMAT))
  file.setframerate(RATE)
  file.writeframes(b''.join(frames))
  file.close

grab_audio()
