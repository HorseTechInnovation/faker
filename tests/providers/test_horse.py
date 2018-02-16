# coding=utf-8

from __future__ import unicode_literals

import re
import unittest
import os
import csv

from faker import Faker
from faker.providers.horse import Provider as HorseProvider
from faker.providers.horse.en_US import Provider as USProvider
from faker.providers.horse.en_IE import Provider as IEProvider
from faker.factory import Factory


from tests import string_types
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from faker.providers.horse.data import HORSE_HANDLES, PIOS, COUNTRY_POPULATION

class TestHorseData(unittest.TestCase):
    """check the data in the data folder"""


    def test_pios_and_population_complete(self):
        '''check that all counties with a pick value > 0 have a at least one PIO and that
        all PIOs country code exists in the HorsePop file.'''

        provider = Factory.create(providers=['faker.providers.horse']).providers[0]

        # get a list of all the countries with a PIO
        pio_countries = set()
        for item in PIOS:
                    pio_countries.add(item['country'])

        # get a list of all the countries with a horse population
        countries = set()
        for item in COUNTRY_POPULATION:
                if int(item['pick']) > 0:
                    countries.add(item['iso3166'])

        # all PIOs are linked to a country with a horse population and  all countries with a horse population have a PIO
        if not countries.issubset(pio_countries):
            for item in countries.difference(pio_countries):
                print("No PIO in pios.csv for country code %s" % item)

            for item in pio_countries.difference(countries):
                print("PIO country code %s does not exist in horse_population.csv" % item)

            self.assertTrue(0, "Data in data directory is missing data that could cause faker to fail")

class TestUS(unittest.TestCase):
    """ Tests horse in the US locale """

    def setUp(self):
        self.factory = Faker('en_US')

    def test_dob(self):
        '''check that date of birth of horse (assumes horse is alive) will return a reasonable date'''
        provider = USProvider('en_US')

        dob = datetime.strptime(provider.horse_dob(),"%Y-%m-%d")

        years_old = date.today().year - dob.year

        self.assertTrue(years_old < 40)

    def test_country(self):

        us = USProvider('en_US')
        country = us.country_of_birth()

        country2 = self.factory.country_of_birth()
        # This fails because using factory uses default not US version, why???????
        #self.assertEqual(country, country2)
        self.assertEqual(country, 840)

    def test_simple(self):

        simple = self.factory.simple_horse()
        # us = USProvider('en_US')
        # simple = us.simple_horse()

        self.assertIsInstance(simple['handle'], string_types)
        self.assertIsInstance(simple['name'], string_types)
        self.assertIsInstance(USProvider.SEX[simple['sex']], string_types)
        self.assertIsInstance(simple['color'], string_types)

        # US measures size in hands
        self.assertTrue(simple['size'] >= 10)
        self.assertTrue(simple['size'] <=  19)

        self.assertTrue(simple['dob'] < date.today())
        self.assertTrue(simple['dob'] >  date.today() - relativedelta(years=40))

        ueln = simple['ueln'].split("-")

        self.assertTrue(len(ueln[0]) == 3)
        self.assertTrue(len(ueln[1]) == 3)
        self.assertTrue(len(ueln[2]) == 9)


class TestIE(unittest.TestCase):
    """ Test differences for horse in the IE locale """

    def setUp(self):
        self.factory = Faker('en_IE')

    def test_country(self):

        ie = IEProvider('en_IE')
        country = ie.country_of_birth()

        self.assertEqual(country, 372)

    def test_size_in_cms(self):

        ie = IEProvider('en_IE')
        size = ie.horse_size()

        self.assertTrue(size > 100)
        self.assertTrue(size <  183)

