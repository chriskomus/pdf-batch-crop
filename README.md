# Batch Crop, Merge, and Move PDFs

- Crop single PDFs, or batch crop entire directories
- Merge batched PDFs all into one PDF
- Filter out pages if they contain a user defined string
- Move/Archive original PDFs to a subdirectory after they have been processed
- Subdirectory archive folders can be broken down by YYYY-MM
- Rotate Portrait to Landscape
- Set a filename suffix for cropped PDFs
- Set a filename for merged PDFs
- Set a subdirectory for Archived PDFs
- Use command line arguments or edit the config.ini file to change parameters

## Default Settings for Cropping 8.5" x 11" Shipping Labels to 4" x 6" Thermal Labels.

- I created this specifically for cropping Canada Post 8.5" x 11" shipping labels to 4" x 6" Mailing Thermal Labels, so that is what the default settings are.

## Help

To run using only config.ini settings:

`python3 pdf_batch_crop.py`

To run using command line args for example:

`python3 pdf_batch_crop.py -v -r -d /home/user/directory`

A single input filename can be used or a whole input directory, or both.

There is a config.ini file where settings are stored. Using command line arguments will override the config.ini file. However, if any of the toggles are set to True in the config.ini, they will be true regardless of whether a toggle command line argument is set.

### Arguments:
- -h, --help **(show this help message and exit)**
- -i INPUT_FILENAME **(Input filename of single PDF)**
- -o OUTPUT_FILENAME **(Output filename of merged PDF)**
- -f FILTER **(Do not crop pages containing this text)**
- -s SUFFIX **(Cropped PDF filename suffix)**
- -d DIRECTORY **(Directory to batch crop)**
- -x ARCHIVED_DIRECTORY **(Name of subdirectory for archive (NOTE: this is not an absolute path, just the name of a subdirectory))**
- -b **(Bounding box [y0 y1 x0 x1])**

### Toggles:
- -v, --verbose         **(Verbose Mode)**
- -m, --merge           **(Create merged file of all cropped PDFs)**
- -a, --archive         **(Move processed PDFs into a sub-directory)**
- -r, --rotate          **(Rotate all Portrait to Landscape)**
- -c, --archive_by_month  **(Put archived PDFs in sub folders archived by date)**

## Setting the Bounding Box

Either set the coordinates in the config.ini file, or by command line by using the -b toggle and then exactly 4 numbers separated by a single space:
-b 1 2 3 4

This has to be set using trial and error for now. Read PyPDF2 documentation for more information.

## Requirements

You will need PyPDF2:

`pip install PyPDF2`

PyPDF2 is a pure-python PDF library capable of splitting, merging together, cropping, and transforming the pages of PDF files. It can also add custom data, viewing options, and passwords to PDF files. It can retrieve text and metadata from PDFs as well as merge entire files together.

Homepage  
http://mstamy2.github.io/PyPDF2/
