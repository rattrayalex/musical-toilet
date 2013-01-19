#!/usr/bin/python
import SimpleCV
import time, sys, os, argparse

cam = SimpleCV.Camera(0)
disp = SimpleCV.Display()
prev = None

def load_play(dirname, func=None):
  i = 0

  while disp.isNotDone():
    if disp.mouseLeft:
      break
    img = SimpleCV.Image('%s/%s.jpg' % (dirname, i))
    if func:
      img = func(img)
    img.save(disp)
    i += 1

def record(dirname):
  warmup_webcam()
  i = 0
  try:
    os.mkdir(dirname)
  except:
    print 'could not make dir'
    exit()

  while disp.isNotDone():
    if disp.mouseLeft:
      break
    img = cam.getImage()
    img.save(disp)
    img.save('%s/%s.jpg' % (dirname, i))
    i += 1

def play(func=None):
  warmup_webcam()
  while disp.isNotDone():
    if disp.mouseLeft:
      break
    img = cam.getImage()
    if func: 
      img = func(img)
    img.save(disp)

def drawlines(img):
  blobs = img.findLines()
  blobs.draw()
  return img

def warmup_webcam():
  for i in range(30):
    img = cam.getImage()

def diffinator(img):
  global prev
  if not prev:
    prev = img
    return img
  else:
    diff = img - prev
    # prev = img
    matrix = diff.getNumpy()
    mean = matrix.mean()
    print mean
    return diff

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--record', metavar='dirname', help="record imgs to dirname")
  parser.add_argument('--play', help="play live without recording", action='store_true')
  parser.add_argument('--diff', help="diff it lolz", action='store_true')
  parser.add_argument('--load', metavar='dirname', help="load and play imgs from dirname")
  args = parser.parse_args()
  print args.__dict__

  if args.diff:
    func = diffinator
  else:
    func = None

  if args.record:
    record(args.record)
  elif args.load:
    load_play(args.load, func)
  else:
    play(func)

  disp.quit()
  time.sleep(.1)

if __name__ == '__main__':
  main()