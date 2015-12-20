# encoding: utf-8
"""
This file contains an assortment of functions which deal with how Steam lays
out its directory hierarchy / where it places important files.
"""

import os

# =============================================================================
# Userdata paths
#
# These functions return the default userdata locations for OS X and Linux. On
# these two platforms the userdata directory doesn't change, so these functions
# are all you need to create a valid Steam instance. On Windows the userdata
# directory is stored in the installation directory, which could be anywhere.
# See the `winutils` module's `find_userdata_directory` function if you would
# like the path to the userdata directory on Windows.
#
# See also the `get_steam()` function, which will return a valid Steam
# instance for the current platform.

def default_osx_userdata_path():
  return os.path.join(
    os.path.expanduser("~"),
    "Library",
    "Application Support",
    "Steam",
    "userdata"
  )

def default_linux_userdata_path():
  return os.path.join(
    os.path.expanduser("~"),
    ".local",
    "share",
    "Steam",
    "userdata"
  )

# =============================================================================
# User-specific paths
#
# These functions all take a `user_context` parameter (an instance of the 
# LocalUserContext class) and return various paths that are specific to that
# user. For example, this could be the location of that user's shortcuts.vdf
# file, or their `grid` directory (where custom images are stored)

def user_specific_data_directory(user_context):
  return  os.path.join(
    user_context.steam.userdata_directory,
    user_context.user_id
  )

def custom_images_directory(user_context):
  return os.path.join(
    user_specific_data_directory(user_context),
    "config",
    "grid"
  )

def shortcuts_path(user_context):
  return os.path.join(
    user_specific_data_directory(user_context),
    "config",
    "shortcuts.vdf"
  )
