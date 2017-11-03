from gps3 import gps3
from datetime import datetime
import gpsd

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

gpsd.connect() # GPSD for access to random stuff

def get_alt():
    return data_stream.TPV['alt']

def get_lat():
    return data_stream.TPV['lat']

def parse_satellite(satellite):
    prn = "PRN: " + str(satellite["PRN"])
    azimuth = "Azimuth: " + str(satellite["az"])
    snr = "SNR: " + str(satellite["ss"])
    elev = "Elevation: " + str(satellite["el"])
    used = "Used: "
    if satellite["used"]:
        used += "Y"
    else:
        used += "N"
    return prn + "    " + elev + "    " + azimuth + "    " + snr + "    " + used

for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        packet = gpsd.get_current() # GPSD
        # print('Alt = ', data_stream.TPV['alt'])
        # print('Lat = ', data_stream.TPV['lat'])
        if data_stream.SKY["satellites"] != "n/a":
            for sat in data_stream.SKY["satellites"]:
                print(parse_satellite(sat))
        print(str(datetime.now()) + " " + str(data_stream.TPV['alt']) + " " + str(data_stream.TPV['lat']))
        print(" ")
