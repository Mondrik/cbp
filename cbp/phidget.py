#!/usr/bin/env python

"""
This module is for communicating with the phidget instruments.

.. module:: phidget
    :platform: unix
    :synopsis: This module is for communicating with phidget instruments.

.. codeauthor:: Adam Stelmack, Michael Coughlin, Eric Coughlin

Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.8'
__date__ = 'May 17 2010'

#Basic imports
from ctypes import *
import sys

import numpy as np
import os
if 'TESTENVIRONMENT' in os.environ:
    import mock
    sys.modules['Phidgets'] = mock.Mock()
else:
    #Phidget specific imports
    from Phidgets.Phidget import Phidget
    from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
    from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
    from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan
    from Phidgets.Phidget import PhidgetLogLevel


class CbpPhidget:
    """
    This is the class that communicates with the phidget.
    """
    def __init__(self):
        self.status = None
        self.spatial = self.create_spatial()
        

    def create_spatial(self):
        try:
            spatial = Spatial()
            self.status = "connected"
            return spatial
        except RuntimeError as e:
            self.status = "not connected"
            print("Runtime Exception: %s" % e.details)

    def check_status(self):
        try:
            self.spatial.getDeviceID()
        except Exception as e:
            self.status = "not connected"

    # Information Display Function
    def DisplayDeviceInfo(self):
        return
        # print("|------------|----------------------------------|--------------|------------|")
        # print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
        # print("|------------|----------------------------------|--------------|------------|")
        # print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (spatial.isAttached(), spatial.getDeviceName(), spatial.getSerialNum(), spatial.getDeviceVersion()))
        # print("|------------|----------------------------------|--------------|------------|")
        # print("Number of Acceleration Axes: %i" % (spatial.getAccelerationAxisCount()))
        # print("Number of Gyro Axes: %i" % (spatial.getGyroAxisCount()))
        # print("Number of Compass Axes: %i" % (spatial.getCompassAxisCount()))

    # Event Handler Callback Functions
    def SpatialAttached(self, e):
        attached = e.device
        # print("Spatial %i Attached!" % (attached.getSerialNum()))

    def SpatialDetached(self, e):
        detached = e.device
        # print("Spatial %i Detached!" % (detached.getSerialNum()))

    def SpatialError(self, e):
        try:
            source = e.device
            print("Spatial %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

    def SpatialData(self, e):
        source = e.device
        # print("Spatial %i: Amount of data %i" % (source.getSerialNum(), len(e.spatialData)))

        for index, spatialData in enumerate(e.spatialData):
            x = spatialData.Acceleration[0]
            y = spatialData.Acceleration[1]
            z = spatialData.Acceleration[2]
            xymag = np.sqrt(x ** 2 + y ** 2)
            xyzmag = np.sqrt(x ** 2 + y ** 2 + z ** 2)

            angle = (360.0 / (2 * np.pi)) * np.arctan(xymag / z)

            # print "%6f %6f %6f %6f" % (x,y,z,mag)
            # print("=== Data Set: %i ===" % (index))
            # if len(spatialData.Acceleration) > 0:
            #    print("Acceleration> x: %6f  y: %6f  z: %6f" % (spatialData.Acceleration[0], spatialData.Acceleration[1], spatialData.Acceleration[2]))
            # if len(spatialData.AngularRate) > 0:
            #    print("Angular Rate> x: %6f  y: %6f  z: %6f" % (spatialData.AngularRate[0], spatialData.AngularRate[1], spatialData.AngularRate[2]))
            # if len(spatialData.MagneticField) > 0:
            #    print("Magnetic Field> x: %6f  y: %6f  z: %6f" % (spatialData.MagneticField[0], spatialData.MagneticField[1], spatialData.MagneticField[2]))
            # print("Time Span> Seconds Elapsed: %i  microseconds since last packet: %i" % (spatialData.Timestamp.seconds, spatialData.Timestamp.microSeconds))

            # print("------------------------------------------")

    def set_handlers(self):
        spatial = self.spatial
        try:
            # logging example, uncomment to generate a log file
            # spatial.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")

            spatial.setOnAttachHandler(SpatialAttached)
            spatial.setOnDetachHandler(SpatialDetached)
            spatial.setOnErrorhandler(SpatialError)
            spatial.setOnSpatialDataHandler(SpatialData)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

    def open_phidget(self):
        spatial = self.spatial
        try:
            spatial.openPhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

    def wait_for_attach(self):
        spatial = self.spatial
        try:
            spatial.waitForAttach(10000)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            try:
                spatial.closePhidget()
            except PhidgetException as e:
                print("Phidget Exception %i: %s" % (e.code, e.details))
                print("Exiting....")
                exit(1)
            print("Exiting....")
            exit(1)
        else:
            spatial.setDataRate(4)
            self.DisplayDeviceInfo()

    def do_phidget(self, nave=10000):
        """
        This method returns the x,y,z coordinates of the phidget and the angle.

        :param nave:
        :return:
        """
        self.set_handlers()

        # print("Opening phidget object....")

        self.open_phidget()

        # print("Waiting for attach....")

        self.wait_for_attach()

        # print("Press Enter to quit....")

        data = True
        while data:
            try:
                x = self.spatial.getAcceleration(0)
                data = False
            except:
                data = True
        xs = []
        ys = []
        zs = []
        for i in xrange(nave):
            try:
                x = self.spatial.getAcceleration(0)
                y = self.spatial.getAcceleration(1)
                z = self.spatial.getAcceleration(2)

                xs.append(x)
                ys.append(y)
                zs.append(z)
            except:
                continue

        xs = np.array(xs)
        ys = np.array(ys)
        zs = np.array(zs)

        x = np.median(xs)
        y = np.median(ys)
        z = np.median(zs)

        if np.abs(x) <= np.abs(y):
            if y <= 0:
                direction = -1
            else:
                direction = 1
        elif np.abs(x) > np.abs(y):
            if x <= 0:
                direction = -1
            else:
                direction = 1

        xymag = np.sqrt(x ** 2 + y ** 2)
        xyzmag = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        angle = direction * (360.0 / (2 * np.pi)) * np.arctan(xymag / z)

        try:
            self.spatial.closePhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

        return x, y, z, angle

        # print("Done.")
        # exit(0)




#Information Display Function
def DisplayDeviceInfo(spatial):
    return
    #print("|------------|----------------------------------|--------------|------------|")
    #print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    #print("|------------|----------------------------------|--------------|------------|")
    #print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (spatial.isAttached(), spatial.getDeviceName(), spatial.getSerialNum(), spatial.getDeviceVersion()))
    #print("|------------|----------------------------------|--------------|------------|")
    #print("Number of Acceleration Axes: %i" % (spatial.getAccelerationAxisCount()))
    #print("Number of Gyro Axes: %i" % (spatial.getGyroAxisCount()))
    #print("Number of Compass Axes: %i" % (spatial.getCompassAxisCount()))

#Event Handler Callback Functions
def SpatialAttached(e):
    attached = e.device
    #print("Spatial %i Attached!" % (attached.getSerialNum()))

def SpatialDetached(e):
    detached = e.device
    #print("Spatial %i Detached!" % (detached.getSerialNum()))

def SpatialError(e):
    try:
        source = e.device
        print("Spatial %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def SpatialData(e):
    source = e.device
    #print("Spatial %i: Amount of data %i" % (source.getSerialNum(), len(e.spatialData)))

    for index, spatialData in enumerate(e.spatialData):
        x = spatialData.Acceleration[0]
        y = spatialData.Acceleration[1]
        z = spatialData.Acceleration[2]
        xymag = np.sqrt(x**2 + y**2)
        xyzmag = np.sqrt(x**2 + y**2 + z**2)
 
        angle = (360.0/(2*np.pi))*np.arctan(xymag/z)

        #print "%6f %6f %6f %6f" % (x,y,z,mag)
        #print("=== Data Set: %i ===" % (index))
        #if len(spatialData.Acceleration) > 0:
        #    print("Acceleration> x: %6f  y: %6f  z: %6f" % (spatialData.Acceleration[0], spatialData.Acceleration[1], spatialData.Acceleration[2]))
        #if len(spatialData.AngularRate) > 0:
        #    print("Angular Rate> x: %6f  y: %6f  z: %6f" % (spatialData.AngularRate[0], spatialData.AngularRate[1], spatialData.AngularRate[2]))
        #if len(spatialData.MagneticField) > 0:
        #    print("Magnetic Field> x: %6f  y: %6f  z: %6f" % (spatialData.MagneticField[0], spatialData.MagneticField[1], spatialData.MagneticField[2]))
        #print("Time Span> Seconds Elapsed: %i  microseconds since last packet: %i" % (spatialData.Timestamp.seconds, spatialData.Timestamp.microSeconds))
    
    #print("------------------------------------------")


def main(nave=10000):
    #Main Program Code
    phidget = CbpPhidget()
    return phidget.do_phidget(nave)

if __name__ == "__main__":
    nave = 10000 
    x,y,z,angle = main(nave=nave)
    print x,y,z,angle
