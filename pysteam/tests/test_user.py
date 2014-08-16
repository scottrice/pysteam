#!/usr/bin/env python
# encoding: utf-8
"""
test_user.py

Created by Scott on 2013-12-29.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import mock
import shutil
import tempfile
import unittest

from pysteam import steam
from pysteam import user

class TestUser(unittest.TestCase):
    
    meris608_32 = 40586375
    meris608_64 = 76561198000852103
    jankenking_32 = 49642724
    jankenking_64 = 76561198009908452

    def test_community_id_is_64(self):
        self.assertFalse(user._community_id_is_64(self.meris608_32))
        self.assertTrue(user._community_id_is_64(self.meris608_64))
        self.assertFalse(user._community_id_is_64(self.jankenking_32))
        self.assertTrue(user._community_id_is_64(self.jankenking_64))

    def test_community_id_32_from_64(self):
        self.assertEqual(user._community_id_32_from_64(self.meris608_64), self.meris608_32)
        self.assertEqual(user._community_id_32_from_64(self.jankenking_64), self.jankenking_32)

    def test_community_id_64_from_32(self):
        self.assertEqual(user._community_id_64_from_32(self.meris608_32), self.meris608_64)
        self.assertEqual(user._community_id_64_from_32(self.jankenking_32), self.jankenking_64)