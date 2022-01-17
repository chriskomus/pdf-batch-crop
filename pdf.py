#!/usr/bin/python
from PyPDF2 import PdfFileWriter, PdfFileReader
import re
import datetime
import os
import shutil
from pathlib import Path


class Pdf:
    """This class represents a PDF file."""
    def __init__(self, filename, filter_text, bounding_box, rotate):
        self.file = filename
        self.filename = filename
        self.filter_text = filter_text
        self.bounding_box = bounding_box
        self.rotate = rotate

        self.pages = 0
        self.new_pages = 0

    def __str__(self):
        return self.filename

    @property
    def file(self):
        """
        Gets the pdf file object
        :return: The pdf file object
        """
        return self._filename

    @file.setter
    def file(self, new_filename):
        """
        Sets the filename of the pdf and creates a pdf object
        :param new_filename: The filename of the pdf
        """
        if new_filename:
            try:
                self._filename = PdfFileReader(open(new_filename, "rb"))
            except OSError:
                raise ValueError(f"Cannot find file: {self.file}")
        else:
            raise ValueError("PDF filename cannot be blank.")

    def processed_file(self, file_suffix):
        """
        The pdf file is cropped, rotated, and text filtered. A new file is created.
        :param file_suffix: The suffix added to the end of the new file.
        :return: A string of the new filename.
        """
        processed_file = PdfFileWriter()
        self.pages = self.file.getNumPages()

        for i in range(self.pages):
            page = self.file.getPage(i)

            # Skip page if filtered text appears in that page.
            if self.filter_text:
                text_result = page.extractText()
                if re.search(self.filter_text, text_result):
                    continue

            # trim the PDF
            page.trimBox.lowerLeft = (self.bounding_box[0], self.bounding_box[2])
            page.trimBox.upperRight = (self.bounding_box[1], self.bounding_box[3])
            page.cropBox.lowerLeft = (self.bounding_box[0], self.bounding_box[2])
            page.cropBox.upperRight = (self.bounding_box[1], self.bounding_box[3])

            # If Portrait, rotate to Landscape
            if self.rotate:
                if page.mediaBox.getUpperRight_x() - page.mediaBox.getUpperLeft_x() > \
                        page.mediaBox.getUpperRight_y() - page.mediaBox.getLowerRight_y():
                    page.rotateCounterClockwise(90)

            processed_file.addPage(page)

        # Create new file
        new_filename = self.filename.replace(".pdf", "-" + file_suffix + ".pdf")
        output_stream = open(new_filename, "wb")

        processed_file.write(output_stream)
        self.new_pages = processed_file.getNumPages()
        output_stream.close()

        return new_filename

    def archive(self, archived_directory, input_directory, archive_by_month):
        """
        put the PDF in a subdirectory with the option of a further subdirectory broken down by month (ie: 2022-08).
        :param archived_directory: The name of the archive directory
        :param input_directory: The input directory where the processed pdf files are located.
        :param archive_by_month: Is it archived by month?
        :return: a string of the archived filename's absolute path
        """
        if not archived_directory.endswith('/'):
            archived_directory += '/'

        if archive_by_month:
            now = datetime.datetime.now()
            now_append = f'{now.year}-{now.month:02d}/'
            archived_directory += now_append

        # Make sure the archive folder ends with a / but does not begin with a /
        if archived_directory.startswith('/'):
            archived_directory = archived_directory[1:]
        if not input_directory.endswith('/'):
            input_directory += '/'

        pdf_archived_path = input_directory + archived_directory

        # Create the directory if it doesn't exist
        if not os.path.exists(pdf_archived_path):
            Path(pdf_archived_path).mkdir(parents=True, exist_ok=True)

        # Move the pdf to the new directory
        pdf_archived_path_file = self.filename.replace(input_directory,input_directory + archived_directory)
        shutil.move(self.filename, pdf_archived_path_file)

        return pdf_archived_path_file

    @staticmethod
    def merge(merged_pdf, input_filename):
        merged_pdf.append(open(input_filename, "rb"))

        # delete the temporary individual file.
        os.remove(input_filename)
