#!/usr/bin/env python
# encoding: utf-8
"""
game.py

Created by Scott on 2013-12-28.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import shutil

class Game(object):

    @staticmethod
    def valid_custom_image_extensions():
        return ['.png', '.jpg', '.jpeg', '.tga']

    def __init__(self, appid):
        self._appid = appid

    def __eq__(self, other):
        """
        Steam considers two games equal if they have the same App ID
        """
        return (
            isinstance(other,self.__class__) and
            self.appid() == other.appid()
        )

    def __hash__(self):
        return "__GAME{0}__".format(self.appid()).__hash__()

    def _custom_image_path(self, user, extension):
        filename = '%s%s' % (self.appid(), extension)
        return os.path.join(user.grid_directory(), filename)

    def appid(self):
        return str(self._appid)

    def custom_image(self, user):
        """Returns the path to the custom image set for this game, or None if
        no image is set"""
        for ext in self.valid_custom_image_extensions():
            image_location = self._custom_image_path(user, ext)
            if os.path.isfile(image_location):
                return image_location
        return None

    def set_image(self, user, image_path):
        """Sets a custom image for the game. `image_path` should refer to
        an image file on disk"""
        _, ext = os.path.splitext(image_path)
        shutil.copy(image_path, self._custom_image_path(user, ext))
