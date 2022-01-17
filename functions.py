#!/usr/bin/python

import glob
import os


def plural(number_input):
    """
    Return an s if number is great than 1 or equal to 0.
    :param number_input: A number
    :return: An 's' if 0 or greater than 1, and '' if 1.
    """
    if number_input > 1 or number_input == 0:
        return "s"
    else:
        return ""


def get_all_pdfs(directory, output_filename):
    """
    Get a list of valid pdf filenames in a directory. The processed output filename will not be included.
    :param directory: An absolute directory path
    :param output_filename: The output filename of the processed pdf.
    :return: A list of valid pdf filenames in a directory.
    """
    file_list = []

    for filename in glob.glob(os.path.join(directory, '*.pdf')):
        if filename != directory + output_filename:
            file_list.append(filename)

    return file_list


