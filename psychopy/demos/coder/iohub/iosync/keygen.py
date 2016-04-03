# -*- coding: utf-8 -*-
"""
A simple example of how to use ioSync as a USB keyboard (iosync keyboard)
that can be programatically instructed to press and release a single key for
a given duration.

An iosync keyboard key press / release is detected by the OS in the same
way as standard USB keyboard events.

This demo requires that an ioSync device is correctly connected to the
computer running this script.

Limitations of iosync keyboard:
1. Only one key can be pressed by the iosync keyboard at a time. If
   another call to generateKeyboardEvent() is made before the last iosync
   keyboard press has been released, the last key is released at the same
   time as the new key is pressed.
2. Key_symbol must be a key in the
   iohub.devices.mcu.iosync.t3keymap.char2t3code dict.
3. Actual key press duration is quantized to 100 msec intervals.
   i.e. actual_msec_dur = int(requested_sec_dur * 10)
4. Modifiers are not currently supported, including Shift
  (i.e. no upper case letters either).
"""

import sys
from psychopy import core
from psychopy.iohub.client import launchHubServer
getTime = core.getTime

key_evts = "This is a test."
key_dur = 0.5
iki = 1.0
genkey_evts =[(c, key_dur) for c in key_evts]

mcu = None
io = None
iohub_config = {'mcu.iosync.MCU': dict(serial_port='auto',
                                       monitor_event_types=[]
                                       )
                }
io = launchHubServer(**iohub_config)
mcu = io.devices.mcu
kb = io.devices.keyboard
if mcu.isConnected():
    mcuport = mcu.getSerialPort()
    print("Connected to ioSync on Serial Port {}".format(mcuport))
else:
    print("Could not connect to ioSync Device...\n"
          "Ensure USB and power cables are plugged in")
    io.quit()
    core.wait(0.25)
    sys.exit()

io.clearEvents()
print("Generating keyboard events:\n")
for k, d in genkey_evts:
    mcu.generateKeyboardEvent(k, d)
    print("Requested key '{}' pressed for {} sec.".format(k, d))

    io.wait(iki)

    kb_evts = kb.getEvents()
    print ("Received {} kb events:".format(len(kb_evts)))
    for kbe in kb_evts:
        print("\t{}".format(kbe))
    print("------")


print("\nPress any Keyboard key to exit....")

kb.waitForKeys()
io.clearEvents()
io.quit()
