#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: monolithic_sw_cfg
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "10/9/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import os
import datetime
import pytz


from utils import utils



def main():

    # Get the current date and time
    now = datetime.datetime.now(pytz.timezone(arguments.timezone))  # Replace with your timezone

    # Format it as a string
    timestamp = now.strftime("%B %d, %Y at %I:%M:%S %p %Z")

    # Date stamp for Report if one already exists
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Load the data in the CSV file
    payload_data = utils.load_csv(os.path.join(os.getcwd(), arguments.payload_file))
    print(f"\nGenerating configurations for switches in CSV file {arguments.payload_file}\n")

    if payload_data:
        # We have read in a CSV file with the first row as the header and then one ore more lines of new switches
        # Its much better to work with a list of dictionaries
        payload_lod = utils.lists_to_dicts(payload_data)

        # cfg_dict will be passed to the template as "cfg"
        for cfg_dict in payload_lod:

            # Build template payload
            cfg_dict.update({"timestamp": timestamp})

            # Get enable secret
            cfg_dict.update({"enable_sec": arguments.secret_temp})

            # Determine Max user interfaces from model number
            # Is this the best way to do this?  No.
            if "24" in cfg_dict['sw_model']:
                max_intfs = 24
            elif "8" in cfg_dict['sw_model']:
                max_intfs = 8
            else:
                max_intfs = 48

            cfg_dict.update({"max_intfs": max_intfs})

            # Determine mask in dotted notation get_mask_from_cidr(cidr)
            cfg_dict.update({"mgmt_mask": utils.get_mask_from_cidr(cfg_dict['mgmt-subnet_cidr'])})

            # Check to see if the output directory exists and if it does not, create it
            # This is the directory where we will store the resulting config files
            cfg_directory = os.path.join(os.getcwd(),arguments.output_dir)
            utils.check_and_create_directory(cfg_directory)
            # Create the resulting template filename with timestamp. Using txt so its easy to open with default
            # editors
            filename = f"{cfg_dict['hostname']}_{file_timestamp}.txt"

            # Create output directory and set the full path
            fullpath = utils.create_output_dir_fp(os.getcwd(), arguments.output_dir, filename)

            rendered = utils.render_in_one("dnac_baseconfig_sample_template.j2", cfg_dict)

            print(f"\tGenerating configuration for {filename}")

            utils.save_file(fullpath, rendered)

        print(f"\nSaved files in {cfg_directory}\n")


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description",
        epilog="Usage: ' python monolithic_sw_cfg.py or uv run monolithic_sw_cfg.py # Assumes a CSV file new_switches.csv with new switch payload' ",
    )

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument(
        "-p",
        "--payload_file",
        help="CSV Payload file to use Default is new_switches.csv",
        action="store",
        default="new_switches.csv",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="output directory for configuration files Default is cfg_output",
        action="store",
        default="cfg_output",
    )
    parser.add_argument(
        "-s",
        "--secret_temp",
        help="Temporary enable secret and login password",
        action="store",
        default="T3mp@ecreto",
    )
    parser.add_argument(
        "-t",
        "--timezone",
        help="Timezone defaults to America/Los_Angeles",
        action="store",
        default="America/Los_Angeles",
    )

    arguments = parser.parse_args()
    main()
