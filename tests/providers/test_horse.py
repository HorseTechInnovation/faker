# coding=utf-8

from __future__ import unicode_literals

import re
import unittest

from faker import Faker
from faker.providers.horse.en_US import Provider as USProvider
# from faker.providers.person.fi_FI import Provider as FiProvider
# from faker.providers.person.ne_NP import Provider as NeProvider
# from faker.providers.person.sv_SE import Provider as SvSEProvider
# from faker.providers.person.pl_PL import (
#     checksum_identity_card_number as pl_checksum_identity_card_number,
# )
from tests import string_types


class TestUS(unittest.TestCase):
    """ Tests horse in the US locale """

    def setUp(self):
        self.factory = Faker('en_US')

    def test_simple(self):

        first = self.factory.simple_horse()

        # General first name
        color = self.factory.horse_color()
        # self.assertTrue(name)
        # self.assertIsInstance(name, string_types)
        # self.assertIn(name, USProvider.first_names)

        ueln = self.factory.ueln()

        self.assertTrue(int(ueln[0:3]) > 0)

        # # Females first name
        # name = self.factory.first_name_female()
        # self.assertTrue(name)
        # self.assertIsInstance(name, string_types)
        # self.assertIn(name, USProvider.first_names)
        # self.assertIn(name, USProvider.first_names_female)
        #
        # # Male first name
        # name = self.factory.first_name_male()
        # self.assertTrue(name)
        # self.assertIsInstance(name, string_types)
        # self.assertIn(name, USProvider.first_names)
        # self.assertIn(name, USProvider.first_names_male)