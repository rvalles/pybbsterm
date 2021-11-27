import pygame
class KeyboardTranslatorBasic(object):
    CSI = '\x1b[' #ESC[
    def __init__(self, **kwargs):
        return
    def translate(self, key, mod):
        if mod & pygame.KMOD_SHIFT: #FIXME: Hardcoded UK layout mess
            if key==ord('`'):
                return b'\xaa' #FIXME: hardcoded cp437
            if key==ord('1'):
                key = ord('!')
            if key==ord('2'):
                key = ord('"')
            if key==ord('3'):
                return b'\x9c' #FIXME: hardcoded cp437
            if key==ord('4'):
                key = ord('$')
            if key==ord('5'):
                key = ord('%')
            if key==ord('6'):
                key = ord('^')
            if key==ord('7'):
                key = ord('&')
            if key==ord('8'):
                key = ord('*')
            if key==ord('9'):
                key = ord('(')
            if key==ord('0'):
                key = ord(')')
            if key==ord('-'):
                key = ord('_')
            if key==ord('='):
                key = ord('+')
            if key==ord('['):
                key = ord('{')
            if key==ord(']'):
                key = ord('}')
            if key==ord(';'):
                key = ord(':')
            if key==ord("'"):
                key = ord('@')
            if key==ord('#'):
                key = ord('~')
            if key==ord(','):
                key = ord('<')
            if key==ord('.'):
                key = ord('>')
            if key==ord('/'):
                key = ord('?')
            if key==ord('\\'):
                key = ord('|')
            elif key >= ord('a') and key <= ord('z'):
                key = ord(chr(key).upper())
            if key >= 0x20 and key <= 0x7e:
                return key.to_bytes(1, byteorder='big')
        elif key >= 0x20 and key <= 0x7b:
            return key.to_bytes(1, byteorder='big')
        elif key==pygame.K_RETURN or key==pygame.K_KP_ENTER:
            return b'\r'
        elif key==pygame.K_TAB:
            return b'\t'
        elif key==pygame.K_BACKSPACE:
            return b'\b'
        elif key==pygame.K_ESCAPE:
            return b'\x1b'
        elif key==pygame.K_LEFT:
            return self.CSI.encode("cp437") + b'D'
        elif key==pygame.K_RIGHT:
            return self.CSI.encode("cp437") + b'C'
        elif key==pygame.K_UP:
            return self.CSI.encode("cp437") + b'A'
        elif key==pygame.K_DOWN:
            return self.CSI.encode("cp437") + b'B'
        elif key==pygame.K_INSERT:
            return self.CSI.encode("cp437") + b'@'
        elif key==pygame.K_DELETE:
            return b'\x7f'
        elif key==pygame.K_HOME:
            return self.CSI.encode("cp437") + b'H'
        elif key==pygame.K_END:
            return self.CSI.encode("cp437") + b'K'
        elif key==pygame.K_PAGEUP:
            return self.CSI.encode("cp437") + b'V'
        elif key==pygame.K_PAGEDOWN:
            return self.CSI.encode("cp437") + b'U'
        elif key==pygame.K_F1:
            return b'\x1bOP'
        elif key==pygame.K_F2:
            return b'\x1bOQ'
        elif key==pygame.K_F3:
            return b'\x1bOR'
        elif key==pygame.K_F4:
            return b'\x1bOS'
        elif key==pygame.K_F5:
            return b'\x1bOt'
        elif key==pygame.K_F6:
            return self.CSI.encode("cp437") + b'17~'
        elif key==pygame.K_F7:
            return self.CSI.encode("cp437") + b'18~'
        elif key==pygame.K_F8:
            return self.CSI.encode("cp437") + b'19~'
        elif key==pygame.K_F9:
            return self.CSI.encode("cp437") + b'20~'
        elif key==pygame.K_F10:
            return self.CSI.encode("cp437") + b'21~'
        elif key==pygame.K_F11:
            return self.CSI.encode("cp437") + b'23~'
        elif key==pygame.K_F12:
            return self.CSI.encode("cp437") + b'24~'
        elif key==pygame.K_KP_DIVIDE:
            return b'/'
        elif key==pygame.K_KP_MULTIPLY:
            return b'*'
        elif key==pygame.K_KP_MINUS:
            return b'-'
        elif key==pygame.K_KP_PLUS:
            return b'+'
        elif key==pygame.K_KP_PERIOD:
            return b'.'
        elif key==pygame.K_KP0:
            return b'0'
        elif key==pygame.K_KP1:
            return b'1'
        elif key==pygame.K_KP2:
            return b'2'
        elif key==pygame.K_KP3:
            return b'3'
        elif key==pygame.K_KP4:
            return b'4'
        elif key==pygame.K_KP5:
            return b'5'
        elif key==pygame.K_KP6:
            return b'6'
        elif key==pygame.K_KP7:
            return b'7'
        elif key==pygame.K_KP8:
            return b'8'
        elif key==pygame.K_KP9:
            return b'9'
        else:
            print(f"Not sure how to process keycode: {key}")
        return
