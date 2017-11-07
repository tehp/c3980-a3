#-------------------------------------------------------------------------------
#-- SOURCE FILE: gps.py - A program that monitors and displays data from a gpsd
#-- instance. Data includes coordinates, satellite information.
#--
#-- PROGRAM: GPS Wrapper
#--
#-- FUNCTIONS:
#-- get_lon()
#-- get_lat()
#-- print_sat_information(sat)
#-- print_time_and_coords(data_stream)
#--
#--
#-- DATE: November 5th, 2017
#--
#-- REVISIONS: (Date and Description)
#-- N/A
#--
#-- DESIGNER: Mackenzie Craig, Angus Lam
#--
#-- PROGRAMMER: Mackenzie Craig, Angus Lam
#--
#-- NOTES:
#-- The program attatches itself to an instance of the gpsd daemon.
#-- Assuming an instance is running, it will print out information of the
#-- satellites that the connected device can discover. If a fix is successfully
#-- made, the program will print out the calculated coordinates of your current
#-- position.
#--
#-- Tested using python3. Other versions are not supported.
#--
#-- Installing: pip3 install gps3 gpsd-py3 terminaltables
#--
#-- Running: python3 gps.py [speed]
#--
#-- Arguments:
#--     [speed] - seconds (integer)
#--         specifies the time between refreshes of output.
#--         setting this to 0 or not including it at all sets the program to run
#--         as fast as gpsd allows it to.
#--
#-------------------------------------------------------------------------------

from gps3 import gps3
from datetime import datetime
from terminaltables import SingleTable
import gpsd
import argparse
import sys
import time

# Speed at which to refresh the program
# First command line argument
speed = int(sys.argv[1])

print("SPEED: " + str(speed))

# Setup connection
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

gpsd.connect() # GPSD old API - Can be removed when packet is not depended on anymore.

def get_lon():
    return data_stream.TPV['lon']

def get_lat():
    return data_stream.TPV['lat']

#-------------------------------------------------------------------------------
#--
#-- DATE: November 5th, 2017
#--
#-- REVISIONS:
#-- N/A
#--
#-- DESIGNER: Angus Lam, Mackenzie Craig
#--
#-- PROGRAMMER: Mackenzie Craig
#--
#-- INTERFACE: print_time_and_coords(data_stream)
#--
#-- RETURNS: void
#--
#-- NOTES:
#-- This function is called whenever the main loop occurs (based on 'speed').
#-- Prints the time, as well as lat/lon.
#-------------------------------------------------------------------------------
def print_time_and_coords(data_stream):
    data_stream.unpack(new_data)
    table_time = [
        [str(datetime.now()),  'Latitude: ' + str(get_lat()) + ' N', 'Longitude: ' + str(get_lon()) + ' W']
    ]
    time = SingleTable(table_time)
    print(time.table)

#-------------------------------------------------------------------------------
#--
#-- DATE: November 5th, 2017
#--
#-- REVISIONS:
#-- N/A
#--
#-- DESIGNER: Angus Lam
#--
#-- PROGRAMMER: Mackenzie Craig, Angus Lam
#--
#-- INTERFACE: print_sat_information(sat)
#--
#-- RETURNS: a string containing PRN, Elevation, Azimuth, SNR, Used (Y/N)
#--
#-- NOTES:
#-- This function is called once for each satellite seen.
#-- See print_time_and_coords(data_stream).
#-------------------------------------------------------------------------------
def print_sat_information(sat):
    prn = "PRN: " + str(sat["PRN"])
    az = "Azimuth: " + str(sat["az"])
    ss = "SNR: " + str(sat["ss"])
    el = "Elevation: " + str(sat["el"])
    if sat["used"]:
        used = "Used: Y"
    else:
        used = "Used: N"

    prnF = '{0: <8}'.format(prn)
    elF = '{0: <13}'.format(el)
    azF = '{0: <13}'.format(az)
    ssF = '{0: <7}'.format(ss)
    usedF = '{0: <7}'.format(used)

    table_time = [
        [prnF, elF, azF, ssF, usedF]
    ]
    time = SingleTable(table_time)
    print(time.table)


#-------------------------------------------------------------------------------
#--
#-- DATE: November 5th, 2017
#--
#-- REVISIONS:
#-- N/A
#--
#-- DESIGNER: Angus Lam, Mackenzie Craig
#--
#-- PROGRAMMER: Mackenzie Craig, Angus Lam
#--
#-- NOTES:
#-- This is the main loop of the program. The loop waits for new data in the
#-- socket. When it detects new data, it unpacks it, and passes that information
#-- to print_sat_information, once per sat. The loop also calls the
#-- print_time_and_coords method once per new data in the socket.
#-------------------------------------------------------------------------------
for new_data in gps_socket:
    if new_data:
        # Prep data
        data_stream.unpack(new_data)
        # packet = gpsd.get_current() # GPSD old API, not needed anymore
        # Print info for each satelite seen
        if data_stream.SKY["satellites"] != "n/a":
            for sat in data_stream.SKY["satellites"]:
                print_sat_information(sat)
        # Print time, lat, lon
        print_time_and_coords(data_stream)
        time.sleep(speed)
        print(chr(27) + "[2J")
