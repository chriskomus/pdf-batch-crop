#!/usr/bin/python

import argparse
import configparser
import os
from pathlib import Path
import re


class Config:
    """This class contains the config data used by the program. If command line arguments are entered,
    they are tested first and will be used if valid. If no command line argument is entered for a
    parameter, the config.ini value will be used instead.

    If an invalid command line argument is given, an error will be raised even if there is valid data in config.ini"""

    # An overly cautious and restrictive filename cleaner that is valid for Windows filenames.
    CLEAN_FILENAME_REGEX = r'[\\/:"*?<>|]+'

    # Command Line arguments
    ARGUMENTS = [["i", "input_filename", "Filename of single input PDF"],
                        ["o", "output_filename", "Filename of merged output PDF"],
                        ["f", "filter", "Do not crop pages containing this text"],
                        ["s", "suffix", "Cropped PDF filename suffix"],
                        ["d", "directory", "Directory to batch crop"],
                        ["x", "archived_directory", "Relative subdirectory for archive"]]

    ARGUMENTS_BOOL = [["v", "verbose", "Verbose Mode"],
                      ["m", "merge", "Create merged file of all cropped PDFs"],
                      ["r", "rotate", "Rotate all Portrait to Landscape"],
                      ["c", "archive_by_month", "Put archived PDFs in sub folders archived by month"],
                      ["a", "archive", "Move processed PDFs into a sub-directory"]]

    def __init__(self):
        self.input_filename = ""
        self.output_filename = ""
        self.filter = ""
        self.suffix = ""
        self.directory = ""
        self.archived_directory = ""
        self.bounding_box = []
        self.args = self.parser_arguments(self.ARGUMENTS,
                                          self.ARGUMENTS_BOOL,
                                          'PDF Batch Crop',
                                          '"%(prog)s" leave args blank to use config.ini instead.')

        self.verbose = False
        self.merge = False
        self.rotate = False
        self.archive_by_month = False
        self.archive = False

        # Create a self dictionary of config.ini data
        config = configparser.ConfigParser()
        found = config.read('config.ini')
        sections = 'DEFAULTS', 'COORDINATES', 'TOGGLES'

        if not found:
            raise ValueError('Config.ini file is missing.')

        for name in sections:
            self.__dict__.update(config.items(name))

        # Use command line argument if provided, otherwise use config.ini
        for argument_name in self.ARGUMENTS + self.ARGUMENTS_BOOL:
            self.set_argument(argument_name[1])

        self.set_argument('bounding_box', argument_list=[self.__dict__.get('lower_left_x'),
                                                         self.__dict__.get('upper_right_x'),
                                                         self.__dict__.get('lower_left_y'),
                                                         self.__dict__.get('upper_right_y')])

    def __str__(self):
        state = ["%s=%r" % (attribute, value)
                 for (attribute, value)
                 in self.__dict__.items()]
        return '\n'.join(state)

    def set_argument(self, argument_key, argument_list=None):
        """Sets the config arguments. Uses command line arguments if provided, otherwise uses config.ini values.
        True and False strings are set to booleans for Toggles in the config.ini files.
        :param argument_key: The config key name must match in both self.__dict__ and self.args
        :param argument_list: (Optional) A list of values instead of a single value matching the argument_key
        """
        true_strings = ['true', 'yes', 'on', '1']
        false_strings = ['false', 'no', 'off', '0']
        if vars(self.args).get(argument_key):
            argument_value = vars(self.args).get(argument_key)
        else:
            if argument_list:
                argument_value = argument_list
            else:
                argument_value = self.__dict__.get(argument_key)
                if argument_value.lower() in true_strings:
                    argument_value = True
                elif argument_value.lower() in false_strings:
                    argument_value = False

        setattr(self, argument_key, argument_value)

    @property
    def directory(self):
        """
        Gets the directory of pdfs that will be processed
        :return: The directory of pdfs that will be processed
        """
        return self._directory

    @directory.setter
    def directory(self, new_directory):
        """
        Sets the directory of pdfs that will be processed
        :param new_directory: The directory of pdfs that will be processed
        """
        p = Path(new_directory)
        if p.exists() and p.is_dir():
            if not new_directory.endswith('/'):
                new_directory += '/'
                self._directory = new_directory
        else:
            raise ValueError("Invalid input directory or directory doesn't exist.")

    @property
    def input_filename(self):
        """
        Gets the filename of a single pdf that will be processed
        :return: The filename of a single pdf that will be processed
        """
        return self._input_filename

    @input_filename.setter
    def input_filename(self, new_filename):
        """
        Sets the filename of a single pdf that will be processed.
        :param new_filename: The filename of a single pdf that will be processed
        """
        if not new_filename == "":
            full_filename_and_path = os.path.abspath(new_filename)
            if os.path.exists(full_filename_and_path):
                self._input_filename = full_filename_and_path
            else:
                raise ValueError("Input filename doesn't exist.")
        else:
            self._input_filename = ""

    @property
    def suffix(self):
        """
        Gets the filename suffix that will be added to processed files.
        :return: The filename suffix that will be added to processed files.
        """
        return self._suffix

    @suffix.setter
    def suffix(self, new_suffix):
        """
        Sets the filename suffix that will be added to processed files.
        :param new_suffix: The filename suffix that will be added to processed files.
        """
        self._suffix = re.sub(self.CLEAN_FILENAME_REGEX, '', new_suffix)

    @property
    def filter(self):
        """
        Gets the text that will be used to filter out pdfs from being process
        :return: The text that will be used to filter out pdfs from being process
        """
        return self._filter

    @filter.setter
    def filter(self, new_filter_text):
        """
        Sets the text that will be used to filter out pdfs from being processed.
        If this text appears in the pdf, it will not be added to the process.
        :param new_filter_text: The text that will be used to filter out pdfs from being processed.
        """
        self._filter = new_filter_text

    @property
    def output_filename(self):
        """
        Gets the output filename of the cropped and merged pdf
        :return: The output filename of the cropped and merged pdf
        """
        return self._output_filename

    @output_filename.setter
    def output_filename(self, new_output_filename):
        """
        Sets the output filename of the cropped and merged pdf
        :param new_output_filename: : The output filename of the cropped and merged pdf
        """
        self._output_filename = re.sub(self.CLEAN_FILENAME_REGEX, '', new_output_filename)

    @property
    def archived_directory(self):
        """
        Gets the archived directory used for storing cropped pdfs.
        :return: The archived directory used for storing cropped pdfs.
        """
        return self._archived_directory

    @archived_directory.setter
    def archived_directory(self, new_archived_directory_name):
        """
        Sets the archived directory used for storing cropped pdfs.
        :param new_archived_directory_name: The relative path of the archive directory.
        """
        directory = re.sub(self.CLEAN_FILENAME_REGEX, '', new_archived_directory_name)
        if not directory.endswith('/'):
            directory += '/'
            self._archived_directory = directory

    @property
    def bounding_box(self):
        """
        Gets the bounding box used for cropping a pdf.
        :return: The bounding box used for cropping a pdf.
        """
        return self._bounding_box

    @bounding_box.setter
    def bounding_box(self, new_bounding_box_list):
        """
        Sets the bounding box used for cropping a pdf.
        :param new_bounding_box_list: A list of 4 float numbers. Anything other than 4 floats will raise an exception.
        """
        bounding_box = []
        for position in new_bounding_box_list:
            if len(new_bounding_box_list) == 4:
                try:
                    bounding_box.append(float(position))
                except ValueError:
                    raise ValueError("Invalid bounding box value(s). Must be 4 numeric values.")
            else:
                raise ValueError("Invalid amount of bounding box values. Must be 4 numeric values.")

        bounding_box = new_bounding_box_list
        self._bounding_box = [float(i) for i in bounding_box]

    def parser_arguments(self, arguments_str, arguments_bool, prog, description):
        """
        Create an Argument Parser from command line inputs supplied by a list of configuration strings and boolean toggles.
        :param arguments_str: A list of settings for argument strings.
        The format of each list in the list is as follows: [char, key, description]
        :param arguments_bool: A list of settings for argument booleans.
        The format of each list in the list is as follows: [char, key, description]
        :param prog: Name of the program
        :param description: Description of the program
        :return: A parser.parse_args
        """
        parser = argparse.ArgumentParser(
            prog=prog,
            description=description
        )

        for i in arguments_str:
            parser.add_argument('-' + i[0],
                                '--' + i[1],
                                type=str,
                                help=i[2])

        for i in arguments_bool:
            parser.add_argument('-' + i[0],
                                '--' + i[1],
                                action="store_true",
                                help=i[2])

        parser.add_argument('-b', '--bounding_box', type=float, nargs='*', help='Bounding box [y0 y1 x0 x1]')

        return parser.parse_args()
