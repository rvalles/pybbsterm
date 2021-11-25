import pygame.fastevent
import serial
class EndpointSerial(object):
    def __init__(self, **kwargs):
        if (not "device" in kwargs) or (not "rate" in kwargs):
            raise ValueError()
        self.serialdev = kwargs['device']
        self.serialrate = kwargs['rate']
        self.serial = serial.Serial(self.serialdev, self.serialrate, exclusive=True)
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
                if incoming := self.serial.read(1):
                    pygame.event.post(pygame.event.Event(self.readevent, data=incoming))
                else:
                    break
            except:
                break
        if self.serial:
            pygame.event.post(pygame.event.Event(self.closeevent))
            self.serial = None
        return
    def write(self, data):
        if self.serial:
            self.serial.write(data)
        return
    def close(self):
        if self.serial:
            serial = self.serial
            self.serial = None
            serial.cancel_read()
            serial.cancel_write()
            serial.close()
            pygame.event.post(pygame.event.Event(self.closeevent))
        return
    def user(self, callno):
        print(f"Unimplemented endpoint user function {callno}.")
        return
