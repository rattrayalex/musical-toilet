import SimpleCV
import time, sys, os, argparse
from datetime import datetime
from collections import Counter
import soundclouding
from twitter import TwitterAPI
from threading import Thread

class PeeCam:

  def __init__(self, cam=1):
    self.cam = SimpleCV.Camera(cam)
    self.disp = SimpleCV.Display()
    self.history = []
    self.status = 'first_off'
    self.sidetime = 0
    self.ss = soundclouding.SoundStreamer()
    self.starttime = None
    self.sent_tweet = False
    self.twitter_un = None

  def run(self, func=None, action=None, dirname=None, show=False,
          twitter_un=None):
    self.twitter_un = twitter_un
    if not action == 'load':
      self.warmup_webcam()

    if action == 'record':
      try:
        os.mkdir(dirname)
      except:
        print 'could not make dir'
        exit()

    i = 0
    orig = None
    dark_slice = None
    while self.disp.isNotDone():
      if self.disp.mouseLeft:
        break
      if action == 'load':
        img = SimpleCV.Image('%s/%s.jpg' % (dirname, i))
      else:
        img = self.cam.getImage()

      if func: # diff
        if not orig:
          print 'not orig'
          dark_blob, orig, dark_matrix = get_dark_slice(img)
          print 'got the dark stuff'

        if not show:
          self.diffinator(img, orig, dark_blob, dark_matrix)
        else:
          img = self.diffinator(img, orig, dark_blob, dark_matrix)
        
        self.set_status()
      
      img.save(self.disp)

      if action == 'record':
        img.save('%s/%s.jpg' % (dirname, i))

      i += 1

    return

  def warmup_webcam(self):
    for i in range(5):
      img = self.cam.getImage()

  def diffinator(self, img, orig, dark_blob, dark_matrix):
    img = img.crop(dark_blob)
    diff = SimpleCV.Image(img.getNumpy() * dark_matrix) - orig
    ydiff = diff.colorDistance(SimpleCV.Color.YELLOW)
    ydiff = ydiff.invert()
    ydiff *= 25
    xval = localize(ydiff)
    self.history.append(xval)
    return ydiff

  def set_status(self):
    print '                    ', self.status
    history_len = 10
    recent = self.history[-history_len:]
    numbers = filter(lambda x: x is not None, recent)
    if self.status in ['share', 'next']: 
      self.sidetime += 1
    if not self.status in ['on'] and self.sidetime > 30:
      self.status = 'off'
      self.ss.pause()
    if len(numbers) < history_len / 2:
      if self.status is 'on':
        self.status = 'off'
        self.ss.pause()
        self.sidetime = 0
        # print '======       TURNING OFF'
        return
      else:
        # print '======       NOT TURNING OFF'
        return
    elif self.status == 'first_off':
      self.status = 'on'
      # print '======       TURNING OOOONNNNNNNNNNN'
      self.ss.play()
      self.sidetime = 0
      self.starttime = datetime.now()
      return
    elif self.status == 'off':
      # print '======       RESSUUUUUUUUUUUUUMMMMEE'
      self.status = 'on'
      self.ss.resume()
      self.sent_tweet = False
      self.sidetime = 0
      self.starttime = datetime.now()
      return

    avg = sum(numbers) / float(len(numbers))
    if avg < 20:
      if self.status != 'next':
        self.status = 'next'
        # print '======       NEEEEEEEEEEEEEEEEEEEEEEXXXXXXXXXXXXXXXXXTTTTTTTT'
        self.ss.next()
        return
      else:
        return
    elif 20 <= avg <= 80:
      self.status = 'on'
      self.sidetime = 0
      # print '======       ON'
      return
    elif avg > 80:
      self.status = 'share'
      if not self.sent_tweet:
        tweet_worker = Thread(target=self.tweet)
        tweet_worker.daemon = True
        tweet_worker.start()
        self.sent_tweet = True

      # print '======       SHAAARRRRRRRRRRRRRRRRIIIIIIIIIIIIIIIINNGG!!!!'
      return

  def tweet(self):
    try:
      twitter = TwitterAPI()
      sec = (datetime.now() - self.starttime).seconds
      soundcloud_link = self.ss.current_track_permalink()
      if not sec < 3:

        if self.twitter_un:
          twitter.tweet(
            '@%s just peed for %d seconds while jamming to %s' % (
              self.twitter_un, sec, soundcloud_link))
        else:
          twitter.tweet('Just peed for %d seconds while jamming to %s' % (
              sec, soundcloud_link))
    except Exception, e:
      print 'could not tweet: ', e

def matrix_avgs(m, n=5):
  slice_avgs = []
  w = len(m) / n
  h = len(m[0])
  for i in range(n):
    a, b = i*w, (i+1)*w
    mean = m[a:b, 0:(h/2)].mean()
    slice_avgs.append(mean)
  return slice_avgsid

def localize(img):
  # img = img.invert()
  blobs = img.findBlobs(threshval=254, minsize=15)

  try:
    blobs.draw()
    # blobs = filter(lambda b: b.mArea > 500, blobs)
    blobs.sort(key=lambda b: -b.mArea)
    blob = blobs[0]
  except Exception, e:
    print 'could not sort'
    return None
  
  # aspect_ratio = blob.width() / float(blob.length())
  # print aspect_ratio

  area = blob.mArea
  print '                                          ', area
  if area < 20:
    print 'too small', area
    return None
  blob.draw()
  left_x = blob.topLeftCorner()[0]
  right_x = blob.topRightCorner()[0]
  avg_x = sum([left_x, right_x]) / 2.
  percent = int(round((avg_x / img.width) * 100))
  print percent
  return percent

def get_dark_slice(img):
  p = img.getPalette()
  print 'got palette'
  darkest = sorted(p, key = lambda r: sum(r))
  print 'sorted out darkest'
  blobs = img.findBlobsFromPalette(darkest[:3], minsize=300)
  print 'found blobs'
  blobs.sort(key=lambda b: -b.mArea)
  print 'sorted blobs'
  dark_blob = blobs[0]
  dark_slice = dark_blob.blobImage()
  # dark_slice =dark_slice.crop(x=0, y=0, w=dark_slice.width, h=min(250, dark_slice.height))
  matrix = dark_slice.getNumpy()
  for col in range(len(matrix)):
    for row in range(len(matrix[col])):
      for c in range(len(matrix[col][row])):
        if matrix[col][row][c] > 0:
          matrix[col][row][c] = 1
  print 'done with the beast'
  return dark_blob, dark_slice, matrix


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--record', metavar='dirname', help="record imgs to dirname")
  parser.add_argument('--play', help="play live without recording", action='store_true')
  parser.add_argument('--diff', help="diff it lolz", action='store_true')
  parser.add_argument('--show', help="SHOW THAT DIFF lolz", action='store_true')
  parser.add_argument('--load', metavar='dirname', help="load and play imgs from dirname")
  parser.add_argument('--twitter', help="The Twitter handle to tweet at.")
  pargs = parser.parse_args()

  if pargs.diff:
    func = True
  else:
    func = False

  pc = PeeCam()

  if pargs.record:
    pc.run(action='record', dirname=pargs.record)
  elif pargs.load:
    pc.run(func=func, action='load', dirname=pargs.load, show=pargs.show,
           twitter_un=pargs.twitter)
  else:
    pc.run(func=func, show=pargs.show, twitter_un=pargs.twitter)

if __name__ == '__main__':
  main()
