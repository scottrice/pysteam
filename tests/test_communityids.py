# encoding: utf-8

import sys
import os
import unittest

from nose_parameterized import parameterized

from pysteam import communityids

KNOWN_ID_PAIRS = [
  # Meris608
  (40586375, 76561198000852103),
  # Jankenking
  (49642724, 76561198009908452),
]

class TestCommunityIds(unittest.TestCase):

  @parameterized.expand(KNOWN_ID_PAIRS)
  def test_id64_from_id32(self, id32, id64):
    """Tests converting an id32 into an id64"""
    self.assertEqual(communityids.id64_from_id32(id32), id64)

  @parameterized.expand(KNOWN_ID_PAIRS)
  def test_id32_from_id64(self, id32, id64):
    """Tests converting an id64 into an id32"""
    self.assertEqual(communityids.id32_from_id64(id64), id32)
