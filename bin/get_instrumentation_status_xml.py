#!/usr/bin/env python

import optparse, time
import cbp.cbp_instrument as CBP
import cbp
import cbp.shutter
import thorlabs

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-d","--duration",default=1,type=int)
    parser.add_option("-w","--wavelength",default=600,type=int)
    parser.add_option("-f","--filename",default="/tmp/test.xml")
    parser.add_option("-s","--shutter",default=1,type=int)

    parser.add_option("-v","--verbose", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

# Parse command line
opts = parse_commandline()
laser_interface = cbp.laser.LaserSerialInterface(loop=False)
laser_interface.change_wavelength(opts.wavelength)

#print "closed shutter"
#thorlabs.thorlabs.main(val=2)
#cbp.shutter.main(runtype="shutter", val=1)

start_time = time.time()
#cbp = CBP.CBP(phidget=True,birger=True,potentiometer=True,laser=True,filter_wheel=True,keithley=True,spectrograph=True)
cbp_inst = CBP.CBP(phidget=False,birger=False,potentiometer=False,laser=False,filter_wheel=False,keithley=True,spectrograph=True,flipper=True)

cbp_inst.flipper.run_flipper(2)

if opts.shutter == 1:
    doShutter = True
elif opts.shutter == 0:
    doShutter = False

cbp_inst.write_status_log_xml(outfile=opts.filename,duration=opts.duration,doShutter=doShutter)

