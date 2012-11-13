###############################################################################
#
# Audio Functions for Record Scrobbler
# Used to record audio from line in and transcode into mp3 format
#
###############################################################################

import pydub, wave, pyaudio, time, os, subprocess

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
  LENGTH   = 30
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

def export_to_mp3(filename, outfile):
  """
  Converts a wave file to mp3, this allows the file to be used with Echo Nest
  Parameters: a string, the name of the file you wish to convert
              a string, the name of the output file
     Returns: none
  """
  file = pydub.AudioSegment.from_wav(filename)
  file.export(outfile, format='mp3')
  clean_up(filename)

def make_raw(filename, outfile):
  args = "-i " + filename + " -ac 1 -ar 22050 -f s16le -t 25 - > " + outfile
  os.system('ffmpeg ' + args)

def clean_up(filename):
  """
  Deletes raw wave files after transcoding to mp3 is complete
  """
  os.remove("./"+filename)

def test():
  grab_audio('test.wav')
  export_to_mp3('test.wav', 'test.mp3')
  make_raw('test.mp3', 'test.raw')
  clean_up('test.mp3')


