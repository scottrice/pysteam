# encoding: utf-8
"""
test_shortcut.py

Created by Scott on 2013-12-29.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import unittest

from pysteam.legacy import shortcut

class TestShortcut(unittest.TestCase):

    def test_appid(self):
        """Tests that pysteam generates the correct appid hash for shortcuts.
        These values are taken from personal testing"""
        self.assertEqual(shortcut.Shortcut("A","A","").appid(), "12204787687793623040")
        self.assertEqual(shortcut.Shortcut("B","B","").appid(), "11188102301002760192")
        self.assertEqual(shortcut.Shortcut("A","B","").appid(), "9389247101243752448")
        self.assertEqual(shortcut.Shortcut("A","m","").appid(), "10399222838585196544")
        self.assertEqual(shortcut.Shortcut("A","n","").appid(), "13509714557521625088")
        self.assertEqual(shortcut.Shortcut("A","o","").appid(), "11702344769781891072")
        self.assertEqual(shortcut.Shortcut("A","k","").appid(), "14270730282167435264")
