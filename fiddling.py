#!/usr/bin/python
import SimpleCV
import time, sys, os

cam = SimpleCV.Camera(0)
disp = SimpleCV.Display()
prev = None

def load_play(func):
  i = 0
  dirname = sys.argv[1]

  while disp.isNotDone():
    if disp.mouseLeft:
      break
    img = SimpleCV.Image('%s/%s.jpg' % (dirname, i))
    if func:
      img = func(img)
    img.save(disp)
    i += 1

def record():
  i = 0
  dirname = sys.argv[1]
  try:
    os.mkdir(dirname)
  except:
    print 'could not make dir'
    exit()

  while disp.isNotDone():
    if disp.mouseLeft:
      break
    img.save(disp)
    img.save('%s/%s.jpg' % (dirname, i))
    i += 1

def play(func=None):
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

def diffinator(img):
  global prev
  if not prev:
    prev = img
    return img
  else:
    diff = img - prev
    prev = img
    matrix = diff.getNumpy()
    mean = matrix.mean()
    print mean
    return diff

def main():
  load_play(diffinator)
  disp.quit()
  time.sleep(.1)

if __name__ == '__main__':
  main()