from .. import Provider as HorseProvider


class Provider(HorseProvider):

    country_code = 840

    def country_of_birth(self):
        return 840


    def horse_size(self):

        return super().horse_size('hands')