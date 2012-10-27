import cv
import time
import math, operator
from PIL import Image
import ipdb
import datetime
import ImageChops
import happybase

#cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("w1", 640)
camera_index = 1
capture = cv.CaptureFromCAM(camera_index)
first_frame = True
frame_decount = 30
last_bubble_time= time.time()


connection = happybase.Connection('192.168.2.105')
table = connection.table('meadcam')

def repeat():
	global capture
	global camera_index
	global first_frame
	global last_frame
	global frame_decount
	global last_bubble_time

	frame = cv.QueryFrame(capture)
	cv.ShowImage("w1", frame)
	c = cv.WaitKey(10)

	image = Image.fromstring("RGB", [frame.width, frame.height], frame.tostring())
	if not first_frame:
		diff = ImageChops.difference(image, last_frame)
		h = diff.histogram()
		sq = (value*(idx**2) for idx, value in enumerate(h))
		sum_of_squares = sum(sq)
		rms = math.sqrt(sum_of_squares/float(image.size[0] * last_frame.size[1]))
		if rms > 579.00 and frame_decount == 0:
			now = time.time()
			delta = (now - last_bubble_time)
			row_key = '-'.join(['row',str(now)])
			table.put(row_key, {'info:delta': str(delta), 'info:date': str(datetime.datetime.now()).split('.')[0], 'info:rms': str(rms), 'info:height': str(frame.height), 'info:width': str(frame.width)})
			print("Gas Release Detected: (Delta: %f)" % (delta))
			print("Record Saved -> %s" % (row_key))
			frame_decount = 40
			last_bubble_time = now
		elif frame_decount > 0:
			frame_decount = frame_decount - 1

	last_frame = image
	first_frame = False

while True:
    repeat()
