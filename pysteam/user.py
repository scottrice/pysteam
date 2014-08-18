#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by Scott on 2013-12-28.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

from _shortcut_parser import ShortcutParser
from _shortcut_generator import ShortcutGenerator

# Information about SteamIDs and conversion between them found here:
# https://developer.valvesoftware.com/wiki/SteamID
#
# In short:
# CommunityID32 = Z*2 + Y
# CommunityID64 = Z*2 + V + Y
# Therefore: CommunityID64 = CommunityID32 + V
# Where V is the Steam64 Identifier for the account type (0x0110000100000000
# for individuals, 0x0170000000000000 for groups)
individual_account_type_identifier = 0x0110000100000000

def _community_id_is_64(communityid):
    return communityid > individual_account_type_identifier

def _community_id_32_from_64(communityid64):
    return communityid64 - individual_account_type_identifier

def _community_id_64_from_32(communityid32):
    return communityid32 + individual_account_type_identifier

class User(object):

    def __init__(self, steam, userid):
        self.steam = steam

        if _community_id_is_64(userid):
            self.id32 = _community_id_32_from_64(userid)
            self.id64 = userid
        else:
            self.id32 = userid
            self.id64 = _community_id_64_from_32(userid)

        self.shortcuts = self._load_shortcuts()

    def __eq__(self, other):
        return (
            isinstance(other,self.__class__) and
            self.id32 == other.id32
        )

    def _user_config_directory(self):
        return os.path.join(
            self.userdata_directory(),
            "config"
        )

    def _load_shortcuts(self):
        try:
            parsed_shortcuts = ShortcutParser().parse(self.shortcuts_file())
        except IOError:
            parsed_shortcuts = []
        if parsed_shortcuts == None:
            # TODO: Raise a decent error
            print "Parsing error on file: %s" % file
            parsed_shortcuts = []
        return parsed_shortcuts

    def userdata_directory(self,):
        return os.path.join(
            self.steam.userdata_location(),
            str(self.id32)
        )

    def shortcuts_file(self):
        """Returns a path to this users shortcuts.vdf file"""
        return os.path.join(self._user_config_directory(), "shortcuts.vdf")
    
    def grid_directory(self):
        """Returns a path to this users grid image directory, where custom
        grid images are stored"""
        return os.path.join(self._user_config_directory(), "grid")

    def save_shortcuts(self, path=None, makedirs=True):
        if path is None:
          path = self.shortcuts_file()
        parent_directory = os.path.dirname(path)
        if not os.path.isdir(parent_directory) and makedirs:
          try:
            os.makedirs(parent_directory)
          except OSError:
            raise OSError("Cannot write to directory `%s`." % parent_directory)
        # Write shortcuts to file
        try:
          contents = ShortcutGenerator().to_string(self.shortcuts)
          with open(path, "w") as f:
            f.write(contents)
        except IOError:
          raise IOError("Cannot save file to `%s`. Permission Denied")