# import the necessary packages
from time import gmtime, strftime
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from dht22temp import AdafruitDHT22
import sys
import datetime
import MySQLdb 
from PIL import Image

db = MySQLdb.connect("localhost","root","firemonitor","firemonitor" )

cursor = db.cursor()

temp_humidity = AdafruitDHT22()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 50
camera.hflip = True

rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)

time_started = time.time()

temp = 0
hum = 0
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
        image = frame.array

        blur = cv2.blur(image, (3,3))

	frame_w,frame_h = image.shape[:2]

        #hsv to complicate things, or stick with BGR
        #hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
        #thresh = cv2.inRange(hsv,np.array((0, 200, 200)), np.array((20, 255, 255)))

        #lower = np.array([76,31,4],dtype="uint8")
        #upper = np.array([225,88,50], dtype="uint8")
        #upper = np.array([210,90,70], dtype="uint8")
	imgray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        #thresh = cv2.inRange(blur, lower, upper)
        #thresh2 = thresh.copy()

        # find contours in the threshold image
        image, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	currtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	
	elapsed = time_started - time.time()
	elapsedint = int(abs(elapsed))

        
	if elapsedint%15 == 0:
		#temp_humidity.retry()
		temp = temp_humidity.get_temp()
		hum = temp_humidity.get_humidity()

	if elapsedint >= 43600:
	#43600:
		cv2.imwrite(currtime + ".jpg",image)
		time_started = time.time()

	cv2.putText(blur,"Temp: {0:0.1f} C".format(temp),(frame_w-int(frame_w * 0.9),400),cv2.FONT_HERSHEY_COMPLEX,0.5,(224,255,255))
	cv2.putText(blur,"Hum: {0:0.01f}  %".format(hum),(frame_w-50,400),cv2.FONT_HERSHEY_COMPLEX,0.5,(224,255,255))	
		
	cv2.putText(blur,str(elapsedint),(frame_w-50,100),cv2.FONT_HERSHEY_COMPLEX,0.5,(224,255,255))

	cv2.putText(blur,"FIRE MONITORING", (frame_w-50,25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (224,255,255))
	cv2.putText(blur,currtime, (frame_w-50,420), cv2.FONT_HERSHEY_COMPLEX, 0.5, (224,255,255))

        # finding contour with maximum area and store it as best_cnt
        max_area = 0
        best_cnt = 1
        for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                        max_area = area
                        best_cnt = cnt

	areas = [cv2.contourArea(c) for c in contours]
	
	if  areas:
		max_index = np.argmax(areas)
		cnt=contours[max_index]

		x,y,w,h = cv2.boundingRect(cnt)

		if w >= 30 and h >= 30:
			cv2.rectangle(blur,(x,y),(x+w,y+h),(0,0,255),2)
			cv2.putText(blur,"POTENTIAL FIRE DETECTED", (x + 10,y + 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (224,255,255))
			cv2.rectangle(blur,(0,0),(blur.shape[0] * 2,blur.shape[1]),(0,0,255),10)
			crop_img = blur[y: y + h, x: x + w]
			cv2.imwrite(currtime + ".jpg",crop_img)
		
			
			#find circles
			#circles = cv2.HoughCircles(blurgauss,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
		
			print("W: ")
			print(w)
			print("\nH: ")
			print(h)
			im_pil = Image.fromarray(frame.array)
			print(im_pil.convert('RGB').getcolors(5))
			#if circles is not None:
				#for c in circles[0,:]:
				    #if c is not None:
					# draw the outer circle
					#cv2.circle(blur,(c[0],c[1]),c[2],(0,255,0),2)
					# draw the center of the circle
					#cv2.circle(blur,(c[0],c[1]),2,(0,0,255),3)

	
        # finding centroids of best_cnt and draw a circle there
        #M = cv2.moments(best_cnt)
        #cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        #if best_cnt>1:
        #cv2.circle(blur,(cx,cy),10,(0,0,255),-1)
        # show the frame
        cv2.imshow("Fire Monitoring System", blur)
	#cv2.imshow("bounded",image)
        #cv2.imshow('thresh',thresh2)
        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
        	break
