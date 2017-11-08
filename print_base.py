#-------------------------------------------------------------------------------
#--
#-- DATE: November 5th, 2017
#--
#-- REVISIONS:
#-- N/A
#--
#-- DESIGNER: Angus Lam
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

# Import getters from gps.py
#from gps import get_lat
#from gps import get_lon

from gps3 import gps3
import gpsd
from terminaltables import SingleTable


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

from datetime import datetime

def print_time_and_coords(data_stream, new_data, lat, lon):
    data_stream.unpack(new_data)
    table_time = [
        [str(datetime.now()),  'Latitude: ' + str(lat) + ' N', 'Longitude: ' + str(lon) + ' W']
    ]
    time = SingleTable(table_time)
    print(time.table)
