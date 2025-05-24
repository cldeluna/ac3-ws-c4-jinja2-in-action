#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: combo_cfg.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "10/9/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import jinja2


def main():

    # Set up the Jinja2 environment
    # template_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = "templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

    # Load the combined template
    combined_template = env.get_template("combined_switch_config.j2")

    # Sample data
    switch_data = {
        "hostname": "SW-ACCESS-01",
        "user_vlan": 100,
        "user_interface": "GigabitEthernet1/0/1",
        "tacacs_server_ip": "192.168.1.100",
        "tacacs_key": "SecretKey123",
    }

    # Render the combined template
    combined_config = combined_template.render(switch_data)

    # Print the rendered configuration
    print("Combined Switch Configuration:")
    print(combined_config)

    # Optionally, save the configuration to a file
    with open("combined_switch_config.txt", "w") as f:
        f.write(combined_config)

    print("\nCombined configuration has been saved to a text file.")


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description", epilog="Usage: ' python combo_cfg.py' "
    )

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    # parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',default=False)
    arguments = parser.parse_args()
    main()
