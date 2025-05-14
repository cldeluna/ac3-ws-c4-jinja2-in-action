#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: modular_inheritance_config_generator.py
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
        "hostname": "ROUTER-2",
        "tacacs_server": "192.168.1.10",
        "tacacs_key": "secret123",
        "interfaces": [
            {
                "name": "GigabitEthernet0/1",
                "description": "Link to Core",
                "ip_address": "10.1.1.1",
                "subnet_mask": "255.255.255.0",
                "ospf_area": "0",
            },
            {
                "name": "GigabitEthernet0/2",
                "description": "Link to Distribution",
                "ip_address": "10.1.2.1",
                "subnet_mask": "255.255.255.0",
                "ospf_area": "1",
            },
        ],
        "ospf_process_id": 100,
        "router_id": "1.1.1.1",
        "ospf_networks": [
            {"prefix": "10.1.1.0", "wildcard": "0.0.0.255", "area": "0"},
            {"prefix": "10.1.2.0", "wildcard": "0.0.0.255", "area": "100"},
        ],
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

    # Load templates
    base_template = env.get_template("mod_inherit_base.j2")
    aaa_template = env.get_template("mod_inherit_aaa.j2")
    interfaces_template = env.get_template("mod_inherit_interfaces.j2")
    ospf_template = env.get_template("mod_inherit_ospf.j2")

    # Generate configurations
    config_sections = {
        "base": base_template.render(cfg_data),
        "aaa": aaa_template.render(cfg_data),
        "interfaces": interfaces_template.render(cfg_data),
        "ospf": ospf_template.render(cfg_data),
    }

    print(config_sections["base"])
    print(config_sections["aaa"])
    print(config_sections["interfaces"])
    print(config_sections["ospf"])

    # Check to see if the output directory exists and if it does not, create it
    # This is the directory where we will store the resulting config files
    output_dir = "cfg_output"
    cfg_directory = os.path.join(os.getcwd(), output_dir)
    pathlib.Path(cfg_directory).mkdir(exist_ok=True)

    # Save the configuration to a file
    file_name = f"{cfg_data['hostname']}_router_config_using_inheritance_extends.txt"
    fp = os.path.join(cfg_directory, file_name)

    with open(fp, "w") as f:
        f.write(config_sections["base"])
        f.write(config_sections["aaa"])
        f.write(config_sections["interfaces"])
        f.write(config_sections["ospf"])

    print(f"\nSaved configuration to file {file_name} in a new {output_dir} directory.\n")


# Standard call to the main() function.
if __name__ == "__main__":
    main()
