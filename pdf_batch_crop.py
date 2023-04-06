#!/usr/bin/python

import sys
import time
import functions

from PyPDF2 import PdfMerger

from config import Config
from pdf import Pdf


if __name__ == '__main__':
    # Get configurations and user settings from either the ini file or from command arguments.
    try:
        config = Config()
    except Exception as ex:
        print(ex)
        sys.exit(1)

    # start timer to determine how long the batch process takes
    start_time = time.time()

    if config.verbose:
        print("-----------------------------------------------")
        print("                 PDF BATCH CROP                ")
        print("-----------------------------------------------")

    pdfs = []

    # Get all PDFs from the input directory, except the processed pdf
    file_list = functions.get_all_pdfs(config.directory, config.output_filename)
    for file in file_list:
        pdf = Pdf(file, config.filter, config.bounding_box, config.rotate)
        pdfs.append(pdf)

    # Get singular PDF file
    if config.input_filename:
        pdf = Pdf(config.input_filename, config.filter, config.bounding_box, config.rotate)
        pdfs.append(pdf)

    if len(pdfs) != 0:
        # create PDF merger that will contain processed the PDFs
        pdf_merger = PdfMerger()

        # Process the pdfs, then merge (if option enabled) and archive.
        merged_pages = 0
        input_pages = 0
        for pdf in pdfs:
            new_pdf_file = pdf.processed_file(config.suffix)
            input_pages += pdf.pages

            if config.verbose:
                print(f"Converting: {pdf.filename}")

            if config.merge:
                pdf.merge(pdf_merger, new_pdf_file)
                merged_pages += pdf.new_pages

            if config.archive:
                archived_file = pdf.archive(config.archived_directory, config.directory, config.archive_by_month)
                if config.verbose:
                    print(f"Archived To: {archived_file}")

            if config.verbose:
                print(f"Processed: Input has {pdf.pages} page{functions.plural(pdf.pages)}, "
                      f"output has {pdf.new_pages} page{functions.plural(pdf.new_pages)}.\n")

        # Write the pdf merger to a new PDF file.
        if config.merge:
            merge_filepath = config.directory + config.output_filename
            pdf_merger.write(open(merge_filepath, "wb"))
            if config.verbose:
                print(f"Merged: {len(pdfs)} PDF file{functions.plural(len(pdfs))} to a {merged_pages} "
                      f"page PDF in {merge_filepath}")

        print(f"Success! {len(pdfs)} PDF file{functions.plural(len(pdfs))} (totalling {input_pages} "
              f"page{functions.plural(input_pages)}) in {round(time.time() - start_time,2)} seconds.")
    else:
        print("There are no PDFs to process.")
