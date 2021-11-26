#!/usr/bin/env python3
import sys
import argparse
def main():
    parser = argparse.ArgumentParser(description="ANSI-BBS terminal.")
    parser.add_argument('-s', '--serial', dest='serial', action='store', metavar='dev[,rate]', help="attach to a serial port")
    parser.add_argument('-t', '--tcp', dest='tcp', action='store', metavar='host[:port]', help="make a TCP connection")
    parser.add_argument('-r', '--replay', dest='replay', action='store', metavar='logfile', help="replay a capture log")
    parser.add_argument('--scheme', dest='colorscheme', action='store', metavar='colorscheme', help="pick a color scheme")
    args = parser.parse_args()
    #print(vars(args))
    endpoints = {'serial', 'tcp', 'replay'}.intersection({k: v for k, v in vars(parser.parse_args()).items() if v is not None})
    if len(endpoints) != 1:
        parser.print_usage()
        sys.exit(2)
    if args.serial:
        serialparam = args.serial.split(',')
        if len(serialparam) > 2:
            print("Serial: Too many colons.")
            sys.exit(2)
        serialdev = serialparam[0]
        if len(serialparam) > 1:
            serialrate = int(serialparam[1])
        else:
            serialrate = 115200
        from EndpointSerial import EndpointSerial
        endpoint = EndpointSerial(device=serialdev, rate=serialrate)
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
        from EndpointTCP import EndpointTCP
        endpoint = EndpointTCP(host=host, port=port)
    if args.replay:
        from EndpointReplay import EndpointReplay
        endpoint = EndpointReplay(path=args.replay)
    fontpath = "/usr/share/fonts/misc/Bm437_Amstrad_PC-2y.otb"
    #fontpath = "/usr/share/fonts/misc/Bm437_IBM_VGA_9x16.otb"
    #fontpath = "/usr/share/fonts/misc/Bm437_IBM_XGA-AI_12x23.otb"
    from Term import Term
    term = Term()
    from KeyboardTranslatorBasic import KeyboardTranslatorBasic
    translator = KeyboardTranslatorBasic()
    term.setkeyboardtranslator(translator)
    term.setfont(fontpath)
    if args.colorscheme:
        result = term.setcolorscheme(args.colorscheme)
        if result != args.colorscheme:
            print(f"Color schemes available: {result}")
            sys.exit(2)
        del result
    term.attach(endpoint)
    term.loop()
    return
if __name__ == "__main__":
    main()
