#!/usr/bin/python -tt
# Training Scaffolding: Monolithic Switch Config Generator

from __future__ import absolute_import, division, print_function

import argparse
import os
import datetime
import pytz

# from utils import utils  # ← Uncomment after you have created your own or
# you have found the functions you need in the utils module in this repository

def main():
    """
    Scaffolding main function for generating monollithic configuration files.
    Workshop Task: implement the logic needed to generate monolithic config files
    """

    # TODO: Get the current time in the specified timezone
    # Why: From this you will create two timestamp strings, one suitable for
    # a filename and one for the template that is human readable
    # Example: now = datetime.datetime.now(pytz.timezone(arguments.timezone))

    # TODO: Format the timestamp string for template injection
    # Why: We want the timestamp to be human-readable in the template
    # Example:  May 22, 2025 at 05:41:53 AM PDT

    # TODO: Format a filename-safe timestamp
    # Why: This is used to timestamp the configuration files itself
    # Example: 20250522-054153

    # TODO: Load CSV data using a helper function (implement yourself or use the one in the utils module)
    # Example: payload_data = utils.load_csv(arguments.payload_file)

    print(f"\nGenerating configurations from {arguments.payload_file}\n")

    # TODO: Convert list of rows to list of dictionaries using a utility function
    # You have read in a CSV file with the first row as the header and then one ore more lines of new switches
    # Its much better to work with a list of dictionaries

    # TODO: Loop through the list of switch configs adding additional key/value pairs to the dictionary
    #
    # for cfg_dict in payload_lod:
    #     - Add human readable timestamp
    #     - Add a temporary enable secret (suitable for staging)
    #     - Determine max interfaces from model
    #     - Convert CIDR to dotted subnet mask
    #     - Ensure output directory exists
    #     - Construct output filename
    #     - Render template
    #     - Save file

    # Print a message with the output location
    print(f"\nSaved configuration files to output directory.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scaffolding: Switch Configuration Generator",
        epilog="Usage: uv run gen_monolithic_sw_cfg_scaffold.py (Default is to use new_switches.csv)"
    )

    parser.add_argument(
        "-p", "--payload_file", help="CSV file with switch data",
        default="new_switches.csv"
    )
    parser.add_argument(
        "-o", "--output_dir", help="Output directory for configs",
        default="cfg_output"
    )
    parser.add_argument(
        "-s", "--secret_temp", help="Temporary enable password",
        default="T3mp@ecreto"
    )
    # Check https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List for timezone values
    parser.add_argument(
        "-t", "--timezone", help="Timezone (e.g., America/Los_Angeles)",
        default="America/Los_Angeles"
    )

    arguments = parser.parse_args()
    main()

