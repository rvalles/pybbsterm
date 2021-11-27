# pybbsterm: Terminal emulator for calling BBSs.

## Use cases (non-exhaustive)
* Explore terminal protocols.
* Connect to BBSs.

## Highlights
* `Python 3.8+` code.
* Built with `pygame`.
* Targets `ANSI-BBS` compatibility.
  * Already has great compatibility with a range of BBSs.
* `cp437` translation.
* Multiple connectivity options.
  * `EndpointTCP` connects the terminal to a remote host:port.
    * Call internet-exposed BBSs.
  * `EndpointReplay` allows for playing stored logs.
    * Useful for debugging.
  * `EndpointSerial` attaches terminal to a serial port.
    * Null-modem direct connections.
    * Interface with modems, call remote computers.
    * Requires `pySerial`.
* Terminal font is settable.
* Multiple color schemes.
* Easy to use.
* MIT License. See LICENSE file.

## Usage
* Ensure `Python 3.8+`, `pygame 2.0+`, `pySerial 3.1+` are installed.
* Run `pybbsterm.py -h` for verbose usage help.
* Run `pybbsterm.py --scheme help` for list of available color schemes.
* Use of bitmap fonts is recommended.
  * `Open Type Bitmap` (`.otb`) fonts preferred
  * A good set is `oldschool-pc-fonts` found at: https://int10h.org
* Keyboard shortcuts
  * `Alt-x` will exit.
  * `PrtScn` and `Shift-F12` will start/finish capture of incoming bytes into file.
  * `Control +/-` will integer-scale the output window.
  * `Shift-Esc` will close connection.
  * `Shift-F1` to `Shift-F4` will call functions specific to the endpoint.

## Caveats
* File transfers are not yet implemented.
* Encoding is always `cp437`.
* Keyboard translation is still poor. A hardcoded UK layout is provided.
* ANSI-BBS specification isn't yet 100% implemented.

## Author
Roc Vallès Domènech
