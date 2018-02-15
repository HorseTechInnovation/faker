from .. import Provider as HorseProvider
import random

class Provider(HorseProvider):

    country_codes = [372,]
    UNITS = 'cms'   # horses measured in hands or cms?

    def country_of_birth(self):
        #TODO: handle multiple country codes
        return self.country_codes[0]


