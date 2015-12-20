# encoding: utf-8
"""
test_vdf_parsing.py

Created by Scott on 2013-12-31.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import glob
import inspect
import os
import sys
import unittest

from nose_parameterized import parameterized

from pysteam._shortcut_parser import ShortcutParser
from pysteam._shortcut_generator import ShortcutGenerator

current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
vdfs_folder = os.path.join(current_folder,"vdfs")

class TestVDFParsing(unittest.TestCase):

  # We want to run this test for every file in the `vdfs` folder. All this
  # test does is parse the vdf file and regenerate a vdf file with the same
  # data and check that the result is the same as the input
  @parameterized.expand(os.listdir(vdfs_folder))
  def test_vdf_parsing(self, file):
    """Tests that parsing and regenerating a vdf file generates the same contents"""
    path = os.path.join(vdfs_folder, file)
    file_contents = open(path,"r").read()
    shortcuts = ShortcutParser().parse(path)
    generated_contents = ShortcutGenerator().to_string(shortcuts)
    self.assertEqual(file_contents.lower(),generated_contents.lower())

  def test_raises_io_error_when_file_doesnt_exist(self):
    invalid_path = os.path.join("this", "path", "doesnt", "exist")
    parser = ShortcutParser()
    with self.assertRaises(IOError):
      parser.parse(invalid_path)
