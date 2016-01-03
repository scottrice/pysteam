# encoding: utf-8

import os
import shutil
import sys
import tempfile
import unittest

from nose_parameterized import parameterized

from pysteam import model
from pysteam import paths
from pysteam import shortcuts

def _dummy_shortcut():
  return model.Shortcut("Banjo Kazooie", "Banjo Kazooie.exe", "", "", [])

class TestShortcut(unittest.TestCase):

  # These values are taken from personal testing
  @parameterized.expand([
    ("A", "A", "12204787687793623040"),
    ("B", "B", "11188102301002760192"),
    ("A", "B", "9389247101243752448"),
    ("A", "m", "10399222838585196544"),
    ("A", "n", "13509714557521625088"),
    ("A", "o", "11702344769781891072"),
    ("A", "k", "14270730282167435264"),
  ])
  def test_appid_generation(self, name, exe, expected):
    """Tests that pysteam generates the correct appid hash for shortcuts."""
    s = model.Shortcut(name, exe, "", "", None)
    self.assertEqual(shortcuts.shortcut_app_id(s), expected)

  def test_write_shortcuts_creates_file_if_it_doesnt_exist(self):
    d = tempfile.mkdtemp()
    path = os.path.join(d, "shortcuts.vdf")

    updated_shortcuts = [_dummy_shortcut()]
    self.assertFalse(os.path.exists(path))
    shortcuts.write_shortcuts(path, updated_shortcuts)
    self.assertTrue(os.path.exists(path))
    self.assertEqual(shortcuts.read_shortcuts(path), updated_shortcuts)

    os.remove(path)
    os.rmdir(d)

  def test_get_and_set_shortcuts_creates_file_at_correct_path(self):
    tempdir = tempfile.mkdtemp()

    steam = model.Steam(tempdir)
    context = model.LocalUserContext(steam=steam, user_id='anonymous')
    # Create the `anonymous` directory, cause we can't open shortcuts.vdf for
    # writing if the containing directory doesn't exist
    os.makedirs(paths.user_config_directory(context))

    self.assertFalse(os.path.exists(paths.shortcuts_path(context)))
    self.assertEqual([], shortcuts.get_shortcuts(context))

    updated_shortcuts = [_dummy_shortcut()]
    shortcuts.set_shortcuts(context, updated_shortcuts)
    self.assertEqual(updated_shortcuts, shortcuts.get_shortcuts(context))

    shutil.rmtree(tempdir)
