#!/usr/bin/env python3
from Term import Term
from EndpointTCP import EndpointTCP
from EndpointReplay import EndpointReplay
from KeyboardTranslatorBasic import KeyboardTranslatorBasic
import sys
import argparse
def main():
    parser = argparse.ArgumentParser(description="ANSI-BBS terminal.")
    parser.add_argument('-t', '--tcp', dest='tcp', action='store', metavar='host:port', help="make a TCP connection")
    parser.add_argument('-r', '--replay', dest='replay', action='store', metavar='logfile', help="replay a capture log")
    args = parser.parse_args()
    #print(vars(args))
    endpoints = {'tcp', 'replay'}.intersection({k: v for k, v in vars(parser.parse_args()).items() if v is not None})
    if len(endpoints) != 1:
        parser.print_usage()
        sys.exit(2)
    if args.tcp:
        tcpparam = args.tcp.split(':')
        if len(tcpparam) > 2:
            print("Malformed hostname")
            sys.exit(2)
        host = tcpparam[0]
        if len(tcpparam) > 1:
            port = int(tcpparam[1])
        else:
            port = 23
        endpoint = EndpointTCP(host=host, port=port)
    if args.replay:
        endpoint = EndpointReplay(path=args.replay)
    fontpath = "/usr/share/fonts/misc/Bm437_Amstrad_PC-2y.otb"
    #fontpath = "/usr/share/fonts/misc/Bm437_IBM_VGA_9x16.otb"
    #fontpath = "/usr/share/fonts/misc/Bm437_IBM_XGA-AI_12x23.otb"
    term = Term()
    translator = KeyboardTranslatorBasic()
    term.setkeyboardtranslator(translator)
    term.setfont(fontpath)
    term.attach(endpoint)
    term.loop()
    return
if __name__ == "__main__":
    main()
