import threading
import time
from Conf import Configuration
import socket
import sys
import traceback

class NetworkDemon(object):
    LAST_PING_TIME = None
    WAIT_TIME = 20*60
    SLEEP_TIME = 30*60

    def __init__(self):
        ## do broadcast
        thread = threading.Thread(target=self.run,args=())
        thread.daemon = True
        thread.start()
    def run(self):
        
        while True:
            cur_time = int(time.time())
            if  self.LAST_PING_TIME ==None or cur_time-self.LAST_PING_TIME > self.WAIT_TIME:
                self.boradcast()
                self.LAST_PING_TIME = int(time.time())
            time.sleep(self.SLEEP_TIME)
            #print(self.LAST_PING_TIME)
            #print(cur_time)



    def boradcast(self):

        """

            import socket

UDP_IP = "10.204.255.255"
UDP_PORT = 3001
MESSAGE = "Hello, World!1"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        """

        msg = b'' if Configuration.get_client_id()==None else Configuration.get_client_id().encode('ascii')
        dest = ("192.168.43.255",3001)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(msg,dest)
        print("Broadcasted")
        

    @staticmethod

    def startup():
        daemon = NetworkDemon()
        #daemon.run()
        



        




     

    