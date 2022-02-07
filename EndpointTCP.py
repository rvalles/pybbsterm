import pygame.fastevent
import socket
class EndpointTCP(object):
    def __init__(self, **kwargs):
        if (not "host" in kwargs) or (not "port" in kwargs):
            raise ValueError()
        self.host = kwargs["host"]
        self.port = kwargs["port"]
        self.sockbufsize = 256
        return
    def setuploop(self, **kwargs):
        if (not "readevent" in kwargs) or (not "closeevent" in kwargs):
            raise ValueError()
        self.readevent = kwargs["readevent"]
        self.closeevent = kwargs["closeevent"]
        try:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
        except:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
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
        if self.sock:
            pygame.event.post(pygame.event.Event(self.closeevent))
            self.sock = None
        return
    def write(self, data):
        if self.sock:
            self.sock.sendall(data)
        return
    def close(self):
        if self.sock:
            sock = self.sock
            self.sock = None
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            pygame.event.post(pygame.event.Event(self.closeevent))
        return
    def user(self, callno):
        print(f"Unimplemented endpoint user function {callno}.")
        return
