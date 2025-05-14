#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: one_step_jinja.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "9/4/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import utils


def main():
    """
    Test script for the all in one template and the all in one "render in one" jinja function
    which executes all three steps
    in the Jinja workflow (create environment, load template, render template with provided payload)

    """
    # All in one

    payload_dict = {
        "list": [1, 2, 3, 4, 5],
        "maxstack": 9,
        "hostname": "myswitch-01",
        "mydict": {
            "subnet": "192.168.0.0/24",
            "gw": "192.168.0.1",
            "mask": "255.255.255.0",
        },
    }

    rendered = utils.render_in_one(
        "all_in_one.j2", payload_dict, search_dir="templates", line_comment="#"
    )
    print(rendered)


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description", epilog="Usage: ' python one_step_jinja.py' "
    )

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    # parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',default=False)
    arguments = parser.parse_args()
    main()
