# encoding: utf-8

import os
import shutil
import sys
import tempfile
import unittest

from nose_parameterized import parameterized

from pysteam import grid
from pysteam import model
from pysteam import paths
from pysteam import shortcuts

class TestGrid(unittest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    s = model.Steam(self.tempdir)
    self.context = model.LocalUserContext(s, '1234')
    os.makedirs(paths.custom_images_directory(self.context))

  def tearDown(self):
    shutil.rmtree(self.tempdir)

  def _write_file_to_path(self, path, contents):
    with open(path, "w") as f:
      f.write(contents)

  def _read_file(self, path):
    with open(path, "r") as f:
      return f.read()

  def _custom_image_path(self, app_id, extension):
    return os.path.join(
      paths.custom_images_directory(self.context),
      "%s%s" % (app_id, extension)
    )

  def _create_file_with_extension(self, app_id, extension):
    path = self._custom_image_path(app_id, extension)
    self._write_file_to_path(path, 'test')

  @parameterized.expand([
    ('png',   True),
    ('jpg',   True),
    ('jpeg',  True),
    ('tga',   True),
    ('.png',  True),
    ('.jpg',  True),
    ('.jpeg', True),
    ('.tga',  True),
    ('gif',   False),
    ('bmp',   False),
    ('.gif',  False),
    ('.bmp',  False),
  ])
  def test_is_valid_extension(self, extension, expected):
    self.assertEqual(grid.is_valid_extension(extension), expected)

  @parameterized.expand([
    ('.png',  True),
    ('.jpg',  True),
    ('.jpeg', True),
    ('.tga',  True),
    ('.gif',  False),
    ('.bmp',  False),
  ])
  def test_has_custom_image(self, extension, expected):
    """Tests that has_custom_image finds images with the right extension"""
    app_id = '4567'
    self._create_file_with_extension(app_id, extension)
    self.assertEqual(grid.has_custom_image(self.context, app_id), expected)

  def test_get_custom_image_returns_none_for_invalid_extension(self):
    app_id = '4567'
    self._create_file_with_extension(app_id, '.bmp')
    self.assertEqual(grid.get_custom_image(self.context, app_id), None)

  def test_get_custom_image(self):
    app_id = '4567'
    extension = '.png'
    self._create_file_with_extension(app_id, extension)
    expected = self._custom_image_path(app_id, extension)
    self.assertEqual(grid.get_custom_image(self.context, app_id), expected)

  def test_set_custom_image_removes_preexisting_image(self):
    app_id = '4567'
    ext = '.png'

    self._create_file_with_extension(app_id, ext)
    original_path = grid.get_custom_image(self.context, app_id)

    new_image_source = os.path.join(self.tempdir, 'foo.jpeg')
    self._write_file_to_path(new_image_source, 'bar')
    self.assertTrue(grid.set_custom_image(self.context, app_id, new_image_source))

    new_path = grid.get_custom_image(self.context, app_id)
    self.assertFalse(original_path == new_path)
    self.assertFalse(os.path.exists(original_path))

  def test_set_custom_image_writes_image_to_new_location(self):
    app_id = '4567'
    ext = '.png'

    self._create_file_with_extension(app_id, ext)
    old_contents = self._read_file(grid.get_custom_image(self.context, app_id))

    new_image_source = os.path.join(self.tempdir, 'foo.png')
    self._write_file_to_path(new_image_source, 'bar')
    self.assertTrue(grid.set_custom_image(self.context, app_id, new_image_source))

    new_contents = self._read_file(grid.get_custom_image(self.context, app_id))
    self.assertEqual(new_contents, 'bar')
    self.assertFalse(old_contents == new_contents)

  def test_set_custom_image_doesnt_remove_old_image_if_new_path_is_none_or_dne(self):
    app_id = '4567'
    ext = '.png'

    self._create_file_with_extension(app_id, ext)
    original_path = grid.get_custom_image(self.context, app_id)

    self.assertFalse(grid.set_custom_image(self.context, app_id, None))
    self.assertEqual(grid.get_custom_image(self.context, app_id), original_path)

    new_image = os.path.join(self.tempdir, 'dne.png')
    self.assertFalse(grid.set_custom_image(self.context, app_id, new_image))
    self.assertEqual(grid.get_custom_image(self.context, app_id), original_path)

  def test_set_custom_image_doesnt_remove_old_image_or_write_new_one_when_image_has_an_invalid_extension(self):
    app_id = '4567'
    ext = '.png'

    self._create_file_with_extension(app_id, ext)
    original_path = grid.get_custom_image(self.context, app_id)

    new_image_source = os.path.join(self.tempdir, 'foo.bmp')
    self._write_file_to_path(new_image_source, 'bar')
    self.assertFalse(grid.set_custom_image(self.context, app_id, new_image_source))

    self.assertEqual(grid.get_custom_image(self.context, app_id), original_path)
    self.assertFalse(os.path.exists(self._custom_image_path(app_id, '.bmp')))
