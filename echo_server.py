# Code taken from "Code for lab 2" section of eclass for CMPUT 404
#!/usr/bin/env python3
import socket
import time
from threading import Thread

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def echo(conn, addr):
    print("Connected by", addr)
    
    #recieve data, wait a bit, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    print("data1:", full_data)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            
            thread = Thread(target=echo, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()
