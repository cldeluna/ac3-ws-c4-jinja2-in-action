#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: modular_include_config_generator.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "11/2/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"


import os
import jinja2
import pathlib


def load_cfg_data():
    config_data = {
        "hostname": "ROUTER-1",
        "tacacs_server": "TACACS-1",
        "tacacs_ip": "192.168.1.100",
        "tacacs_key": "tacacs123",
        "local_users": [
            {"name": "admin", "privilege": 15, "password": "admin123"},
            {"name": "operator", "privilege": 5, "password": "oper123"},
        ],
        "interfaces": [
            {
                "name": "GigabitEthernet0/0",
                "description": "WAN Interface",
                "ip_address": "10.1.1.1",
                "subnet_mask": "255.255.255.0",
                "ospf_area": "0",
            },
            {
                "name": "GigabitEthernet0/1",
                "description": "LAN Interface",
                "ip_address": "192.168.1.1",
                "subnet_mask": "255.255.255.0",
                "ospf_area": "1",
            },
        ],
        "ospf_process_id": 1,
        "router_id": "1.1.1.1",
        "ospf_networks": [
            {"prefix": "10.1.1.0", "wildcard": "0.0.0.255", "area": "0"},
            {"prefix": "192.168.1.0", "wildcard": "0.0.0.255", "area": "1"},
        ],
        "redistribute": ["connected", "static"],
    }

    return config_data


def main():

    # Load configuration payload
    cfg_data = load_cfg_data()

    # Create Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Load base template
    template = env.get_template("modular_inc_base.j2")

    # Render configuration
    config = template.render(cfg_data)

    # Check to see if the output directory exists and if it does not, create it
    # This is the directory where we will store the resulting config files
    output_dir = "cfg_output"
    cfg_directory = os.path.join(os.getcwd(), output_dir)
    pathlib.Path(cfg_directory).mkdir(exist_ok=True)

    # Save the configuration to a file
    file_name = f"{cfg_data['hostname']}_router_config_using_includes.txt"
    fp = os.path.join(cfg_directory, file_name)

    with open(fp, "w") as f:
        f.write(config)

    print(f"\nSaved configuration to file {file_name} in current directory.\n")


# Standard call to the main() function.
if __name__ == "__main__":
    main()
