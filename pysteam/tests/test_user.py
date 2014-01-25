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
    
    
    def setUp(self):
        self.temp_directory = tempfile.mkdtemp()
        self.userdata_directory = os.path.join(self.temp_directory, "userdata")
        os.mkdir(self.userdata_directory)
        self.steam = steam.Steam()
    
    def tearDown(self):
        shutil.rmtree(self.temp_directory)

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

    @mock.patch("pysteam.steam.Steam.userdata_location")
    def test_local_users(self, mocked_userdata_location):
        mocked_userdata_location.return_value = self.userdata_directory

        test_user_ids = [40586375, 49642724]
        for user_id in test_user_ids:
            os.mkdir(os.path.join(self.userdata_directory, str(user_id)))
        
        self.assertEqual(user.User.local_users(self.steam), test_user_ids)