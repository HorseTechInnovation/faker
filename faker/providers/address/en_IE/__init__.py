from __future__ import unicode_literals
from collections import OrderedDict

from ..en import Provider as AddressProvider
from faker.utils.distribution import choice_distribution
import csv
import random


#TODO: this needs to be fully modified for Ireland - Postcodes are setup as UK postcodes for example

class Provider(AddressProvider):



    building_number_formats = ('#', '##', '###')
    street_suffixes = (
        'alley',
        'avenue',
        'branch',
        'bridge',
        'brook',
        'brooks',
        'burg',
        'burgs',
        'bypass',
        'camp',
        'canyon',
        'cape',
        'causeway',
        'center',
        'centers',
        'circle',
        'circles',
        'cliff',
        'cliffs',
        'club',
        'common',
        'corner',
        'corners',
        'course',
        'court',
        'courts',
        'cove',
        'coves',
        'creek',
        'crescent',
        'crest',
        'crossing',
        'crossroad',
        'curve',
        'dale',
        'dam',
        'divide',
        'drive',
        'drive',
        'drives',
        'estate',
        'estates',
        'expressway',
        'extension',
        'extensions',
        'fall',
        'falls',
        'ferry',
        'field',
        'fields',
        'flat',
        'flats',
        'ford',
        'fords',
        'forest',
        'forge',
        'forges',
        'fork',
        'forks',
        'fort',
        'freeway',
        'garden',
        'gardens',
        'gateway',
        'glen',
        'glens',
        'green',
        'greens',
        'grove',
        'groves',
        'harbor',
        'harbors',
        'haven',
        'heights',
        'highway',
        'hill',
        'hills',
        'hollow',
        'inlet',
        'inlet',
        'island',
        'island',
        'islands',
        'islands',
        'isle',
        'isle',
        'junction',
        'junctions',
        'key',
        'keys',
        'knoll',
        'knolls',
        'lake',
        'lakes',
        'land',
        'landing',
        'lane',
        'light',
        'lights',
        'loaf',
        'lock',
        'locks',
        'locks',
        'lodge',
        'lodge',
        'loop',
        'mall',
        'manor',
        'manors',
        'meadow',
        'meadows',
        'mews',
        'mill',
        'mills',
        'mission',
        'mission',
        'motorway',
        'mount',
        'mountain',
        'mountain',
        'mountains',
        'mountains',
        'neck',
        'orchard',
        'oval',
        'overpass',
        'park',
        'parks',
        'parkway',
        'parkways',
        'pass',
        'passage',
        'path',
        'pike',
        'pine',
        'pines',
        'place',
        'plain',
        'plains',
        'plains',
        'plaza',
        'plaza',
        'point',
        'points',
        'port',
        'port',
        'ports',
        'ports',
        'prairie',
        'prairie',
        'radial',
        'ramp',
        'ranch',
        'rapid',
        'rapids',
        'rest',
        'ridge',
        'ridges',
        'river',
        'road',
        'road',
        'roads',
        'roads',
        'route',
        'row',
        'rue',
        'run',
        'shoal',
        'shoals',
        'shore',
        'shores',
        'skyway',
        'spring',
        'springs',
        'springs',
        'spur',
        'spurs',
        'square',
        'square',
        'squares',
        'squares',
        'station',
        'station',
        'stravenue',
        'stravenue',
        'stream',
        'stream',
        'street',
        'street',
        'streets',
        'summit',
        'summit',
        'terrace',
        'throughway',
        'trace',
        'track',
        'trafficway',
        'trail',
        'trail',
        'tunnel',
        'tunnel',
        'turnpike',
        'turnpike',
        'underpass',
        'union',
        'unions',
        'valley',
        'valleys',
        'via',
        'viaduct',
        'view',
        'views',
        'village',
        'village',
        'villages',
        'ville',
        'vista',
        'vista',
        'walk',
        'walks',
        'wall',
        'way',
        'ways',
        'well',
        'wells')

    POSTAL_ZONES = (
        'AB', 'AL', 'B', 'BA', 'BB', 'BD', 'BH', 'BL', 'BN', 'BR',
        'BS', 'BT', 'CA', 'CB', 'CF', 'CH', 'CM', 'CO', 'CR', 'CT',
        'CV', 'CW', 'DA', 'DD', 'DE', 'DG', 'DH', 'DL', 'DN', 'DT',
        'DY', 'E', 'EC', 'EH', 'EN', 'EX', 'FK', 'FY', 'G', 'GL',
        'GY', 'GU', 'HA', 'HD', 'HG', 'HP', 'HR', 'HS', 'HU', 'HX',
        'IG', 'IM', 'IP', 'IV', 'JE', 'KA', 'KT', 'KW', 'KY', 'L',
        'LA', 'LD', 'LE', 'LL', 'LN', 'LS', 'LU', 'M', 'ME', 'MK',
        'ML', 'N', 'NE', 'NG', 'NN', 'NP', 'NR', 'NW', 'OL', 'OX',
        'PA', 'PE', 'PH', 'PL', 'PO', 'PR', 'RG', 'RH', 'RM', 'S',
        'SA', 'SE', 'SG', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SR',
        'SS', 'ST', 'SW', 'SY', 'TA', 'TD', 'TF', 'TN', 'TQ', 'TR',
        'TS', 'TW', 'UB', 'W', 'WA', 'WC', 'WD', 'WF', 'WN', 'WR',
        'WS', 'WV', 'YO', 'ZE'
    )

    POSTAL_ZONES_ONE_CHAR = [zone for zone in POSTAL_ZONES if len(zone) == 1]
    POSTAL_ZONES_TWO_CHARS = [zone for zone in POSTAL_ZONES if len(zone) == 2]

    postcode_formats = (
        'AN NEE',
        'ANN NEE',
        'PN NEE',
        'PNN NEE',
        'ANC NEE',
        'PND NEE',
    )

    _postcode_sets = OrderedDict((
        (' ', ' '),
        ('N', [str(i) for i in range(0, 10)]),
        ('A', POSTAL_ZONES_ONE_CHAR),
        ('B', 'ABCDEFGHKLMNOPQRSTUVWXY'),
        ('C', 'ABCDEFGHJKSTUW'),
        ('D', 'ABEHMNPRVWXY'),
        ('E', 'ABDEFGHJLNPQRSTUWXYZ'),
        ('P', POSTAL_ZONES_TWO_CHARS),
    ))


    street_name_formats = (
        '{{first_name}} {{street_suffix}}',
        '{{last_name}} {{street_suffix}}'
    )
    street_address_formats = (
        '{{building_number}} {{street_name}}',
        '{{secondary_address}}\n{{street_name}}',
    )
    address_formats = (
        "{{street_address}}\n{{city}}\n{{county}}",
    )
    secondary_address_formats = (
        'Flat #', 'Flat ##', 'Flat ##?', 'Studio #', 'Studio ##', 'Studio ##?')

    counties_by_town = {}
    population = []
    population_distribution = []

    def __init__(self, object):

        super().__init__(object)
        # load csv files
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cwd = os.getcwd()
        # get list of countries and population
        #TODO: this is not the full list of irish towns used in addresses and needs to be extended
        csv_file = os.path.join(dir_path,'data/irish_towns.csv' )
        with open(csv_file, 'rt') as csvfile:
            # country,iso3166,population,pct_registered,confidence in pct_reg,source of pct_reg,pick_pct
            items = csv.DictReader(csvfile, delimiter=',')
            for item in items:
                self.population.append(item['town'])
                self.population_distribution.append(int(item['population']))
                self.counties_by_town[item['town']] = item['county']


    def city_suffix(self):
        """
        :all cities listed so don't need this
        """
        return ''

    def city(self):
        """
        :example 'Cork'
        """
        return choice_distribution(self.population, self.population_distribution)

    def postcode(self):
        """
        See http://web.archive.org/web/20090930140939/http://www.govtalk.gov.uk/gdsc/html/noframes/PostCode-2-1-Release.htm
        """
        postcode = ''
        pattern = self.random_element(self.postcode_formats)
        for placeholder in pattern:
            postcode += self.random_element(self._postcode_sets[placeholder])
        return postcode



    def secondary_address(self):
        return self.bothify(self.random_element(self.secondary_address_formats))

    def county(self):
        return random.choice(list(self.counties_by_town.keys()))

    def country_code(self):
        return {'timezones': ['Europe/Dublin'],
                  'code': 'IE',
                  'continent': 'Europe',
                  'name': 'Republic of Ireland',
                  'capital': 'Dublin'},

    def country(self):
        return "Eire"

    def address(self):
        """
        currently only doing city or town addresses, needs to also do rural addresses
        """
        town = self.generator.city()
        county = self.counties_by_town[town]
        street = self.generator.street_address()
        return "%s, %s, Co %s" % (street, town, county)