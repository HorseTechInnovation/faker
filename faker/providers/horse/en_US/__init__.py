from .. import Provider as HorseProvider


class Provider(HorseProvider):

    country_codes = [840,]
    UNITS = 'hands'   # horses measured in hands or cms?

    def __init__(self, object):
        self.country_codes = [840, ]
        super().__init__(object)


    def country_of_birth(self):
        return 840


