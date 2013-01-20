Musical Toilet
==============


By Kyle Hardgrave and Alex Rattray at PennApps Spring 2013
----------------------------------------------------------


Installation
------------

You need SimpleCV, the soundcloud client library, and GStreamer (PyGST). We recommend Ubuntu for this since we spent >6hrs trying to install on both Windows and Mac to no avail. Ubuntu installation took five minutes. Note that the soundcloud api currently has an error requiring you to install an old version of the requests library with `pip install -I requests==0.14.2`. 


Usage
-----

`python peecam.py [--load dirname] [--record dirname] [--diff] [--show]`

`--record` records images to a directory (easier to work with than a movie file). 
`--load` loads directory of images and plays them. 
`--diff` runs the actual computer-vision type stuff. Run w/o args to play live
`--show` shows something close to what the computer sees, as it were. 

