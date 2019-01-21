import math
import simplejson as json
from physmodels import solar, temptank
from decimal import Decimal

class Proceso:

    def __init__(self, sr=1):
        self.sr = sr
        self.counter = 0
        self.solarRad = solar.SolarRad()
        self.tempAmb = solar.TempAmb()
        self.tempTank = temptank.TempTank()
        self.tags={
                   'TEMP:WATER':{ 
                      'func': self.set_temp_water,
                      'var': 0},
                   'TEMP:AMB':{ 
                      'func': self.set_temp_amb,
                      'var': 0},
                   'RAD:SOLAR':{
                      'func': self.set_rad_solar,
                      'var': 0},
                   'TEMP:TANK':{
                       'func': self.set_temp_tank,
                       'var': 0
                              },
                        }

    def set_time(self, time):
        self.counter = time
        [self.tags[tag]['func']() for tag in self.tags]

    def get_states(self):
        return{tag:'{}'.format(round(self.tags[tag]['var'],2)) for tag in self.tags}

    def set_temp_water(self):
        self.tags['TEMP:WATER']['var'] = 10 *\
                math.sin(6.28 * self.counter / 100) + 10

    def set_rad_solar(self):
        self.tags['RAD:SOLAR']['var'] = Decimal(self.solarRad.get(self.counter))

    def set_temp_amb(self):
        self.tags['TEMP:AMB']['var'] = self.tempAmb.get(self.counter)

    def set_temp_tank(self):
        self.tags['TEMP:TANK']['var'] = self.tempTank.get(self.counter)

    def reset(self):
        for tag in self.tags:
            self.tags[tag]['var'] = 0
        self.counter = 0


    def __str__(self):
        return json.dumps(self.get_states())

    def get_tags(self):
        return [tag for tag in self.tags]

