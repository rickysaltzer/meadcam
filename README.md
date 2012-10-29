Meadcam
=======

Description (Why?)
------------------
I'm cheap and lazy, and I didn't feel like buying a Rasberry Pi and all the other sensors needed
to do this properly. Yes, it would be better to take gravity readings and to keep track of the temperature. I mainly
just wanted to keep track of how often a bubble is released in the fermentation lock. 

Basically, you hook a webcam up, point it directly at the fermentation lock (provided you have good lighting), the program
will basically find differences between each frame, when a bubble is emitted, the program will pick it up and record the details, 
including the image into HBase. The time between bubbles will steadily increase while fermenting. 


Basic "How it works"
-------------------

1. First image from webcam is used as a sample
2. Infinite Loop (30+ frames per second)
3. Is there a major difference between this image and the last image?

  Yes:
    There was a bubble, record it into the database and wait a few seconds before comparing more images. 

  No:
    Return to beginning of loop


Authors
-------
Ricky Saltzer


Requirements
------------
* HBase w/ Thrift interface
* Python
* Happybase (HBase client)


