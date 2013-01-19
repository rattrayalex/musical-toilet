#!/usr/bin/python
import SimpleCV
import time, sys, os

cam = SimpleCV.Camera(1)
disp = SimpleCV.Display()
i = 0

dirname = sys.argv[1]
try:
  os.mkdir(dirname)
except:
  exit()

while disp.isNotDone():
  if disp.mouseLeft:
    break
  img = cam.getImage()
  # blobs = img.findLines()
  # blobs.draw()
  img.save(disp)
  img.save('%s/%s.jpg' % (dirname, i))
  i += 1

disp.quit()

time.sleep(.1)