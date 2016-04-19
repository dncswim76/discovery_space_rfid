#!/usr/bin/env python

#Basic imports
from ctypes import *
import sys
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, OutputChangeEventArgs, TagEventArgs
from Phidgets.Devices.RFID import RFID, RFIDTagProtocol
from Phidgets.Phidget import PhidgetLogLevel

import pyautogui
import time

#Create an RFID object
try:
    rfid = RFID()
except RuntimeError as e:
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Runtime Exception: %s" % e.details)
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Exiting....")
    exit(1)


#Information Display Function
def displayDeviceInfo():
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "|------------|----------------------------------|--------------|------------|")
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "|------------|----------------------------------|--------------|------------|")
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "|- %8s -|- %30s -|- %10d -|- %8d -|" % (rfid.isAttached(), rfid.getDeviceName(), rfid.getSerialNum(), rfid.getDeviceVersion()))
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "|------------|----------------------------------|--------------|------------|")
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Number of outputs: %i -- Antenna Status: %s -- Onboard LED Status: %s" % (rfid.getOutputCount(), rfid.getAntennaOn(), rfid.getLEDOn()))


#Event Handler Callback Functions
def rfidAttached(e):
    attached = e.device
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "RFID %i Attached!" % (attached.getSerialNum()))


def rfidDetached(e):
    detached = e.device
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "RFID %i Detached!" % (detached.getSerialNum()))

def rfidError(e):
    try:
        source = e.device
        rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "RFID %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Phidget Exception %i: %s" % (e.code, e.details))


def rfidOutputChanged(e):
    source = e.device
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "RFID %i: Output %i State: %s" % (source.getSerialNum(), e.index, e.state))


def rfidTagGained(e):
    source = e.device
    rfid.setLEDOn(1)
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "RFID %i: Tag Read: %s" % (source.getSerialNum(), e.tag))
    #Fake keyboard input as RFID tag
    pyautogui.typewrite('%s\r' % (str(e.tag)))


def rfidTagLost(e):
    source = e.device
    rfid.setLEDOn(0)
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "RFID %i: Tag Lost: %s" % (source.getSerialNum(), e.tag))


#Main Program Code
try:
    rfid.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")
    rfid.setOnAttachHandler(rfidAttached)
    rfid.setOnDetachHandler(rfidDetached)
    rfid.setOnErrorhandler(rfidError)
    rfid.setOnOutputChangeHandler(rfidOutputChanged)
    rfid.setOnTagHandler(rfidTagGained)
    rfid.setOnTagLostHandler(rfidTagLost)
except PhidgetException as e:
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Phidget Exception %i: %s" % (e.code, e.details))
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Exiting....")
    exit(1)

rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Opening phidget object....")

try:
    rfid.openPhidget()
except PhidgetException as e:
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Phidget Exception %i: %s" % (e.code, e.details))
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Exiting....")
    exit(1)

rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Waiting for attach....")

try:
    rfid.waitForAttach(10000)
except PhidgetException as e:
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Phidget Exception %i: %s" % (e.code, e.details))
    try:
        rfid.closePhidget()
    except PhidgetException as e:
        rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Phidget Exception %i: %s" % (e.code, e.details))
        rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Exiting....")
        exit(1)
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Exiting....")
    exit(1)
else:
    displayDeviceInfo()

rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Turning on the RFID antenna....")
rfid.setAntennaOn(True)

#Loop indefinitely - sleep has low overhead
while True:
    time.sleep(sys.maxint)

'''
rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Press Enter to quit....")

chr = sys.stdin.read(1)
try:
    lastTag = rfid.getLastTag()
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Last Tag: %s" % (lastTag))
except PhidgetException as e:
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Phidget Exception %i: %s" % (e.code, e.details))

rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Closing...")

try:
    rfid.closePhidget()
except PhidgetException as e:
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Phidget Exception %i: %s" % (e.code, e.details))
    rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Exiting....")
    exit(1)

rfid.log(PhidgetLogLevel.PHIDGET_LOG_INFO, None, "Done.")
exit(0)
'''
