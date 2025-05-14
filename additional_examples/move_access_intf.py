#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: move_access_intf.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "11/2/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"


import jinja2
from utils import utils


def main():

    # Step 1 - Define the environment containing the templates you want to use
    # Here all the templates will be in a directory called "templates" relative to the current directory
    env_obj = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates", encoding="utf-8")
    )

    # Step 2 - Load the specific template to be used
    template_obj = env_obj.get_template("move_intf.j2")

    # Template Payload
    cfg_dict = { "GigabitEthernet1/0/27": 300,}

    # Step 3 - Render the template with specific payload
    # The template is expecting a dictionary named "cfg"

    rendered = template_obj.render(cfg=cfg_dict, desc="Digital Signage")
    print(rendered)



# Standard call to the main() function.
if __name__ == "__main__":
    main()
