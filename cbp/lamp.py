#!/usr/bin/env python

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-l","--lamp",default=100,type=int)
    parser.add_option("-c","--doCompile", action="store_true",default=False)
    parser.add_option("--doLamp", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

def run_lamp(lamp):
    shutter_command = "picocom -b 57600 /dev/ttyACM.LAMP"
    child = pexpect.spawn (shutter_command)
    loop = True
    while loop:
        i = child.expect ([pexpect.TIMEOUT,'\n'], timeout = 2)
        #print child.before, child.after
        if i == 0: # Timeout
            argstring = 'args %d 1\r'%(lamp)
            print argstring
            child.sendline(argstring)
            loop = False
        if i == 1:
            continue
    child.close()

def main(runtype = "compile", val = 0):

    if runtype == "compile":
        steps_command = "cd /home/pi/Code/arduino/lamp/; ./compile.sh"
        os.system(steps_command)
    elif runtype == "lamp":
        if val > 255 or val < 0:
            raise Exception("Lamp must be between 0-255")
        print "Running the lamp ..."
        run_lamp(val)

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doCompile:
        main(runtype = "compile")
    if opts.doLamp:
        main(runtype = "lamp", val = opts.lamp)

