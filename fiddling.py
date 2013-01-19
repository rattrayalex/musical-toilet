#!/usr/bin/python
import SimpleCV
import time

cam = SimpleCV.Camera(1)
disp = SimpleCV.Display()

while disp.isNotDone():
  if disp.mouseLeft:
    break
  img = cam.getImage()
  blobs = img.findLines()
  blobs.draw()
  img.save(disp)

disp.quit()

time.sleep(.1)