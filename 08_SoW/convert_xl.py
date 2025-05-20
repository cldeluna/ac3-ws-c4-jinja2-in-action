#!/usr/bin/python -tt
# Project: ac3_templating_workshop
# Filename: convert_xl.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/13/25"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse


from utils import utils


def some_function():
    pass


def main():

    filename = arguments.file
    utils.convert_excel_to_format(
        input_file=filename, output_format="yaml", export_schema=True
    )


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description", epilog="Usage: ' python convert_xl.py' "
    )

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument(
        "-f", "--file", help="Excel file", action="store", default="GDL_NewAPs.xlsx"
    )
    arguments = parser.parse_args()
    main()
