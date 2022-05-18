# USAGE
# python attendance.py --conf config/config.json --server-ip localhost --server-port 5555 

# import the necessary packages
import socket, pickle
from pyimagesearch.utils import Conf
from imutils.video import VideoStream
from datetime import datetime
from datetime import date
import face_recognition
import numpy as np
import argparse
import imutils
import pyttsx3
import pickle
import time
import cv2
import zmq
import os
import sys

sys.path.append('../')
from controller.path import path

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, 
	help="Path to the input configuration file")
ap.add_argument("-ip", "--server-ip", required=True, type=str,
	help="server's ip address")
ap.add_argument("-p", "--server-port", required=True, type=str,
	help="server's port")
args = vars(ap.parse_args())

# load the configuration file
# ruta = path()
# ruta += ('model\\datasets\\attendance_system_dataset\\111\\config')
# os.chdir(ruta)
conf = Conf(args["conf"])

# create a container for all sockets in this process
context = zmq.Context()

# establish a socket to talk to server
print("[INFO] connecting to the server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://{}:{}".format(args["server_ip"],
	args["server_port"]))

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(conf["recognizer_path"], "rb").read())
le = pickle.loads(open(conf["le_path"], "rb").read())

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# initialize previous and current person to None
prevPerson = None
curPerson = None

# initialize consecutive recognition count to 0
consecCount = 0

# initialize the text-to-speech engine, set the speech language, and
# the speech rate
print("[INFO] taking attendance...")
ttsEngine = pyttsx3.init()
ttsEngine.setProperty("voice", conf["language"])
ttsEngine.setProperty("rate", conf["rate"])

# initialize a dictionary to store the student ID and the time at
# which their attendance was taken
studentDict = {}

# loop over the frames from the video stream
while True:
	# store the current time and calculate the time difference
	# between the current time and the time for the class
	currentTime = datetime.now()
	timeDiff = (currentTime - datetime.strptime(conf["timing"],
		"%H:%M")).seconds

	# grab the next frame from the stream, resize it and flip it
	# horizontally
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	frame = cv2.flip(frame, 1)

	# if the maximum time limit to record attendance has been crossed
	# then skip the attendance taking procedure
	if timeDiff > conf["max_time_limit"]:
		# check if the student dictionary is not empty
		if len(studentDict) != 0:
			# insert the attendance into the database and reset the
			# student dictionary
			socket.send_pyobj({"badera":"attendanceTable",
							   "mesaje": {str(date.today()): studentDict} })
			studentDict = {}

		# draw info such as class, class timing, and current time on
		# the frame
		cv2.putText(frame, "Ficha: {}".format(conf["class"]),
			(10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
		cv2.putText(frame, "Hora de entrada: {}".format(conf["timing"]),
			(10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
		cv2.putText(frame, "Hora actual: {}".format(
			currentTime.strftime("%H:%M:%S")), (10, 40),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

		# show the frame
		cv2.imshow("Attendance System", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

		# skip the remaining steps since the time to take the
		# attendance has ended
		continue

	# convert the frame from RGB (OpenCV ordering) to dlib 
	# ordering (RGB)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb,
		model=conf["detection_method"])

	# loop over the face detections
	for (top, right, bottom, left) in boxes:
		# draw the face detections on the frame
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)

	# calculate the time remaining for attendance to be taken
	timeRemaining = conf["max_time_limit"] - timeDiff

	# draw info such as class, class timing, current time, and
	# remaining attendance time on the frame
	cv2.putText(frame, "Ficha: {}".format(conf["class"]), (10, 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
	cv2.putText(frame, "Hora de entrada: {}".format(conf["timing"]),
		(10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
	cv2.putText(frame, "Hora actual: {}".format(
		currentTime.strftime("%H:%M:%S")), (10, 40),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
	cv2.putText(frame, "Tiempo transcurrido: {}s".format(timeRemaining),
		(10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

	# check if atleast one face has been detected	
	if len(boxes) > 0:
		# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)
				
		# perform classification to recognize the face
		preds = recognizer.predict_proba(encodings)[0]
		j = np.argmax(preds)
		curPerson = le.classes_[j]

		# if the person recognized is the same as in the previous
		# frame then increment the consecutive count
		if prevPerson == curPerson:
			consecCount += 1

		# otherwise, these are two different people so reset the 
		# consecutive count 
		else:
			consecCount = 0

		# set current person to previous person for the next
		# iteration
		prevPerson = curPerson
				
		# if a particular person is recognized for a given
		# number of consecutive frames, we have reached a 
		# positive recognition and alert/greet the person accordingly
		if consecCount >= conf["consec_count"]:
			# check if the student's attendance has been already
			# taken, if not, record the student's attendance
			if curPerson not in studentDict.keys():
				studentDict[curPerson] = datetime.now().strftime("%H:%M:%S")
			
				# get the student's name from the database and let them
				# know that their attendance has been taken
				socket.send_pyobj({"badera":"studentTable",
							   "mesaje": curPerson})
				name = socket.recv_pyobj()
				ttsEngine.say("{} la asistencia ha sido registrada.".format(
					name))
				ttsEngine.runAndWait()

			# construct a label saying the student has their attendance
			# taken and draw it on to the frame
			label = "{}, la asistencia ha sido registrada {}".format(
				name, conf["class"])
			cv2.putText(frame, label, (5, 175),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

		# otherwise, we have not reached a positive recognition and
		# ask the student to stand in front of the camera
		else:
			# construct a label asking the student to stand in fron
			# to the camera and draw it on to the frame
			label = "Por favor espere mientras el sistema lo detecta"
			cv2.putText(frame, label, (5, 175),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

	# show the frame
	cv2.imshow("Attendance System", frame)
	key = cv2.waitKey(1) & 0xFF

	# check if the `q` key was pressed
	if key == ord("q"):
		# check if the student dictionary is not empty, and if so,
		# insert the attendance into the database
		if len(studentDict) != 0:
			socket.send_pyobj({"badera":"attendanceTable",
					"mesaje": {str(date.today()): studentDict} })
		break

# clean up
print("[INFO] cleaning up...")
vs.stop()

