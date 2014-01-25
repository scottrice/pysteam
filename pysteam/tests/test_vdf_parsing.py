#!/usr/bin/env python
# encoding: utf-8
"""
test_vdf_parsing.py

Created by Scott on 2013-12-31.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import inspect
import unittest

from pysteam._shortcut_parser import ShortcutParser
from pysteam._shortcut_generator import ShortcutGenerator

class TestVDFParsing(unittest.TestCase):

    @staticmethod
    def create_file_specific_function(path):
        """Returns a function that tests whether we can correctly
        1) Parse a shortcuts file
        2) Generate a shortcuts file"""
        def test_file_equality(self):
            file_contents = open(path,"r").read()
            shortcuts = ShortcutParser().parse(path)
            generated_contents = ShortcutGenerator().to_string(shortcuts)
            self.assertEqual(file_contents.lower(),generated_contents.lower())
        return test_file_equality    
    
    def test_raises_io_error_when_file_doesnt_exist(self):
        invalid_path = os.path.join("this", "path", "doesnt", "exist")
        parser = ShortcutParser()
        with self.assertRaises(IOError):
            parser.parse(invalid_path)

# Taken from a StackOverflow answer, which you can find here:
# http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
vdfs_folder = os.path.join(current_folder,"vdfs")

test_method = None
for file in os.listdir(vdfs_folder):
    if not os.path.isdir(file):
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".vdf":
            test_method = TestVDFParsing.create_file_specific_function(os.path.join(vdfs_folder,file))
            test_method.__name__ = 'test_%s' % filename
            setattr(TestVDFParsing, test_method.__name__, test_method)
test_method = None