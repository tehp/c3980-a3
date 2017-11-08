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

# Import getters from gps.py
#from gps import get_lat
#from gps import get_lon

def print_time_and_coords(data_stream):
    data_stream.unpack(new_data)
    table_time = [
        [str(datetime.now()),  'Latitude: ' + str(get_lat()) + ' N', 'Longitude: ' + str(get_lon()) + ' W']
    ]
    time = SingleTable(table_time)
    print(time.table)
