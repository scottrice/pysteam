#!/usr/bin/env python
# encoding: utf-8
"""
steam.py

Created by Scott on 2013-12-28.
Copyright (c) 2013 Scott Rice. All rights reserved.

Represents the local steam installation.
"""

import sys
import os

def _is_mac():
    return sys.platform == 'darwin'

def _is_windows():
    return sys.platform != 'darwin' and 'win' in sys.platform
    
def _is_linux():
    return sys.platform.startswith('linux')

def _windows_steam_location():
    if not _is_windows():
        return
    import _winreg as registry
    key = registry.CreateKey(registry.HKEY_CURRENT_USER,"Software\Valve\Steam")
    return registry.QueryValueEx(key,"SteamPath")[0]

class Steam(object):
    
    def __init__(self, steam_location=None):
        # If no steam_location was provided but we are on Windows, then we can
        # find Steam's location by looking in the registry
        if not steam_location and _is_windows():
            steam_location = _windows_steam_location()
        self.steam_location = steam_location

    def userdata_location(self):
        if _is_windows():
            return os.path.join(self.steam_location, "userdata")
        elif _is_mac():
            return os.path.join(os.path.expanduser("~"),
                                "Library",
                                "Application Support",
                                "Steam",
                                "userdata"
            )
        elif _is_linux():
            return os.path.join(os.path.expanduser("~"),
                                ".local",
                                "share",
                                "Steam",
                                "userdata"
            )
        else:
            raise EnvironmentError("Running on unsupported environment %s" % sys.platform)
