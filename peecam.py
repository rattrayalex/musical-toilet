import SimpleCV
import time, sys, os, argparse

class PeeCam:

  def __init__(self, cam=0):
    self.cam = SimpleCV.Camera(cam)
    self.disp = SimpleCV.Display()

  def run(self, func=None, action=None, dirname=None):

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

      if not orig:
        print 'not orig'
        dark_blob, orig, dark_matrix = get_dark_slice(img)
        print 'got the dark stuff'

      if func:
        img = func(img, orig, dark_blob, dark_matrix)

      img.save(self.disp)

      if action == 'record':
        img.save('%s/%s.jpg' % (dirname, i))

      i += 1

    return

  def warmup_webcam(self):
    for i in range(5):
      img = self.cam.getImage()

def diffinator(img, orig, dark_blob, dark_matrix):
  img = img.crop(dark_blob)
  diff = SimpleCV.Image(img.getNumpy() * dark_matrix) - orig
  ydiff = diff.colorDistance(SimpleCV.Color.YELLOW)
  matrix = ydiff.getNumpy()
  # means = matrix_avgs(matrix)
  # print max(zip(means, range(5)))
  xval = localize(matrix)
  print xval
  return ydiff

def matrix_avgs(m, n=5):
  slice_avgs = []
  w = len(m) / n
  h = len(m[0])
  for i in range(n):
    a, b = i*w, (i+1)*w
    mean = m[a:b, 0:(h/2)].mean()
    slice_avgs.append(mean)
  return slice_avgs

def localize(m):
  # col row rgb
  mlen = len(m)
  xval, blackest = 0, 255 #cols =
  for i in range(mlen):
    fro, to = max(i-5,0), min(i+5,(mlen - 1))
    col_sum = sum(sum(list(m[fro:to,j,0].flatten())) for j in range(len(m[i])))
    # col_sum = 0
    # for j in range(len(m[i])):
    #   # print j
    #   col_sum += sum(list(m[fro:to,j,0].flatten()))
    # # print col_sum
    if col_sum < blackest:
      blackest = col_sum
      xval = i
  # cols = [(sum(m[max(i-5,0):min(i+5,mlen),:,0]), i) for i in range(mlen)]
  # xval = min(cols)[1]
  percent = float(xval) / mlen
  return percent

def get_dark_slice(img):
  p = img.getPalette()
  print 'got palette'
  darkest = sorted(p, key = lambda r: sum(r))
  print 'sorted out darkest'
  blobs = img.findBlobsFromPalette(darkest[:2], minsize=300)
  print 'found blobs'
  blobs.sort(key=lambda b: -b.mArea)
  print 'sorted blobs'
  dark_blob = blobs[0]
  dark_slice = dark_blob.blobImage()
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
  parser.add_argument('--load', metavar='dirname', help="load and play imgs from dirname")
  args = parser.parse_args()

  if args.diff:
    func = diffinator
  else:
    func = None

  pc = PeeCam()

  if args.record:
    pc.run(action='record', dirname=args.record)
  elif args.load:
    pc.run(func=func, action='load', dirname=args.load)
  else:
    pc.run(func=func)

if __name__ == '__main__':
  main()