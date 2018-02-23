# coding=utf-8

from .. import BaseProvider
import itertools
from datetime import date, datetime
from faker.utils.distribution import choice_distribution
from random import randint
import calendar, random
import csv
import os

from .data import HORSE_HANDLES, PIOS, COUNTRY_POPULATION, HORSE_IMAGE_URLS


class Provider(BaseProvider):
    """
    This provider is a collection of functions to generate data related to horses.

    """
    # standard settings - may be modified by country
    '''
        Horse Sex
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
    SEX_PROPORTIONS = (0.05,0.05, 0.4, 0.05, 0.01, 0.4, 0.01, 0.01)

    # TODO: extend range of colours
    # these are the base colours used by the FEI: http://inside.fei.org/system/files/ID_of_horses_2014.pdf

    COLORS = ["brown","bay", "chestnut", "black", "grey", "strawberry", "piebald", "skewbald", "dun", "cream", "palomino", "appaloosa"]
    COLOURS_PROPORTIONS = (5,50,30,5,10,1,1,1,1,1,1,1)

    UNITS = "cms"

    data_dir = os.path.dirname(os.path.realpath(__file__))
    pios = {}
    pios_distribution = {}
    population = []
    population_distribution = []
    handles = []

    def __init__(self, object):

        super().__init__(object)
        # load csv files


        # get list of countries and population
        for item in COUNTRY_POPULATION:
                if int(item['pick']) > 0:
                    self.population.append(item['iso3166'])
                    self.population_distribution.append(int(item['pick']))

        # get list of Passport Issuing Authorities (PIOs) by country and numbers per PIO

        for item in PIOS:
                if item['country'] in self.pios.keys():
                    self.pios[item['country']].append(item['org_id'])
                    self.pios_distribution[item['country']].append(int(item['num_reg']))
                else:
                    self.pios[item['country']] = [item['org_id'],]
                    self.pios_distribution[item['country']] = [int(item['num_reg']),]



        # get possible names
        self.handles = HORSE_HANDLES


    def simple_horse(self):
        """
        Generates a basic profile with horse informations

        """
        name = self.generator.horse_name()
        handle = self.generator.horse_handle(name)

        country = self.generator.country_of_birth()

        return {
            "handle": handle,
            "name": name,
            "sex": self.generator.horse_sex(),
            "color": self.generator.horse_color(),
            "size": self.generator.horse_size(),
            "dob": self.generator.horse_dob(),
            "chipid": self.generator.chipid(),
            "country_of_birth": country,
            "ueln": self.generator.ueln(country),
            "image_url": self.generator.horse_pic(),
        }

    def horse_handle(self, name=None):
        '''handle is a short unique name, like a twitter handle.  In real life a horse might be called
        Cooragannive Diamond Star but have a short name of Blackie.  For the sake of tests, the handle
        is just the name with spaces removed.'''
        if name:
            return name.replace(" ",'')
        else:
            return random.choice(self.handles)


    def horse_name(self):

        color = self.generator.safe_color_name()
        handle = random.choice(self.handles)

        return "%s %s" % (color.title(), handle)

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

        return choice_distribution(sex_choices, self.SEX_PROPORTIONS)

    def horse_color(self):
        #https://en.wikipedia.org/wiki/Equine_coat_color
        #http://www.animalgenetics.us/Equine/CCalculator1.asp

        return choice_distribution(self.COLORS, self.COLOURS_PROPORTIONS)

    def horse_size(self, units = 'cms'):
        '''horses are measured in hands (4 inches per hand) or centimeters depending on country'''

        #TODO: get statistics for size to better reflect population
        #TODO: raise error if units is not cms or hands

        size_in_cms = random.choice([s for s in range(101, 182)])
        if self.UNITS == 'hands':
            hands = int(size_in_cms/2.54) + abs(size_in_cms/2.54)
            return hands
        else:
            return size_in_cms


    def horse_dob(self):
        '''get a date of birth for a live horse, assuming horses live up to 40 years but distribution favours
        younger horses'''
        this_year = date.today().year
        years = [y for y in range(this_year, this_year-40, -1)]

        # note that these do not add up to 100 and they are pure guesswork
        p = [0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04,
             0.03,0.03,0.03,0.03,0.02,0.02,0.02,0.02,0.02,0.02,
             0.01,0.01,0.01,0.01,0.01,0.01,0.01, 0.005, 0.005, 0.005,
             0.001, 0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001]

        # get a year - distributed around average horse age
        year = choice_distribution(years, p)

        # get a month - in northern hemisphere most horses are born in spring
        #TODO: handle date of birth for southern hemisphere
        months = [m for m in range(1, 13)]
        p = [0.2, 0.2, 0.2, 0.2, 0.1, 0.5, 0.2, 0.1, 0.01, 0.01, 0.01, 0.01]
        month = choice_distribution(months, p)

        # get day of birth
        dates = calendar.Calendar().itermonthdates(year, month)

        dob = random.choice([date for date in dates if date.month == month])

        # return in format YYYY-MM-DD
        return str(dob)


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

    def horse_pic(self):
        '''get image url from a list '''

        return random.choice(HORSE_IMAGE_URLS)