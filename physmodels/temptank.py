import datetime
import random
import pytz

class TempTank:
    def __init__(self, mean_temp = 20, sigma = .1, rand=True):
        self.temperature = mean_temp
        self.mean_temp = mean_temp
        self.sigma = sigma
        self.rand = rand

    def set(self, counter, date=None):
        if date == None:
            date = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        if self.rand:
            self.temperature = random.gauss(self.mean_temp, self.sigma)
        else:
            self.temperature =  self.mean_temp

    def get(self, counter, date=None):
        self.set(counter, date=None)
        return self.temperature
  
    def __str__(self):
        return 'TEMP:TANK {}'.format(self.temperature)

