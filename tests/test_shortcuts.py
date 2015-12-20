# encoding: utf-8

import sys
import os
import unittest

from nose_parameterized import parameterized

from pysteam import model
from pysteam import shortcuts

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
