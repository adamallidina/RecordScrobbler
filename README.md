#Record Scrobbler

Record Scrobbler is in early alpha. It's purpose is to allow last.fm users to scrobble music which they listen to on their turntables.

Record Scrobbler is a work in progress and is barely usable in its current form, the README will be updated as progress is made.

Dependencies:
  * [PyAudio](http://people.csail.mit.edu/hubert/pyaudio)
  * [requests](http://docs.python-requests.org/en/latest/)
  * [Boost](http://www.boost.org/)

##Usage
Currently, you will need an api access key from both last.fm and [Echo Nest](http://developer.echonest.com/docs/v4/) in order to use this application.
Steps to run your own instance
* Clone the repo
* Clone [echoprint-codegen](https://github.com/echonest/echoprint-codegen) into the RecordScrobbler directory
* Build echoprint-codegen, make sure that the file RecordScrobbler/echoprint-codegen exists
* Create a file RecordScrobbler/config.txt which should contain:
```
    [lastfm] 
    api_key = your_last_fm_api_key 
    secret = your_last_fm_secret_key 

    [echonest] 
    api_key = your_echonest_api_key 

* Now just: python main.py

Feel free to contact me at adam(dot)allidina(at)gmail(dot)com with any questions or comments
