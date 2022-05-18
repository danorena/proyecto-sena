# USAGE
# python server.py --server-port 5555 --conf config/config.json

# import necessary packages
from pyimagesearch.utils import Conf
from tinydb import TinyDB
from tinydb import where
import argparse
import pickle
import sys
import zmq
import json

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--server-port", required=True, type=str,
	help="server's port")
ap.add_argument("-c", "--conf", required=True, 
	help="Path to the input configuration file")
args = vars(ap.parse_args())

# load the configuration file
conf = Conf(args["conf"])

# initialize the database, student table, and attendance table
# objects
db = TinyDB(conf["db_path"])
studentTable = db.table("student")
attendanceTable = db.table("attendance")

# create a container for all sockets in this process
context = zmq.Context()

# establish a socket for incoming connections
print("[INFO] creating socket…")
socket = context.socket(zmq.REP)
socket.bind("tcp://*:{}".format(args["server_port"]))

while (True):
	# receive a message, decode it, and conver to lowercase
	try:
		response = socket.recv_pyobj()
	except:
		print("[INFO] terminating the server")
		break

	# check if the correct message, *raspberry*, is received and then
	# send return message message accordingly
	if response["badera"] in "attendanceTable":
		print("[INFO] correct message, so sending 'correct'")
		attendanceTable.insert(response["mesaje"])
		#socket.send_pyobj(msg.data)
	elif response["badera"] in "studentTable":
		name = studentTable.search(where(
						response["mesaje"]))[0][response["mesaje"]][0]
		socket.send_pyobj(name)

	




