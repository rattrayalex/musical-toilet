#!/usr/bin/python
import SimpleCV
import time, sys

cam = SimpleCV.Camera(1)
disp = SimpleCV.Display()
i = 0
dirname = sys.argv[1]

while disp.isNotDone():
  if disp.mouseLeft:
    break
  # img = cam.getImage()
  img = SimpleCV.Image('%s/%s.jpg' % (dirname, i))
  blobs = img.findLines()
  blobs.draw()
  img.save(disp)
  i += 1

disp.quit()

time.sleep(.1)