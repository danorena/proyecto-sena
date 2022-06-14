# import the necessary packages
import face_recognition
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
from datetime import datetime
from datetime import date
import numpy as np
import imutils
import cv2
import pyttsx3
import os


class PhotoBoothApp:
	def __init__(self, vs, outputPath, conf, socket, recognizer, le):
     
		
		
		# store the video stream object and output path, then initialize
		# the most recently read frame, thread for reading frames, and
		# the thread stop event
		self.vs = vs
		self.outputPath = outputPath
		self.frame = None
		self.thread = None
		self.stopEvent = None

		# initialize the root window and image panel
		self.root = tki.Tk()
		self.panel = None
		self.conf = conf
		self.socket = socket
		self.recognizer = recognizer
		self.le = le

  
		# initialize the text-to-speech engine, set the speech language, and
		# the speech rate
		print("[INFO] Por favor espere mientras inicia la camara...")
		self.ttsEngine = pyttsx3.init()
		self.ttsEngine.setProperty("voice", self.conf["language"])
		self.ttsEngine.setProperty("rate", self.conf["rate"])
		self.ttsEngine.say("Por favor espere mientras el sistema lo detecta")
		self.ttsEngine.runAndWait()
  
		# create a button, that when pressed, will take the current
		# frame and save it to file
		btn = tki.Button(self.root, text="Cerrar",
			command=self.onClose)
		btn.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)

		# start a thread that constantly pools the video sensor for
		# the most recently read frame
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()

		# set a callback to handle when the window is closed
		self.root.wm_title("PyImageSearch PhotoBooth")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoLoop(self):
		# DISCLAIMER:
		# I'm not a GUI developer, nor do I even pretend to be. This
		# try/except statement is a pretty ugly hack to get around
		# a RunTime error that Tkinter throws due to threading
		try:
			
			# initialize previous and current person to None
			self.prevPerson = None
			self.curPerson = None

			# initialize consecutive recognition count to 0
			self.consecCount = 0

			# initialize a dictionary to store the student ID and the time at
			# which their attendance was taken
			self.studentDict = {}
			# keep looping over frames until we are instructed to stop
			while not self.stopEvent.is_set():
				# store the current time and calculate the time difference
				# between the current time and the time for the class
				self.currentTime = datetime.now()
				self.timeDiff = (self.currentTime - datetime.strptime(self.conf["timing"],
					"%H:%M")).seconds

				# grab the frame from the video stream and resize it to
				# have a maximum width of 300 pixels
				self.frame = self.vs.read()
				self.frame = imutils.resize(self.frame, width=400)
				self.frame = cv2.flip(self.frame, 1)
				
				# if the maximum time limit to record attendance has been crossed
				# then skip the attendance taking procedure
				if self.timeDiff > self.conf["max_time_limit"]:
					# check if the student dictionary is not empty
					if len(self.studentDict) != 0:
						# insert the attendance into the database and reset the
						# student dictionary
						self.socket.send_pyobj({"badera":"attendanceTable",
										"mesaje": {str(date.today()): self.studentDict} })
						self.studentDict = {}

					# draw info such as class, class timing, and current time on
					# the frame
					cv2.putText(self.frame, "Ficha: {}".format(self.conf["class"]),
						(10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
					cv2.putText(self.frame, "Hora de entrada: {}".format(self.conf["timing"]),
						(10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
					cv2.putText(self.frame, "Hora actual: {}".format(
						self.currentTime.strftime("%H:%M:%S")), (10, 40),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

					
                	# -------Va lo que falta del attendance.py-------
					# skip the remaining steps since the time to take the
					# attendance has ended
					continue
           		
                # convert the frame from RGB (OpenCV ordering) to dlib 
				# ordering (RGB)
				self.rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                
                
                # detect the (x, y)-coordinates of the bounding boxes
				# corresponding to each face in the input image
				self.boxes = face_recognition.face_locations(self.rgb,model=self.conf["detection_method"])
    
				# loop over the face detections
				for (top, right, bottom, left) in self.boxes:
					# draw the face detections on the frame
					cv2.rectangle(self.frame, (left, top), (right, bottom),
						(0, 255, 0), 2)

				# calculate the time remaining for attendance to be taken
				self.timeRemaining = self.conf["max_time_limit"] - self.timeDiff

				# draw info such as class, class timing, current time, and
				# remaining attendance time on the frame
				cv2.putText(self.frame, "Ficha: {}".format(self.conf["class"]), (10, 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
				cv2.putText(self.frame, "Hora de entrada: {}".format(self.conf["timing"]),
					(10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
				cv2.putText(self.frame, "Hora actual: {}".format(
					self.currentTime.strftime("%H:%M:%S")), (10, 40),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
				cv2.putText(self.frame, "Tiempo transcurrido: {}s".format(self.timeRemaining),
					(10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    

				# check if atleast one face has been detected
				if len(self.boxes) > 0:
					# compute the facial embedding for the face
					self.encodings = face_recognition.face_encodings(self.rgb, self.boxes)

					# perform classification to recognize the face
					self.preds = self.recognizer.predict_proba(self.encodings)[0]
					self.j = np.argmax(self.preds)
					self.curPerson = self.le.classes_[self.j]
     
					# if the person recognized is the same as in the previous
					# frame then increment the consecutive count
					if self.prevPerson == self.curPerson:
						self.consecCount += 1
      

					# otherwise, these are two different people so reset the 
					# consecutive count 
					else:
						self.consecCount = 0
      
					# set current person to previous person for the next
					# iteration
					self.prevPerson = self.curPerson
    
					
     
					# if a particular person is recognized for a given
					# number of consecutive frames, we have reached a 
					# positive recognition and alert/greet the person accordingly
					if self.consecCount >= self.conf["consec_count"]:
						# check if the student's attendance has been already
						# taken, if not, record the student's attendance
						if self.curPerson not in self.studentDict.keys():
							self.studentDict[self.curPerson] = datetime.now().strftime("%H:%M:%S")
     
							# get the student's name from the database and let them
							# know that their attendance has been taken
							self.socket.send_pyobj({"badera":"studentTable",
										"mesaje": self.curPerson})
							self.name = self.socket.recv_pyobj()
							self.ttsEngine.say("{} la asistencia ha sido registrada.".format(
								self.name))
							self.ttsEngine.runAndWait()

						# construct a label saying the student has their attendance
						# taken and draw it on to the frame
						self.label = "{}, la asistencia ha sido registrada {}".format(
							self.name, self.conf["class"])
						cv2.putText(self.frame, self.label, (5, 175),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
     
					# otherwise, we have not reached a positive recognition and
					# ask the student to stand in front of the camera
					else:
						# construct a label asking the student to stand in fron
						# to the camera and draw it on to the frame
						self.label = "Por favor espere mientras el sistema lo detecta"
						cv2.putText(self.frame, self.label, (5, 175),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
     
     
     
				# OpenCV represents images in BGR order; however PIL
				# represents images in RGB order, so we need to swap
				# the channels, then convert to PIL and ImageTk format
				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)


				# if the panel is not None, we need to initialize it
				if self.panel is None:
					self.panel = tki.Label(image=image)
					self.panel.image = image
					self.panel.pack(side="left", padx=10, pady=10)
		
				# otherwise, simply update the panel
				else:
					self.panel.configure(image=image)
					self.panel.image = image


		except RuntimeError :
			print("[INFO] caught a RuntimeError")
   
   
	def onClose(self):
		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()