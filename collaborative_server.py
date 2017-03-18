import socket
import sys
import thread
import time
import json

HOST = ''   # all interfaces
PORT = 31114 # fixed port,can be changed, to be moved to a config file
 

def client_thread(conn):
    #time.sleep(10);
    video_name=conn.recv(4096).rstrip("\r\n\r\n")
    print video_name
    data=json.loads(open("historic_results.json").read())
    conn.sendall(str(data[video_name]))
    conn.close()
    thread.exit()

def setup_listening_socket():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "Socket created"
	 
	#Bind socket to local host and port
	try:
	    s.bind((HOST, PORT))
	except socket.error as msg:
	    print "Bind failed with error : " + str(msg[0]) + ", " + msg[1]
	    sys.exit()
	     
	print "Socket bind successful"
	 
	s.listen(10) #10 is maximum number of backlogged connections
	print "Socket listen successful"
	 
	#wait for client connections indefinitely
	while 1:
	    print "Waiting to accept"
	    conn, addr = s.accept()
	    print "Incoming from " + addr[0] + ":" + str(addr[1])
	    thread.start_new_thread(client_thread,(conn,))

	s.close()
