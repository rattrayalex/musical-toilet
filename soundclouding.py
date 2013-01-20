import soundcloud
import pygst, gst
import time

class SoundStreamer:
  def __init__(self):
    self.client = soundcloud.Client(client_id='045b8c0a4960cce57af82f215695fb3b')
    #creates a playbin (plays media form an uri) 
    self.player = gst.element_factory_make("playbin", "player")

  def get_artist_songs(self, artist):
    artist_id = self.client.get('/users', q=artist)[0].id
    tracks = self.client.get('/tracks', user_id=artist_id)
    tracks.sort(key = lambda t: -t.playback_count)
    for t in tracks: print t.download_count, t.playback_count, t.permalink
    return tracks

  def get_track_url(self, track):
    # track = self.client.get('/tracks/%s' % track_id)
    stream_url = self.client.get(track.stream_url, allow_redirects=False)
    print stream_url.location
    return stream_url.location

  # no idea what this does
  def on_tag(self, bus, msg):
    taglist = msg.parse_tag()
    print 'on_tag:'
    for key in taglist.keys():
      print '\t%s = %s' % (key, taglist[key])

  def play(self, url):
    #set the uri
    self.player.set_property('uri', url)

    #start playing
    self.player.set_state(gst.STATE_PLAYING)
    print 'playing'

    #listen for tags on the message bus; tag event might be called more than once
    bus = self.player.get_bus()
    bus.enable_sync_message_emission()
    bus.add_signal_watch()
    bus.connect('message::tag', self.on_tag)

  def resume(self):
    self.player.set_state(gst.STATE_PLAYING)
    print 'playing'

  def pause(self):
    self.player.set_state(gst.STATE_PAUSED)
    print 'paused'

def play_pause_tester(ss, url):
  ss.play(url)
  time.sleep(5)
  ss.pause()
  time.sleep(5)
  ss.resume()
  time.sleep(5)
  print 'done'


def main():
  ss = SoundStreamer()
  tracks = ss.get_artist_songs('dj-sampo')
  url = ss.get_track_url(tracks[0])
  play_pause_tester(ss, url)

if __name__ == '__main__':
  main()