import pygame.fastevent
import socket
class EndpointTCP(object):
    def __init__(self, **kwargs):
        if (not "host" in kwargs) or (not "port" in kwargs):
            raise ValueError()
        self.host = kwargs["host"]
        self.port = kwargs["port"]
        self.sockbufsize = 256
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        return
    def setuploop(self, **kwargs):
        if (not "readevent" in kwargs) or (not "closeevent" in kwargs):
            raise ValueError()
        self.readevent = kwargs["readevent"]
        self.closeevent = kwargs["closeevent"]
        return
    def loop(self):
        while True:
            try:
                if incoming := self.sock.recv(self.sockbufsize):
                    pygame.event.post(pygame.event.Event(self.readevent, data=incoming))
                else:
                    break
            except:
                break
        pygame.event.post(pygame.event.Event(self.closeevent))
        self.sock = None
        return
    def write(self, data):
        if self.sock:
            self.sock.sendall(data)
        return
    def close(self):
        if self.sock:
            self.sock.close()
        return
    def user(self, callno):
        if callno==0:
            print("Close requested.")
            if self.sock:
                self.sock.close()
                print("Socket closed.")
                pygame.event.post(pygame.event.Event(self.closeevent))
            return
        print(f"Unimplemented endpoint user function {callno}.")
        return
