from .. import Provider as HorseProvider


class Provider(HorseProvider):

    country_codes = [840,]

    def __init__(self, object):
        country_codes = [840, ]
        super().__init__(object)


    def country_of_birth(self):
        return 840


    def horse_size(self):

        return super().horse_size('hands')