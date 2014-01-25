#!/usr/bin/env python
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

from pysteam import steam

class TestSteam(unittest.TestCase):

    @mock.patch("pysteam.steam._windows_steam_location")
    @mock.patch("pysteam.steam._is_linux")
    @mock.patch("pysteam.steam._is_mac")
    @mock.patch("pysteam.steam._is_windows")
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

    @mock.patch("pysteam.steam._is_linux")
    @mock.patch("pysteam.steam._is_mac")
    @mock.patch("pysteam.steam._is_windows")
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

    @mock.patch("pysteam.steam._is_linux")
    @mock.patch("pysteam.steam._is_mac")
    @mock.patch("pysteam.steam._is_windows")
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