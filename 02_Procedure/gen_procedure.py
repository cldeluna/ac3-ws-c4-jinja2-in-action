#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: gen_procedure
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "9/2/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import sys
import os
import re
import datetime
import pprint


### This is no longer necessary because we are using uv and utils is now a module
# # This is necessary because I want to import functions in a file called utils.py and that file is one level up
# # from here
# # Get the absolute path of the top level main repository
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # Append the parent directory to sys.path so python searches that directory for the utils file
# sys.path.append(parent_dir)
# # Import the utils module (python script) one level up
# try:
#     import utils
# except:
#     print(f"Move this script up a level to execute.")
#     exit("Aborting run!")

# Import all the functions from the local utils module
from utils import utils


def main():

    # ------------------------------------------ PAYLOAD SETUP -------------------------------------------------
    # Date stamp for Report if one already exists
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Format as human-readable string
    human_readabl = "This is NOT a Human Readable Timestamp!!"
    human_readable = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # ----------------------------------------------------------------------------------------------------------
    # Load the installation details YAML file
    payload_dict = utils.load_yaml(arguments.payload_file)
    print("YAML File Contents")
    pprint.pprint(payload_dict)
    # ----------------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------------
    # Select Image
    # This sets the image we will use in the document
    if re.search(r"600", payload_dict["model"]):
        img = os.path.join(".", "images", "ORDR_S600_Sensor.jpg")
    elif re.search(r"2000", payload_dict["model"]):
        img = os.path.join(".", "images", "ORDR_S2000_Sensor.jpg")
    else:
        img = os.path.join(".", "images", "istockphoto-519363862-612x612.jpeg")

    #  ----------------------------------- ADDING DATA TO PAYLOAD DICT  ----------------------------------------
    # Here we are adding the appropriate diagram image to the payload dictionary
    payload_dict.update({"diagram": img})

    # Update the payload dictionary we will send to the template with the human readable timestamp
    payload_dict.update({"dattim": human_readabl})

    # Get Gateway
    payload_dict.update({"mgmt_gw": utils.get_first_ip(payload_dict["mgmt_subnet"])})

    # Get Mask in dotted notation
    mgmt_mask = utils.get_mask_from_cidr(payload_dict["mgmt_subnet"])
    payload_dict.update({"mgmt_mask": mgmt_mask})

    # Get Appliance IP (4th Valid in subnet)
    payload_dict.update({"mgmt_ip": utils.get_fourth_ip(payload_dict["mgmt_subnet"])})

    # ----------------------------------------------------------------------------------------------------------
    # CREATE JINJA2 TEMPLATE ENVIRONMENT
    # Note: in the jenv_filesystem function the default line comment is #
    #       Because # is part of the Markdown syntax we need to use something else if we
    #       are rendering Markdown otherwise our # Titles will be interpreted by Jinja as comments!
    env_obj = utils.jenv_filesystem(line_comment="=")
    # print(env_obj.list_templates())
    # ADD DEBUGGING Just In Case
    env_obj.add_extension("jinja2.ext.debug")

    # LOAD TEMPLATE
    template_obj = utils.load_jtemplate(
        env_obj, template_file_name="installation_procedure_md_templat.j2"
    )
    rendered = template_obj.render(cfg=payload_dict)

    # ----------------------------------------------------------------------------------------------------------
    # Save the rendered content to a file

    # Define the filename
    # Remove special characters from location including replacing spaces with underscores
    location = utils.replace_special_chars(payload_dict["location"])
    filename = f"{location}_ORDR_Appliance_Installation_{file_timestamp}.md"

    # Create output directory and set the full path
    procedure_fp = utils.create_output_dir_fp(
        os.getcwd(), arguments.output_dir, filename
    )

    if procedure_fp:
        # Save the rendered content to the file
        utils.save_file(procedure_fp, rendered)
        print(f"\n\nInstallation Markdown file {filename} created.")
        print(f"\tSaved file to {procedure_fp}\n")


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description",
        epilog="Usage: ' python or uv run gen_procedure_starter_starter.py <payload yaml>' Example payload yaml: 'Installation_details_S2000.yml'.  ",
    )

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument(
        "payload_file",
        help="YAML Payload file to use. Default: Installation_details_S2000.yml",
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        help="output directory Markdown procedure files. Default is output.",
        action="store",
        default="output",
    )

    arguments = parser.parse_args()
    main()
