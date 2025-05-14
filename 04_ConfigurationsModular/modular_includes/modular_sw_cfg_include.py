#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: modular_sw_cfg_include.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "10/10/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import os
import jinja2
import pathlib
import argparse


def main():

    # Set up the Jinja2 environment
    # template_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = "templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

    # Load the main template
    main_template = env.get_template('main_switch_config_include.j2')

    # Sample data
    switch_data = {
        'hostname': 'SW-ACCESS-01',
        'user_vlan': 100,
        'user_interface': 'GigabitEthernet1/0/1',
        'tacacs_server_ip': '192.168.1.100',
        'tacacs_key': 'SecretKey123'
    }

    # Render the main template
    combined_config = main_template.render(switch_data)

    # Print the rendered configuration
    print("Combined Switch Configuration:")
    print(combined_config)

    # Check to see if the output directory exists and if it does not, create it
    # This is the directory where we will store the resulting config files
    output_dir = "cfg_output"
    cfg_directory = os.path.join(os.getcwd(), output_dir)
    pathlib.Path(cfg_directory).mkdir(exist_ok=True)

    # Save the configuration to a file
    filename = "combined_switch_config_include.txt"
    fp = os.path.join(cfg_directory, filename)
    with open(fp, 'w') as f:
        f.write(combined_config)

    print("\nCombined configuration has been saved as:")
    print(fp)
    print()


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python modular_sw_cfg_include.py' ")

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    # parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',default=False)
    arguments = parser.parse_args()


    main()
