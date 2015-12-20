# encoding: utf-8

import os
import shutil
import sys
import tempfile
import unittest

import mock

from nose_parameterized import parameterized

from pysteam import model
from pysteam import steam

class TestSteam(unittest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.tempdir)
    self.tempdir = None

  def _make_folders_in_temp_directory_for_ids(self, uids):
    assert(os.path.exists(self.tempdir))
    paths = map(lambda uid: os.path.join(self.tempdir, uid), uids)
    for path in paths:
      os.mkdir(path)

  def test_get_steam_returns_none_if_directory_doesnt_exist(self):
    with mock.patch('os.path.exists', return_value=False):
      self.assertIsNone(steam.get_steam())

  def test_local_user_ids_returns_empty_list_for_empty_userdata_directory(self):
    s = model.Steam(self.tempdir)
    self.assertEqual(len(steam.local_user_ids(s)), 0)

  def test_local_user_ids_returns_none_if_steam_is_none(self):
    self.assertIsNone(steam.local_user_ids(None))

  def test_local_user_contexts_returns_none_if_steam_is_none(self):
    self.assertIsNone(steam.local_user_contexts(None))

  def test_local_user_ids_returns_list_of_users_with_entries_in_userdata_folder(self):
    self._make_folders_in_temp_directory_for_ids(['1234', '4567'])
    s = model.Steam(self.tempdir)

    uids = steam.local_user_ids(s)
    self.assertEqual(len(uids), 2)
    self.assertIn('1234', uids)
    self.assertIn('4567', uids)

  def test_local_user_ids_returns_anonymous_user(self):
    self._make_folders_in_temp_directory_for_ids(['anonymous'])
    s = model.Steam(self.tempdir)

    uids = steam.local_user_ids(s)
    self.assertEqual(len(uids), 1)
    self.assertEqual(uids[0], 'anonymous')

  def test_local_user_contexts_returns_user_context_with_same_steam(self):
    self._make_folders_in_temp_directory_for_ids(['1234'])
    s = model.Steam(self.tempdir)

    contexts = steam.local_user_contexts(s)
    self.assertEqual(len(contexts), 1)
    self.assertEqual(contexts[0].steam, s)
