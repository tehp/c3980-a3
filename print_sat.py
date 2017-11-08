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
