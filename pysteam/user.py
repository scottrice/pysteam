#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by Scott on 2013-12-28.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import steam
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

    @staticmethod
    def local_users(steam):
        """Returns an array of user ids for users on the filesystem"""
        # Any users on the machine will have an entry inside of the userdata
        # folder. As such, the easiest way to find a list of all users on the
        # machine is to just list the folders inside userdata
        ids = []
        userdata_dir = steam.userdata_location()
        for entry in os.listdir(userdata_dir):
            if os.path.isdir(os.path.join(userdata_dir,entry)):
                ids.append(int(entry))
        return ids
    
    def __init__(self, steam, userid):
        self.steam = steam

        if _community_id_is_64(userid):
            self.id32 = _community_id_32_from_64(userid)
            self.id64 = userid
        else:
            self.id32 = userid
            self.id64 = _community_id_64_from_32(userid)

        self.shortcuts = self._load_shortcuts()

    def _user_config_directory(self):
        return os.path.join(
            self.steam.userdata_location(),
            str(self.id32),
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

    def shortcuts_file(self):
        """Returns a path to this users shortcuts.vdf file"""
        return os.path.join(self._user_config_directory(), "shortcuts.vdf")
    
    def grid_directory(self):
        """Returns a path to this users grid image directory, where custom
        grid images are stored"""
        return os.path.join(self._user_config_directory(), "grid")
    
    def save_shortcuts(self):
        # Write shortcuts to file
        contents = ShortcutGenerator().to_string(self.shortcuts)
        f = open(self.shortcuts_file(), "w")
        f.write(contents)
        f.close()
