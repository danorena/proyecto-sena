# USAGE
# python client.py --server-ip localhost --server-port 5555


# import the necessary packages
import argparse
import pickle
import sys
import zmq

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ip", "--server-ip", required=True, type=str,
	help="server's ip address")
ap.add_argument("-p", "--server-port", required=True, type=str,
	help="server's port")
args = vars(ap.parse_args())

# create a container for all sockets in this process
context = zmq.Context()

# establish a socket to talk to server
print("[INFO] connecting to the server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://{}:{}".format(args["server_ip"],
	args["server_port"]))

socket.send("read".encode("ascii"))

# receive a reply text message
response = socket.recv_pyobj()
#data_variable = pickle.loads(response)
print("[INFO] received reply '{}'".format(response['header']))


