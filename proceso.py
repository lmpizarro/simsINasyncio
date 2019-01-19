import math
import simplejson as json

class Proceso:

    def __init__(self, sr=1):
        self.sr = sr
        self.counter = 0
        self.tags={'TEMP:WATER':{ 
                     'func': self.set_temp_water,
                     'var': 0}}

    def set_time(self, time):
        self.counter = time
        [self.tags[tag]['func']() for tag in self.tags]

    def get_states(self):
        return{tag:self.tags[tag]['var'] for tag in self.tags}

    def set_temp_water(self):
        self.tags['TEMP:WATER']['var'] = 10 *\
                math.sin(6.28 * self.counter / 100) + 10

    def reset(self):
        for tag in self.tags:
            self.tags[tag]['var'] = 0
        self.counter = 0

    def __str__(self):
        return json.dumps(self.get_states())

    def get_tags(self):
        return [tag for tag in self.tags]


