#!/usr/bin/env python3
from Term import Term
from EndpointTCP import EndpointTCP
from EndpointReplay import EndpointReplay
from KeyboardTranslatorBasic import KeyboardTranslatorBasic
import sys
def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)
    host, port = sys.argv[1], int(sys.argv[2])
    logpath = "capture.log"
    fontpath = "/usr/share/fonts/misc/Bm437_Amstrad_PC-2y.otb"
    #fontpath = "/usr/share/fonts/misc/Bm437_IBM_VGA_9x16.otb"
    #fontpath = "/usr/share/fonts/misc/Bm437_IBM_XGA-AI_12x23.otb"
    term = Term()
    translator = KeyboardTranslatorBasic()
    term.setkeyboardtranslator(translator)
    term.setfont(fontpath)
    endpoint = EndpointTCP(host=host, port=port)
    #endpoint = EndpointReplay(path=logpath)
    term.attach(endpoint)
    term.loop()
    return
if __name__ == "__main__":
    main()
