#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: gen_sow.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "11/9/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import datetime
import sys
import os

# # This is necessary because I want to import functions in a file called utils.py and that file is one level up
# # from here
# # Get the absolute path of the top level main repository
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # Append the parent directory to sys.path so python searches that directory for the utils file
# sys.path.append(parent_dir)
# # Import the utils module (python script) one level up
# import utils

from utils import utils


def dict_to_markdown_table(data):
    if not data:
        return ""

    headers = list(data[0].keys())
    markdown = "| " + " | ".join(headers) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for item in data:
        row = "| " + " | ".join(str(item.get(h, "")) for h in headers) + " |"
        markdown += row + "\n"

    return markdown


def main():

    # Lets check to see if SQ is running
    print("Checking SuzieQ API Heath.")
    sq_health_check = utils.get_sq_health()
    if not sq_health_check:
        print("ERROR! Cannot connect to SuzieQ API. Please check server and connectivity.")
        exit()

    # Date stamp for Report if one already exists
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Format as human-readable string
    human_readable = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # Payload
    sow = dict()

    namespace = "GDL_Campus"
    extdb_table = "new_ap_cabling"

    sow.update({"location": namespace})
    sow.update({"extdb": extdb_table})
    sow.update({"timestamp": human_readable})

    # Get the cabling information from SuzieQ
    resp = utils.get_extdb(extdb_table, namespace)

    sow.update({"data_lod": resp.json()})

    # Use a set comprehension to extract unique model values
    unique_models = {item['APModel'] for item in resp.json() if 'APModel' in item}

    sow.update({"models": list(unique_models)})

    # AP Placement Map List
    maps = {item['APLoationMap'] for item in resp.json() if 'APLoationMap' in item}

    sow.update({"maps": list(maps)})

    sow.update({"mdtable": dict_to_markdown_table(resp.json())})

    template_file = "ap_cabling_sow_md_template.j2"
    # template_file = "test.j2"
    rendered_sow = utils.render_in_one(template_file, sow, line_comment="==")

    # Define the filename
    filename = (
        f"{namespace}_AP_Installation_Statement_of_Work_{file_timestamp}.md"
    )

    # Create output directory and set the full path
    sow_fp = utils.create_output_dir_fp(os.getcwd(), arguments.output_dir, filename)

    # Save the rendered content to the file
    utils.save_file(sow_fp, rendered_sow)
    print(f"\n\nSaved installation Markdown file to {sow_fp}\n")


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python gen_sow.py' or 'uv run gen_sow.py' ")
    arguments = parser.parse_args()

    parser.add_argument(
        "-o",
        "--output_dir",
        help="output directory Markdown procedure files. Default is output.",
        action="store",
        default="output",
    )

    main()
