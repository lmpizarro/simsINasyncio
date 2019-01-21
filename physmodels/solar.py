from pysolar import solar
import datetime
import pytz

#
#  https://www.hukseflux.com/products/solar-radiation-sensors/pyranometers/sr05-d1a3-pyranometer 
#

class SolarRad:
    def __init__(self, lat_deg=-34.6, 
                 long_deg=-58.382):
        # negative reckoning west from prime meridian in Greenwich, England
        # positive in the northern hemisphere
        self.lat = lat_deg
        self.long = long_deg

    def set(self, counter, date=None):
        if date == None:
            date = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        self.altitude_deg = solar.get_altitude(self.lat, self.long, date)
        self.rs = solar.radiation.get_radiation_direct(date, self.altitude_deg)
 
    def get(self, counter, date=None):
        self.set(counter, date=None)
        return self.rs

    def __str__(self):
        return 'Solar Radiation {}'.format(self.rs)

class TempAmb:
    def __init__ (self, cloud=.5):
        self.tamb = 273.15
        self.solarRad = SolarRad()
        self.cloud = cloud

    def set(self, counter, date=None):
        self.solarRad.set(counter, date)
        self.tamb = self.cloud * ((self.solarRad.rs * 0.05 + 258.15) - 273.15)

    def get(self, counter, date=None):
        self.set(counter, date)
        return self.tamb

    def __str__(self):
        return 'TEMP:AMB {}'.format(self.tamb)
