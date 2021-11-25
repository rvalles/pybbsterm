import pygame.fastevent
import socket
class EndpointReplay(object):
    def __init__(self, **kwargs):
        if (not "path" in kwargs):
            raise ValueError()
        self.path = kwargs["path"]
        return
    def setuploop(self, **kwargs):
        if (not "readevent" in kwargs) or (not "closeevent" in kwargs):
            raise ValueError()
        self.readevent = kwargs["readevent"]
        self.closeevent = kwargs["closeevent"]
        self.fh = open(self.path, "rb")
        return
    def loop(self):
        self.fh = open(self.path, "rb")
        print("Replay log: Shift-F1 to F4 to advance 1, 4, 16, 64 characters respectively.")
        return
    def write(self, data):
        return
    def close(self):
        self.fh.close()
        return
    def user(self, callno):
        if callno==0:
            pygame.event.post(pygame.event.Event(self.closeevent))
            return
        elif callno==1:
            self.advance(1)
            return
        elif callno==2:
            self.advance(4)
            return
        elif callno==3:
            self.advance(16)
            return
        elif callno==4:
            self.advance(64)
            return
        print(f"Unimplemented endpoint user function {callno}.")
        return
    def advance(self, amount):
        data = self.fh.read(amount)
        print([hex(char) for char in data])
        if len(data):
            pygame.event.post(pygame.event.Event(self.readevent, data=data))
        if len(data) != amount:
            pygame.event.post(pygame.event.Event(self.closeevent))
        return
