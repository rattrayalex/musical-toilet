import soundcloud
import pygst, gst
import time
from threading import Thread

class SoundStreamer:
  def __init__(self):
    self.client = soundcloud.Client(client_id='045b8c0a4960cce57af82f215695fb3b')
    self.playlist = [
      36247624,  # party-pants
      # 36894638,  # party-pants-1
      37662755,  # party-pants-2
      38415258,  # party-pants-3
      40651214,  # party-pants-6
      42484028,  # party-pants-8
      46637250,  # party-pants-9
      46639797,  # party-pants-10
      61522767,  # party-pants-12
      71527983,  # party-pants-13
      71533432,  # party-pants-14
    ]
    self.playlist_urls = []
    self.playlist_permalinks = []
    playlist_loader = Thread(target=self.load_track_urls)
    playlist_loader.daemon = True
    playlist_loader.start()
    self.current_track = 0

    #creates a playbin (plays media form an uri) 
    self.player = gst.element_factory_make("playbin", "player")


  # Credit the uploader as the creator of the sound
  # Credit SoundCloud as the source by including one of the logos found here
  # Link to the SoundCloud URL containing the work
  # If the sound is private link to the profile of the creator

  def load_track_urls(self):
    for t in self.playlist:
      stream_url, permalink_url = self.get_track_url(t)
      self.playlist_permalinks.append(permalink_url)
      self.playlist_urls.append(stream_url)

  def get_track_url(self, track):
    try:
      track = self.client.get('/tracks/%s' % track)
    except:
      pass
    stream_url = self.client.get(track.stream_url, allow_redirects=False)
    print stream_url.location
    return stream_url.location, track.permalink_url

  # no idea what this does
  def on_tag(self, bus, msg):
    taglist = msg.parse_tag()
    print 'on_tag:'
    for key in taglist.keys():
      print '\t%s = %s' % (key, taglist[key])

  def play(self):
    url = self.current_track_url()
    #set the uri
    self.player.set_property('uri', url)

    #start playing
    self.player.set_state(gst.STATE_PLAYING)

    #listen for tags on the message bus; tag event might be called more than once
    bus = self.player.get_bus()
    bus.enable_sync_message_emission()
    bus.add_signal_watch()
    bus.connect('message::tag', self.on_tag)

    print 'playing'

  def stop(self):
    self.player.set_state(gst.STATE_NULL)

  def resume(self):
    self.player.set_state(gst.STATE_PLAYING)
    print 'playing'

  def pause(self):
    self.player.set_state(gst.STATE_PAUSED)
    print 'paused'

  def current_track_url(self):
    return self.playlist_urls[self.current_track]

  def current_track_permalink(self):
    return self.playlist_permalinks[self.current_track]

  def next(self):
    self.current_track += 1
    self.stop()
    self.play()

  def play_pause_tester(self):
    self.play()
    for i in range(len(self.playlist) - 1):
      time.sleep(5)
      self.next()

    print 'done'


def main():
  ss = SoundStreamer()
  # tracks = ss.get_artist_songs('dj-sampo')
  # url = ss.get_track_url(tracks[0])
  ss.play_pause_tester()

if __name__ == '__main__':
  main()