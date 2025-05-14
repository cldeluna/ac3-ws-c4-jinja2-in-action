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

import pprint

# Notice we don't need to import Jinja2 here as we are using the function in utils.py
from utils import utils


def main():
    """
    This script is a more evolved version of "move_access_intf.py" which includes only using the env function
    from utils and includes a more complex data structure sent to a Template wich uses Jinja2 macros.
    :return:
    """

    # Step 1 - Define the environment containing the templates you want to use
    # Here all the templates will be in a directory called "templates" relative to the current directory
    env_obj = utils.jenv_filesystem(line_comment="##", ktn=True, lsb=True, tb=True)

    # Step 2 - Load the specific template to be used
    template_obj = env_obj.get_template("move_intf_w_macro.j2")

    # Template Payload
    # Creating a dictionary for the first 5 GigE interfaces using the GigE shorthand so we can use the
    # interface expansion macro in the template to expand the interface
    cfg_dict = dict()
    desc = "supply kiosk"

    for idx in range(34, 39):
        # Cisco UXM switches
        if idx > 36:
            intf_prefix = "Te"
        else:
            intf_prefix = "Tw"
        cfg_dict.update(
            {
                f"{intf_prefix}1/0/{idx}": {
                    "new_vlan": 300,
                    "desc": desc,
                    "original_intf": f"GigE1/0/{idx}",
                }
            }
        )

    pprint.pprint(cfg_dict)

    # Step 3 - Render the template with specific payload
    # The template is expecting a dictionary named "cfg"
    desc = ""
    rendered = template_obj.render(cfg=cfg_dict)

    print(rendered)


# Standard call to the main() function.
if __name__ == "__main__":
    main()
