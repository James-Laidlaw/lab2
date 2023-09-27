# Code based on client.py and echo_server.py from "Code for lab 2" section of eclass for CMPUT 404
#!/usr/bin/env python3

#things pertaining to client-side connection are prefixed with c_
#things pertaining to server-side connection are prefixed with s_
import socket, sys, time
from threading import Thread

forward_target = 'www.google.com'

#create a tcp socket
def c_create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def listen(conn: socket.socket, buffer_size: int):
    print("listen started")
    full_payload = b""
    while True:
        data = conn.recv(buffer_size)
        if not data:
            break
        full_payload += data
    print("recieved data")
    return full_payload


def listen_forward_reply(conn: socket.socket):
    print("listen forward reply started") 
    c_port = 80
    buffer_size = 4096
    c_host = forward_target


    #recieve data, send it to client target, then send response back to client


    forward_full_payload = listen(conn, buffer_size)

    #connect to google
    try:
        #make the socket, get the ip, and connect
        c_s = c_create_tcp_socket()

        remote_ip = get_remote_ip(c_host)

        c_s.connect((remote_ip , c_port))
        print (f'Socket Connected to {c_host} on ip {remote_ip}')

        #forward the data to google and shutdown
        c_s.sendall(forward_full_payload)
        c_s.shutdown(socket.SHUT_WR)
        print("forwarded data")

        #continue accepting response data until no more left
        response_full_payload = listen(c_s, buffer_size)

        #return response data to client
        conn.sendall(response_full_payload)
        print("sent response data")
    
    except Exception as e:
        print(e)
    finally:
        #close the connection to google, then close the connection to the client
        c_s.close()
        conn.close()
        print("closed connection to google and client")

def main():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_s:
            #set up proxy server
            #define address & buffer size
            s_host = ""
            s_port = 8001
            
            s_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #bind socket to address
            s_s.bind((s_host, s_port))
            #set to listening mode
            s_s.listen(2)

            #continuously listen for connections
            while True:
                conn, addr = s_s.accept()
                print("Connected by", addr)

                thread = Thread(target=listen_forward_reply, args=(conn,))
                thread.start()
                

if __name__ == "__main__":
    main()

