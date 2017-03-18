#Socket client example in python
 
import socket   #for sockets
import sys  #for exit



if __name__=="__main__":
    try:
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()
    print 'Socket Created'
     
    host = 'localhost';
    port = 31114;
     
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print 'Hostname Resolution Error'
        sys.exit()
     
    mysocket.connect((remote_ip , port))
    print 'Socket Connected to ' + host + ' on ip ' + remote_ip
     
    #Send some data to remote server
    message = "video_name\r\n\r\n"
    try :
        #Set the whole string
        mysocket.sendall(message)
    except socket.error:
        print 'Send failed'
        sys.exit()
     
    #Now receive data
    response = mysocket.recv(4096)
    print response
