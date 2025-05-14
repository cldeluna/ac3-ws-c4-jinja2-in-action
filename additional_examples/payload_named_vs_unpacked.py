#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: payload_named_vs_unpacked.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "11/3/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"


import utils


def main():
    """
    Short script to illustrate the differences between passing a named variable (data structure or payload) to
    a Jinja2 template vs passing the variable itself and using the default ** (unpacking) behavior.

    While the un-named strategy exposes the keys directly, it is harder to troubleshoot and handle lists.

    :return:
    """

    # Step 1 - Define the environment containing the templates you want to use
    # Here all the templates will be in a directory called "templates" relative to the current directory

    env_obj = utils.jenv_filesystem(line_comment="", ktn=True, lsb=True, tb=True)

    # Step 2 - Load the specific template to be used
    template_obj_upacked = env_obj.get_template("test_unpacked.j2")

    template_obj_named = env_obj.get_template("test_named.j2")

    # Template Payload
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

    print(payload_dict.keys())

    # You cannot directly access unnamed positional arguments in standalone Jinja2 templates.
    # payload_list = [-1, 0, 1, 2, 3, 4, 5, 6]
    # rendered_unpacked = template_obj_unpacked.render(payload_list)

    # Step 3 - Render the template with specific payload
    # The unpacked template will need to know the keys
    rendered_unpacked = template_obj_upacked.render(payload_dict)

    print("\n==== Passing Un-named and Unpacked variable ====")
    print(rendered_unpacked)

    # The named template will just dump whatever is in the named variable cfg
    rendered_named = template_obj_named.render(cfg=payload_dict)

    print("\n==== Passing named variable ====")
    print(rendered_named)


# Standard call to the main() function.
if __name__ == "__main__":
    main()
