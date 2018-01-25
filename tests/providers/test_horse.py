# coding=utf-8

from __future__ import unicode_literals

import re
import unittest

from faker import Faker
from faker.providers.horse.en_US import Provider as USProvider

from tests import string_types
from datetime import date
from dateutil.relativedelta import relativedelta

class TestUS(unittest.TestCase):
    """ Tests horse in the US locale """

    def setUp(self):
        self.factory = Faker('en_US')

    def test_simple(self):

        simple = self.factory.simple_horse()

        self.assertIsInstance(simple['handle'], string_types)
        self.assertIsInstance(simple['name'], string_types)
        self.assertIsInstance(USProvider.SEX[simple['sex']], string_types)
        self.assertIsInstance(simple['color'], string_types)

        # us measures size in hands
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

        country = self.factory.country_of_birth()

        self.assertEqual(country, 372)

    def test_size_in_cms(self):

        size = self.factory.horse_size()

        self.assertTrue(size > 100)
        self.assertTrue(size <  183)