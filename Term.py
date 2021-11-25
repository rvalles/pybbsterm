import pygame
import pygame.freetype
import pygame.fastevent
import threading
import struct
class Term(object):
    CSI = '\x1b[' #ESC[
    colortable_guess = [
        (0, 0, 0), #black
        (160, 0, 0), #red
        (0, 160, 0), #green
        (160, 160, 0), #yellow
        (0, 0, 160), #blue
        (160, 0, 160), #magenta
        (0, 160, 160), #cyan
        (160, 160, 160), #white
        #bright
        (80, 80, 80), #black
        (255, 0, 0), #red
        (0, 255, 0), #green
        (255, 255, 0), #yellow
        (0, 0, 255), #blue
        (255, 0, 255), #magenta
        (0, 255, 255), #cyan
        (255, 255, 255), #white
        ]
    colortable_vga = [
        (0, 0, 0), #black
        (170, 0, 0), #red
        (0, 170, 0), #green
        (170, 85, 0), #yellow
        (0, 0, 170), #blue
        (170, 0, 170), #magenta
        (0, 170, 170), #cyan
        (170, 170, 170), #white
        #bright
        (85, 85, 85), #black
        (255, 85, 85), #red
        (85, 255, 85), #green
        (255, 255, 85), #yellow
        (85, 85, 255), #blue
        (255, 85, 255), #magenta
        (85, 255, 255), #cyan
        (255, 255, 255), #white
        ]
    colortable_syncterm = [
        (0, 0, 0), #black
        (168, 0, 0), #red
        (0, 168, 0), #green
        (168, 84, 0), #yellow
        (0, 0, 168), #blue
        (168, 0, 168), #magenta
        (0, 168, 168), #cyan
        (168, 168, 168), #white
        #bright
        (84, 84, 84), #black
        (255, 84, 84), #red
        (84, 255, 84), #green
        (255, 255, 84), #yellow
        (84, 84, 255), #blue
        (255, 84, 255), #magenta
        (84, 255, 255), #cyan
        (255, 255, 255), #white
        ]
    def __init__(self, **kwargs):
        pygame.init()
        pygame.freetype.init()
        pygame.fastevent.init()
        self.encoding = "cp437"
        self.cols = 80
        self.rows = 25
        self.cursorx = 1 #column is 1-indexed
        self.cursory = 1 #row is 1-indexed
        self.escape = False
        #self.color = self.colortable_guess
        #self.color = self.colortable_syncterm
        self.color = self.colortable_vga
        self.fgcolordefault = 7
        self.bgcolordefault = 0
        self.fgcolor = self.fgcolordefault
        self.bgcolor = self.bgcolordefault
        #self.fgcolordefault = (224, 224, 128)
        #self.bgcolordefault = (32, 16, 0)
        #self.fgcolordefaultbright = (255, 255, 160)
        #self.bgcolordefaultbright = (48, 24, 0)
        self.blink = False
        self.bright = False
        self.readevent = pygame.event.custom_type()
        self.closeevent = pygame.event.custom_type()
        self.controlsequence = False
        self.controlsequencedata = b''
        self.controlsequencecmdseen = set()
        self.lograwinc = False
        return
    def attach(self, endpoint):
        self.endpoint = endpoint
        endpoint.setuploop(readevent=self.readevent, closeevent=self.closeevent)
        threading.Thread(target=self.endpoint.loop, args=()).start()
        return
    def setkeyboardtranslator(self, translator):
        self.keyboardtranslator = translator
        return
    def setfont(self, fontpath):
        self.font = pygame.freetype.Font(fontpath)
        (x, y, self.fontx, self.fonty) = self.font.get_rect("T")
        self.surfacex = self.cols*self.fontx
        self.surfacey = self.rows*self.fonty
        self.screen = pygame.display.set_mode((self.surfacex, self.surfacey))
        self.surface = pygame.Surface((self.surfacex, self.surfacey))
        return
    def translate(self, byte):
        char = byte.decode(self.encoding)
        return char
    def getfgcolor(self):
        return self.color[self.fgcolor + self.bright*8]
    def getbgcolor(self):
        return self.color[self.bgcolor]
    def getcursorx(self):
        return self.fontx*(self.cursorx-1)
    def getcursory(self):
        return self.fonty*(self.cursory-1)
    def getcursorcolor(self): 
        #return (255, 192, 192)
        return self.getfgcolor()
    def processcontrol(self, cmd, data):
        if cmd == b'A': #Cursor Up
            params = data.split(b';')
            if len(params) != 1:
                print(f"CS A invalid params: {params} data: {data}")
                return
            if not len(params[0]):
                p1 = 1
            else:
                p1 = int(params[0])
            self.cursory = max(self.cursory-p1, 1)
            return
        if cmd == b'B': #Cursor Down
            params = data.split(b';')
            if len(params) != 1:
                print(f"CS B invalid params: {params} data: {data}")
                return
            if not len(params[0]):
                p1 = 1
            else:
                p1 = int(params[0])
            self.cursory = min(self.cursory+p1, self.rows)
            return
        if cmd == b'C': #Cursor Right
            params = data.split(b';')
            if len(params) != 1:
                print(f"CS C invalid params: {params} data: {data}")
                return
            if not len(params[0]):
                p1 = 1
            else:
                p1 = int(params[0])
            self.cursorx = min(self.cursorx+p1, self.cols)
            return
        if cmd == b'D': #Cursor Left
            params = data.split(b';')
            if len(params) != 1:
                print(f"CS D invalid params: {params} data: {data}")
                return
            if not len(params[0]):
                p1 = 1
            else:
                p1 = int(params[0])
            self.cursorx = max(self.cursorx-p1, 1)
            return
        if cmd == b'H' or cmd == b'f': #Cursor Position
            params = data.split(b';')
            if len(params) > 2:
                print(f"CS H invalid params: {params}")
                return
            if not len(params[0]):
                p1 = 1
                p2 = 1
            else:
                p1 = int(params[0])
                if len(params) == 2:
                    p2 = int(params[1])
                else:
                    p2 = 1
            self.cursory = p1
            self.cursorx = p2
            #print(f"CS {chr(ord(cmd))} set row: {p1} col: {p2}")
            return
        if cmd == b'J': #Erase in Page
            params = data.split(b';')
            if len(params) > 1:
                print(f"CS J invalid params: {params}")
                return
            if len(params[0]):
                p1 = int(params[0])
            else:
                p1 = 0
            if p1 == 2: #Erase entire screen
                self.cursorx = 1
                self.cursory = 1
                self.surface.fill(color=self.bgcolor)
                return
            print(f"CS J unimpl p1={p1}")
            return
        if cmd == b'K': #Erase in Line
            params = data.split(b';')
            if len(params) > 1:
                print(f"CS J invalid params: {params}")
                return
            if len(params[0]):
                p1 = int(params[0])
            else:
                p1 = 0
            #print(f"CS K {p1} requested. R:{self.cursory} C:{self.cursorx}.")
            if p1 == 0: #Erase from the current position to the end of the line.
                self.surface.fill(color=self.getbgcolor(), rect=(self.getcursorx(), self.getcursory(), self.fontx*self.cols, self.fonty))
                return
            if p1 == 1: #Erase from the current position to the start of the line.
                self.surface.fill(color=self.getbgcolor(), rect=(0, self.getcursory(), self.getcursorx(), self.fonty))
                return
            if p1 == 2: #Erase entire line
                self.surface.fill(color=self.getbgcolor(), rect=(0, self.getcursory(), self.fontx*self.cols, self.fonty))
                return
            print(f"CS K unimpl p1={p1}")
            return
        if cmd == b'm': #Select Graphic Rendition
            params = data.split(b';')
            if not len(params[0]):
                params[0] = b'0'
            for param in params:
                pX = int(param)
                if pX == 0: #Default attribute, white on black
                    self.blink = False
                    self.bright = False
                    self.fgcolor = self.fgcolordefault
                    self.bgcolor = self.bgcolordefault
                    continue
                if pX == 1: #Bright Intensity
                    self.bright = True
                    continue
                if pX == 2: #Dim Intensity
                    print("CS m Dim Intensity requested, bright instead.")
                    self.bright = True
                    continue
                if pX == 5:
                    print("CS m Blink (slow) requested, not handled.")
                    continue
                if pX == 6:
                    print("CS m Blink (fast) requested, not handled.")
                    continue
                if pX == 7: #Negative Image - Reverses FG and BG	
                    self.fgcolor, self.bgcolor = self.bgcolor, self.fgcolor
                    continue
                if pX == 8: #Concealed characters. Sets the FG to the BG
                    self.bgcolor = self.fgcolor
                    continue
                if pX == 10: #Not ANSI-BBS: Set font to default font.
                    print("CS m Default font requested.")
                    continue
                if pX == 22: #Normal intensity
                    self.bright = False
                    continue
                if pX == 25: #Steady (not blinking)
                    self.blink = False
                    continue
                if pX >= 30 and pX <= 37:
                    self.fgcolor = pX%10
                    continue
                if pX >= 40 and pX <= 47:
                    self.bgcolor = pX%10
                    continue
                else:
                    print(f"CS m unimpl pX={pX}")
            return
        if cmd == b'n': #Device Status Report
            params = data.split(b';')
            if len(params) != 1:
                print(f"CS n invalid params: {params}")
                return
            p1 = int(params[0])
            if p1 == 6: #Request active cursor position
                response = self.CSI + str(self.cursory) + ';' + str(self.cursorx) + 'R'
                self.endpoint.write(response.encode(self.encoding))
                return
            print(f"CS n unimpl p1={p1}")
            return
        if cmd == b's': #Save Current Cursor Position
            if len(data):
                print(f"CS s invalid params: {data}")
                return
            self.cursorsavedx = self.cursorx
            self.cursorsavedy = self.cursory
            return
        if cmd == b'u': #Restore Cursor Position
            if len(data):
                print(f"CS u invalid params: {data}")
                return
            self.cursorx = self.cursorsavedx
            self.cursory = self.cursorsavedy
            return
        print(f"CS unknown CMD: {cmd} parameters: {data}")
        return
    def processoutput(self, data):
        for byte in data:
            if self.controlsequence:
                if byte >= 0x40 and byte <= 0x7e:
                    cmd = byte.to_bytes(1, byteorder='big')
                    self.controlsequence = False
                    self.controlsequencecmdseen.add(cmd)
                    self.processcontrol(cmd, self.controlsequencedata)
                    self.controlsequencedata = b''
                    continue
                else:
                    self.controlsequencedata += byte.to_bytes(1, byteorder='big')
                    continue
            if self.escape:
                self.escape = False
                if byte == ord('['):
                    self.controlsequence = True
                    continue
            if byte == 0x1b:
                self.escape = True
                continue
            if byte == 10:
                #print("NL!")
                if self.cursory == self.rows:
                    #print("scroll text up one line!")
                    self.surface.scroll(0, -self.fonty)
                    self.surface.fill(color=self.getbgcolor(), rect=(0, self.fonty*(self.rows-1), self.fontx*self.cols, self.fonty*self.rows))
                    continue
                self.cursory += 1
                continue
            if byte == 13:
                #print("CR!")
                self.cursorx = 1
                continue
            if byte == 8:
                #print("BS!")
                self.cursorx = max(1,self.cursorx-1)
                continue
            char = self.translate(byte.to_bytes(1, byteorder='big'))
            textsurface, textrect = self.font.render(char, fgcolor=self.getfgcolor(), bgcolor=self.getbgcolor())
            self.surface.blit(textsurface, (self.getcursorx(), self.getcursory()))
            #print(char, textsurface, textrect, self.cursorx*self.fontx, self.cursory*self.fonty)
            self.cursorx = min(self.cursorx+1, self.cols)
        return
    def processkeyboardinput(self, key, mod):
        #special keys with local meaning
        if key==pygame.K_PRINT:
            self.lograwinc = not self.lograwinc
            print(f"Log raw incoming: {self.lograwinc}.")
            return
        if mod & pygame.KMOD_SHIFT:
            if key==pygame.K_ESCAPE:
                self.endpoint.user(0)
                return
            elif key==pygame.K_F1:
                self.endpoint.user(1)
                return
            elif key==pygame.K_F2:
                self.endpoint.user(2)
                return
            elif key==pygame.K_F3:
                self.endpoint.user(3)
                return
            elif key==pygame.K_F4:
                self.endpoint.user(4)
                return
        #rest of events go to keyb translator
        if data := self.keyboardtranslator.translate(key, mod):
            self.endpoint.write(data)
        return
    def loop(self):
        fh = open("capture.log", "wb")
        while True:
            event = pygame.fastevent.wait()
            if event.type==pygame.QUIT:
                print("QUIT event received.")
                #FIXME: close endpoint.
                self.endpoint.close()
                break
            if event.type==self.readevent:
                #print(f"data: {event.data}")
                if self.lograwinc:
                    fh.write(event.data)
                self.processoutput(event.data)
            if event.type==self.closeevent:
                print("Connection closed.")
                print(f"Commands seen: {b''.join(self.controlsequencecmdseen)}")
            if event.type==pygame.KEYDOWN:
                #print(f"keyb input mod: {event.mod}, key: {event.key}")
                self.processkeyboardinput(event.key, event.mod)
            self.screen.blit(self.surface, (0, 0))
            self.screen.fill(color=self.getcursorcolor(), rect=(self.getcursorx(), self.getcursory(), self.fontx, self.fonty))
            pygame.display.flip()
        pygame.quit()
        return
