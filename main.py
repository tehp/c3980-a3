# Packages: gps3, gpsd-py3

from gps3 import gps3
from datetime import datetime
import gpsd
import argparse
import sys

# Speed at which to refresh the program
speed = int(sys.argv[1])


print("SPEED: " + str(speed))

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

gpsd.connect() # GPSD old API

def get_alt():
    return data_stream.TPV['alt']

def get_lat():
    return data_stream.TPV['lat']

def print_sat_information(sat):
    prn = "PRN: " + str(sat["PRN"])
    azimuth = "Azimuth: " + str(sat["az"])
    snr = "SNR: " + str(sat["ss"])
    elev = "Elevation: " + str(sat["el"])
    used = "Used: "
    if sat["used"]:
        used += "Y"
    else:
        used += "N"
    return '{0: <8}'.format(prn) + "    " + '{0: <13}'.format(elev) + "    " + '{0: <13}'.format(azimuth) + "    " + '{0: <7}'.format(snr) + "    " + '{0: <7}'.format(used)

def print_time_and_coords(data_stream):
    data_stream.unpack(new_data)
    print(str(datetime.now()) + " Latitude: " + str(data_stream.TPV['lat']) + " N: Longitude: " + str(data_stream.TPV['lon']) + " W")

for new_data in gps_socket:
    if new_data:
        # Prep data
        data_stream.unpack(new_data)
        # packet = gpsd.get_current() # GPSD old API, not needed anymore
        # Print info for each satelite seen
        if data_stream.SKY["satellites"] != "n/a":
            for sat in data_stream.SKY["satellites"]:
                print(print_sat_information(sat))
        # Print time, lat, lon
        print_time_and_coords(data_stream)
        print(" ")
        time.sleep(speed)
