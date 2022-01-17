import unittest
from config import Config
import os


class TestConfig(unittest.TestCase):
    config = Config()

    def test_config_load(self):
        """ Test that config.py loads completely """
        self.assertRaises(Exception, self.config)

    def test_input_filename(self):
        """ Test that input_filename returns the correct value"""
        expected = os.path.abspath("test.pdf")
        actual = self.config.input_filename

        self.assertEqual(expected, actual, 'does not match')

    def test_output_filename(self):
        """ Test that output_filename returns the correct value"""
        expected = "pdf_crop_merge.pdf"
        actual = self.config.output_filename

        self.assertEqual(expected, actual, 'does not match')

    def test_filter(self):
        """ Test that input_filename returns the correct value"""
        expected = "Commercial Invoice"
        actual = self.config.filter

        self.assertEqual(expected, actual, 'does not match')

    def test_suffix(self):
        """ Test that the suffix returns the correct value"""
        expected = "crop"
        actual = self.config.suffix

        self.assertEqual(expected, actual, 'does not match')

    def test_directory(self):
        """ Test that directory returns the correct value"""
        expected = "/home/chris/Desktop/Shipping Labels/"
        actual = self.config.directory

        self.assertEqual(expected, actual, 'does not match')

    def test_archived_directory(self):
        """ Test that archived directory returns the correct value"""
        expected = "Archived"
        actual = self.config.archived_directory

        self.assertEqual(expected, actual, 'does not match')


if __name__ == '__main__':
    unittest.main()
