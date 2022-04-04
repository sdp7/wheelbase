import socket
import time

c = None

def start_socket():
    global c
    # take the server name and port name
    host = '192.168.105.84'
    port = 35000
    
    # create a socket at server side
    # using TCP / IP protocol
    s = socket.socket(socket.AF_INET,
                    socket.SOCK_STREAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # bind the socket with server
    # and port number
    s.bind(('', port))

    s.listen(2)
    
    # wait till a client accept
    # connection
    c, addr = s.accept()
    
    # display client address
    print("CONNECTION FROM:", str(addr))

def send_message(message):
    c.send(message.encode())
  
def close_socket():
    # disconnect the server
    c.close()

if __name__ == "__main__":
    start_socket()
    print("Socket started!!!")
    send_message("Hiiiii")
    time.sleep(10)
    send_message("Workssssss")
    close_socket()
