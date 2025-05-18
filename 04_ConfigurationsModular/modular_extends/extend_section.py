#!/usr/bin/python -tt
# Project: ac3_templating_workshop
# Filename: extend_section.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/18/25"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import jinja2


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


def template_map():
    tmap = {
        "aaa": "mod_inherit_aaa.j2",
        "interfaces": "mod_inherit_interfaces.j2",
        "ospf": "mod_inherit_ospf.j2",
        "base": "mod_inherit_base.j2",
    }

    return tmap


def main():

    # Set up the Jinja2 environment
    template_dir = "templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

    # Load configuration payload
    cfg_data = load_cfg_data()

    # Load Template Map
    tmap = template_map()

    if arguments.section:

        template_file = tmap[arguments.section]
        print(f"Using template: {template_file}")
        template = env.get_template(template_file)

        print(f"Rendering template: {template_file}")
        print(template.render(cfg_data))


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python extend_section.py' ")

    parser.add_argument('-s', '--section', help='Specify section (aaa, interfaces, ospf, base)', action='store',default="base")
    arguments = parser.parse_args()
    main()
