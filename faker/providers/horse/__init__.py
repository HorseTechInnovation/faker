# coding=utf-8

from .. import BaseProvider
import itertools
from datetime import date
from faker.utils.distribution import choice_distribution
from random import randint
import calendar, random
import csv


class Provider(BaseProvider):
    """
    This provider is a collection of functions to generate personal profiles and identities.

    """
    # standard settings - may be modified by country
    '''
        Horse Seix
        Many male horses are gelded/neutered, so the code for sex includes this option.  Rarely a female horse can also be neutered. 
    '''

    SEX = {
        00 : "Not Known",
        10 : "Male", # entire/neutered not known
        11 : "Stallion", # entire
        12 : "Gelding",
        20 : "Female", # neutered not known
        21 : "Mare",
        22 : "Neutered female",
        30 : "Hermaphrodite",
    }
    # TODO: extend range of colours
    COLORS = ["bay", "chestnut", "black", "grey"]

    pios = {}
    pios_distribution = {}
    population = []
    population_distribution = []
    handles = []

    def __init__(self, object):

        super().__init__(object)
        # load csv files
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cwd = os.getcwd()
        # get list of countries and population
        csv_file = os.path.join(dir_path,'data/HorsePop.csv' )
        with open(csv_file, 'rt') as csvfile:
            # country,iso3166,population,pct_registered,confidence in pct_reg,source of pct_reg,pick_pct
            items = csv.DictReader(csvfile, delimiter=',')
            for item in items:
                self.population.append(item['iso3166'])
                self.population_distribution.append(int(item['pick_pct']))

        # get list of pios by country and numbers per org
        csv_file = os.path.join(dir_path, 'data/PIOs.csv')
        with open(csv_file, 'rt') as csvfile:

            # name,full_org_id,country, org_id,num_reg,source_of_num_reg
            items = csv.DictReader(csvfile, delimiter=',')
            for item in items:
                if item['country'] in self.pios.keys():
                    self.pios[item['country']].append(item['org_id'])
                    self.pios_distribution[item['country']].append(int(item['num_reg']))
                else:
                    self.pios[item['country']] = [item['org_id'],]
                    self.pios_distribution[item['country']] = [int(item['num_reg']),]

        csv_file = os.path.join(dir_path,'data/horse_handles.csv' )
        with open(csv_file, 'rt') as csvfile:
            # one name per line
            items = csv.reader(csvfile, )
            for item in items:
                self.handles.append(item[0])


    #list(set(seq))
    def simple_horse(self):
        """
        Generates a basic profile with horse informations

        """
        sex = self.generator.horse_sex()


        # TODO: generate horse names
        if sex >= 20:
            name = self.generator.name_female()
        else:
            name = self.generator.name_male()

        country = self.generator.country_of_birth()

        return {
            "handle": self.generator.handle(),
            "name": name,
            "sex": sex,
            "color": self.generator.horse_color(),
            "size": self.generator.horse_size(),
            "dob": self.generator.horse_dob(),
            "chipid": self.generator.chipid(),
            "country_of_birth": country,
            "ueln": self.generator.ueln(country),
        }

    def horse_sex(self):
        '''
        Many male horses are gelded/neutered, so the code for sex includes this option.  Rarely a female horse can also be neutered. The full list is:

    00 - Not Known
    10 - Male - entire/neutered not known
    11 - Stallion - entire
    12 - Gelding
    20 - Female - neutered not known
    21 - Mare
    22 - Neutered female
    30 - Hermaphrodite

        :return:
        '''

        sex_choices = list(self.SEX.keys())
        p = (0.05,0.05, 0.4, 0.05, 0.01, 0.4, 0.01, 0.01)

        return choice_distribution(sex_choices, p)

    def horse_color(self):
        #https://en.wikipedia.org/wiki/Equine_coat_color
        #http://www.animalgenetics.us/Equine/CCalculator1.asp

        p = [0.5, 0.3, 0.1, 0.1]

        return choice_distribution(self.COLORS, p)

    def horse_size(self, units = 'cms'):
        '''horses are measured in hands (4 inches per hand) or centimeters depending on country'''

        #TODO: get statistics for size to better reflect population
        #TODO: raise error if units is not cms or hands

        size_in_cms = random.choice([s for s in range(101, 182)])
        if units == 'hands':
            hands = int(size_in_cms/2.54) + abs(size_in_cms/2.54)
            return hands
        else:
            return size_in_cms

    def handle(self):
        return random.choice(self.handles)

    def horse_dob(self):
        this_year = date.today().year
        years = [y for y in range(this_year, this_year-40, -1)]

        # note that these do not add up to 100 and they are pure guesswork
        p = [0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04,
             0.03,0.03,0.03,0.03,0.02,0.02,0.02,0.02,0.02,0.02,
             0.01,0.01,0.01,0.01,0.01,0.01,0.01, 0.005, 0.005, 0.005,
             0.001, 0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001]


        year = choice_distribution(years, p)


        months = [m for m in range(1, 13)]
        # in northern hemisphere most horses are born in spring
        p = [0.2, 0.2, 0.2, 0.2, 0.1, 0.5, 0.2, 0.1, 0.01, 0.01, 0.01, 0.01]
        month = choice_distribution(months, p)

        dates = calendar.Calendar().itermonthdates(year, month)
        return random.choice([date for date in dates if date.month == month])



    def ueln(self, country):


        # choose breed society (PIO)
        pio = choice_distribution(self.pios[country], self.pios_distribution[country])

        # create random id
        id = randint(100000, 999999999)


        return "%s-%s-%s" % (country, pio, id)

    def chipid(self):
        '''the proportion of the horse population with chips varies from country to country.
        The default is that 50% of horses have chips
        see: https://en.wikipedia.org/wiki/Microchip_implant_(animal)

        TODO: return correct range of values'''

        horse_has_chip = randint(0, 1)
        if horse_has_chip:
            return "%s" % randint(100000000, 999999999)
        else:
            return ''

    def country_of_birth(self):

        return choice_distribution(self.population, self.population_distribution)

