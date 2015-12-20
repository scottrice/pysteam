# encoding: utf-8
"""
test_steam.py

Created by Scott on 2013-12-29.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import unittest
import mock
import tempfile
import shutil

from pysteam.legacy import steam

class TestSteam(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.mkdtemp()
        self.userdata_directory = os.path.join(self.temp_directory, "userdata")
        os.mkdir(self.userdata_directory)

    def tearDown(self):
        shutil.rmtree(self.temp_directory)

    @mock.patch("pysteam.legacy.steam._windows_steam_location")
    @mock.patch("pysteam.legacy.steam._is_linux")
    @mock.patch("pysteam.legacy.steam._is_mac")
    @mock.patch("pysteam.legacy.steam._is_windows")
    def test_userdata_location_windows(self, mock_is_windows, mock_is_mac, mock_is_linux, mock_windows_steam_location):
        mock_is_windows.return_value = True
        mock_is_mac.return_value = False
        mock_is_linux.return_value = False

        custom_temp_dir = tempfile.mkdtemp()
        custom_steam = steam.Steam(steam_location=custom_temp_dir)
        custom_steam_userdata = custom_steam.userdata_location()
        self.assertIn(custom_temp_dir, custom_steam_userdata)
        self.assertEquals(os.path.basename(custom_steam_userdata), "userdata")

        reg_temp_dir = tempfile.mkdtemp()
        mock_windows_steam_location.return_value = reg_temp_dir
        reg_steam = steam.Steam()
        reg_steam_userdata = reg_steam.userdata_location()
        self.assertIn(reg_temp_dir, reg_steam_userdata)
        self.assertEquals(os.path.basename(reg_steam_userdata), "userdata")

        shutil.rmtree(custom_temp_dir)
        shutil.rmtree(reg_temp_dir)

    @mock.patch("pysteam.legacy.steam._is_linux")
    @mock.patch("pysteam.legacy.steam._is_mac")
    @mock.patch("pysteam.legacy.steam._is_windows")
    def test_userdata_location_mac(self, mock_is_windows, mock_is_mac, mock_is_linux):
        mock_is_windows.return_value = False
        mock_is_mac.return_value = True
        mock_is_linux.return_value = False

        custom_temp_dir = tempfile.mkdtemp()
        custom_steam = steam.Steam(steam_location=custom_temp_dir)
        custom_steam_userdata = custom_steam.userdata_location()

        normal_steam = steam.Steam()
        normal_steam_userdata = normal_steam.userdata_location()

        # Changing the Steam install location should have no effect on the
        # userdata directory, as it is always in the same place
        self.assertEqual(custom_steam_userdata, normal_steam_userdata)
        # On Mac, userdata is in ~/Library/Application Support/Steam/userdata
        self.assertIn("Library", normal_steam_userdata)
        self.assertIn("Application Support", normal_steam_userdata)

        shutil.rmtree(custom_temp_dir)

    @mock.patch("pysteam.legacy.steam._is_linux")
    @mock.patch("pysteam.legacy.steam._is_mac")
    @mock.patch("pysteam.legacy.steam._is_windows")
    def test_userdata_location_linux(self, mock_is_windows, mock_is_mac, mock_is_linux):
        mock_is_windows.return_value = False
        mock_is_mac.return_value = False
        mock_is_linux.return_value = True

        custom_temp_dir = tempfile.mkdtemp()
        custom_steam = steam.Steam(steam_location=custom_temp_dir)
        custom_steam_userdata = custom_steam.userdata_location()

        normal_steam = steam.Steam()
        normal_steam_userdata = normal_steam.userdata_location()

        # Changing the Steam install location should have no effect on the
        # userdata directory, as it is always in the same place
        self.assertEqual(custom_steam_userdata, normal_steam_userdata)
        # On Linux, userdata is in ~/.local/share/Steam/userdata
        self.assertIn(".local", normal_steam_userdata)
        self.assertIn("share", normal_steam_userdata)

        shutil.rmtree(custom_temp_dir)

    @mock.patch("pysteam.legacy.steam.Steam.userdata_location")
    def test_local_users(self, mocked_userdata_location):
        mocked_userdata_location.return_value = self.userdata_directory
        os.mkdir(os.path.join(self.userdata_directory, "40586375"))
        os.mkdir(os.path.join(self.userdata_directory, "49642724"))

        s = steam.Steam()
        ids = [ u.id32 for u in s.local_users() ]

        self.assertEqual(ids, [40586375, 49642724])

    @mock.patch("pysteam.legacy.steam.Steam.userdata_location")
    def test_local_users_ignores_anonymous_user(self, mocked_userdata_location):
        mocked_userdata_location.return_value = self.userdata_directory
        os.mkdir(os.path.join(self.userdata_directory, "40586375"))
        os.mkdir(os.path.join(self.userdata_directory, "49642724"))
        os.mkdir(os.path.join(self.userdata_directory, "anonymous"))

        s = steam.Steam()
        ids = [ u.id32 for u in s.local_users() ]

        self.assertEqual(ids, [40586375, 49642724])
