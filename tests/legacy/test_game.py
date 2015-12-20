# encoding: utf-8
"""
test_game.py

Created by Scott on 2013-12-29.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import mock
import tempfile
import shutil
import unittest

from pysteam.legacy import game
from pysteam.legacy import steam
from pysteam.legacy import user

class TestGame(unittest.TestCase):
    
    def setUp(self):
        self.temp_directory = tempfile.mkdtemp()
        self.userdata_directory = os.path.join(self.temp_directory, "userdata")
        os.mkdir(self.userdata_directory)
        self.userdata_patcher = mock.patch("pysteam.legacy.steam.Steam.userdata_location")
        self.userdata_patcher.start()
        steam.Steam.userdata_location.return_value = self.userdata_directory
        self.steam = steam.Steam()
        self.user = user.User(self.steam, 40586375)
        self.game_id = 1234
        self.game = game.Game(self.game_id)
        # Make necessary directories
        os.makedirs(self.user.grid_directory())

    def tearDown(self):
        self.userdata_patcher.stop()
        shutil.rmtree(self.temp_directory)
        
    def write_file_with_contents(self, path, contents):
        f = open(path, "w")
        f.write(contents)
        f.close()

    def test_image_returns_path_if_file_exists(self):
        self.assertIsNone(self.game.custom_image(self.user))

        grid_image_path = self.game._custom_image_path(self.user, '.png')
        self.write_file_with_contents(grid_image_path, 'test')
        self.assertEqual(self.game.custom_image(self.user), grid_image_path)
    
    def test_image_returns_none_if_file_exists_with_invalid_extension(self):
        self.assertEqual(self.steam.userdata_location(), self.userdata_directory)
        self.assertIsNone(self.game.custom_image(self.user))

        grid_image_path = self.game._custom_image_path(self.user, '.gif') #Invalid extension
        self.write_file_with_contents(grid_image_path, 'test')
        self.assertIsNone(self.game.custom_image(self.user))

    def test_set_image_overwrites_existing_image(self):
        # Setup needed files
        old_contents = "old image contents"
        new_contents = "new image contents"
        grid_image_path = self.game._custom_image_path(self.user, '.jpg')
        self.write_file_with_contents(grid_image_path, old_contents)
        new_image_path = os.path.join(self.temp_directory, 'temp_image.png')
        self.write_file_with_contents(new_image_path, new_contents)

        # Verify that the games image contains the old contents
        before = open(self.game.custom_image(self.user))
        self.assertEqual(before.read(), old_contents)
        before.close()

        # Should overwrite the old image
        self.game.set_image(self.user, new_image_path)

        after = open(self.game.custom_image(self.user))
        self.assertEqual(after.read(), new_contents)
        after.close()
