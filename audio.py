###############################################################################
#
# Audio Functions for Record Scrobbler
# Grabs audio from line in, saves it to a wav file
#
###############################################################################

import pydub, wave, pyaudio, os

def grab_audio(filename):
  """
  The grab_audio function will use the pyaudio library to record audio from
  the line in of the computer and will save it in WAVE format
  Parameters: a string, the name of the file you wish to save the wav file out
              to
     Returns: none
  """
  # Constants needed
  CHUNK    = 1024
  FORMAT   = pyaudio.paInt16
  CHANNELS = 2
  RATE     = 44100
  LENGTH   = 21
  OUTPUT   = filename
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

def clean_up(filename):
  """
  Deletes filename
  Parameters: a string, name of the file you wish to delete
     Returns: none
  """
  os.remove("./"+filename)
