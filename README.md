Musical Toilet
==============


Video of toilet in action: http://www.youtube.com/watch?v=EG2NHagHWM0


Installation
------------

You need SimpleCV, the soundcloud client library, tweepy, and GStreamer (PyGST). We recommend Ubuntu for this since we spent >6hrs trying to install on both Windows and Mac to no avail. Ubuntu installation took five minutes (ymmv). Note that the soundcloud api currently has an error requiring you to install an old version of the requests library with `pip install -I requests==0.14.2`. 


Usage
-----

`python peecam.py [--play] [--load dirname] [--record dirname] [--diff] [--show]`

`--play` plays live without recording to dir. 

`--record` records images to a directory (easier to work with than a movie file). 

`--load` loads directory of images and plays them. 

`--diff` runs the actual computer-vision type stuff. Run w/o args to play live

`--show` shows something close to what the computer sees, as it were. 


Setting up the Camera
---------------------

The webcam should be perched near the base of the back of the toilet; we put it on the top of the toilet seat when it is up. It's important that the view is centered and that nothing but toilet is visible (ie; avoid having areas of the background showing in the camera). The script relies on there being a relatively thin, dark shadow underneath the rim of the toilet, which is common in most lighting conditions. 


Authors
-------

Kyle Hardgrave (http://kylehardgrave.com/) and Alex Rattray (http://alexrattray.com/). Built at PennApps Spring 2013 (and tuned up a little bit thereafter). 

MIT License. 