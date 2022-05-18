import socket
import pickle

headersize = 10 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))

full_msg = 'b'
new_msg = True

while True:
    msg=s.recv(16)

    if new_msg:
        print(f'new message len: { msg[:headersize] }')
        msglen = int(msg[:headersize])
        new_msg= False
    print(msg)
    full_msg += msg

    if len(full_msg)-headersize==msglen:
        print('full msg recvd')
        print(full_msg[headersize:])
        new_msg= True
        full_msg=b''