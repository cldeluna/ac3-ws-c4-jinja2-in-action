#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: gen_bgp_report
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "10/4/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import jinja2
import json
import sys
import os
import re

from diagrams import Diagram, Edge
from diagrams.generic.network import Router
from typing import Optional, Dict, Any


def replace_special_chars(text: str) -> str:
    """
    Replace spaces and special characters in the provided text string with underscores
    :param text:
    :return: string with underscores replacing anything that is not alphanumeric.
    """

    return re.sub(r"[^a-zA-Z0-9]", "_", text)


def load_json(filename: str) -> Optional[Dict[str, Any]]:
    """
    Safely load a JSON file
    :param filename:
    :return: data or None
    """

    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{filename}'. {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    return None


def save_file(fn: str, text: str) -> str:
    """
    Simple function to save text to a file fn
    :param fn: filename or full path filename
    :param text:
    :return: fn
    """
    with open(fn, "w") as f:
        f.write(text)

    return fn


def create_bgp_diagram(
    bgp_sessions: list, filename: str = "bgp_sessions", outformat: str = "png"
) -> None:
    """
    Given a list of dictionaries in bgp_sessions with local and peer information, draw a diagram which
    shows each peering session including state and ASN

    from diagrams import Diagram, Edge
    from diagrams.generic.network import Router

    # Diagram and Edge are in the diagrams module
    with diagrams.Diagram("Example Diagram"):
        # Router is in diagrams.generic.network
        router1 = diagrams.generic.network.Router("Router 1")
        router2 = diagrams.generic.network.Router("Router 2")
        router1 >> diagrams.Edge(label="Connection") >> router2


    :param bgp_sessions:
    :param filename:
    :return: Nothing but the file is saved as "filename".
    """

    try:
        with Diagram(
            "BGP Sessions",
            show=False,
            filename=filename,
            direction="LR",
            outformat=outformat,
        ):
            # Initialize an empty dictionary which will have a key and Diagram object based on each element
            # (peering session dictionary) of the list
            routers = {}

            for session in bgp_sessions:
                # Create each local nodes
                local_key = f"{session['hostname']}_{session['asn']}"
                if local_key not in routers:
                    routers[local_key] = Router(
                        f"{session['hostname']}\nAS {session['asn']}"
                    )

                # Create peer nodes
                peer_key = f"{session['peerHostname']}_{session['peerAsn']}"
                if peer_key not in routers:
                    routers[peer_key] = Router(
                        f"{session['peerHostname']}\nAS {session['peerAsn']}"
                    )

                # Create edge with session details
                edge_label = f"State: {session['state']}\nVRF: {session['vrf']}"
                routers[local_key] - Edge(label=edge_label) - routers[peer_key]

    except Exception as e:
        print("\n\nDIAGRAM ERROR!!")
        print(f"{e}\n\n")


def main() -> None:
    print("\n======= EXECUTING BGP Report Script=======")

    # Step 1: Create Environment
    if arguments.step <= 1:

        print("\n\n=== STEP 1: Create Environment ===")

        env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

        # Tip: if you want to see the various methods availalbe to an object use dir(object)
        # print(dir(env))

        print(
            f"Object env has been created using loader=jinja2.FileSystemLoader('templates')\n{env}\n"
        )

        print(f"Templates directory is {env.loader.searchpath}\n")
        print(f"Loader is {env.loader}\n")
        print(f"lstrip_blocks is {env.lstrip_blocks}\n")
        print(f"trim_blocks is {env.trim_blocks}\n")
        print(f"keep_trailing_newline is {env.keep_trailing_newline}\n")

    # TODO: Future: Add option to use a custom template
    # ====  START Example of an interactive CLI to pick the template
    # What templates are available in this environment?
    # template_list = env.list_templates()

    # Print the list of templates available in the defined environment
    # which is looking at a relative path in the "templates" directory
    # for template in template_list:
    #     print(template)

    # selected_template = utils.get_template_selection(template_list)
    # print(f"You selected: {selected_template}")
    # ====  END Example of an interactive CLI to pick the template

    # Step 2: Load the template
    if arguments.step <= 2:

        print("\n\n=== STEP 2: Load the template and craft the payload ===")

        # Set template file (this file should be in the templates directory under 01_CurrentStateReport
        selected_template = "bgp_report_md.j2"

        bgp_rpt_template = env.get_template(selected_template)

        # This is only needed to display the template in the Terminal
        bgp_rpt_template.source = open(bgp_rpt_template.filename).read()
        print(f"\nTemplate name: {bgp_rpt_template.name}")
        print(f"Template filename: {bgp_rpt_template.filename}")

        print(f"\nTemplate {selected_template} Source (View the Template):\n")
        print(bgp_rpt_template.source)

        # -------------------- Manipulate the data --------------------
        # In this case we have queried SuzieQ for a list of BGP sessions at the GDL_Campus

        # Load the JSON file GDL_bgp.json into a variable named data
        # Calculate a boolean all_peers_up (bool)
        # Calculate the number of iBGP sessions in ibgp_count (int)
        # Calculate the number of eBGP sessions in ebgp_count (int)
        # Tip: Take a look at the JSON file with the data and determine how you are going to process it to get the
        # values above

        # Load the JSON file
        data_fn = "GDL_bgp.json"
        print(f"\nLoading data from {data_fn}")
        data = load_json(data_fn)

        print(
            f"\nCalculating all_peers_up, ibgp_count, ebgp_count from data of type {type(data)} from file {data_fn}"
        )

        # Boolean to see if all sessions are up
        all_peers_up = True
        ibgp_count = 0
        ebgp_count = 0
        for line in data:
            if "Down" in line["state"]:
                all_peers_up = False
            if line["asn"] == line["peerAsn"]:
                ibgp_count += 1
            else:
                ebgp_count += 1

        print("\nCreating BGP diagram from data")
        # Define a filename for the Markdown report and the resulting diagram
        drawing_filename = f"{replace_special_chars(arguments.location)}_BGP_Diagram"
        outformat = "jpg"

        if data:
            create_bgp_diagram(data, filename=drawing_filename, outformat=outformat)
            print(f"\nDiagram saved as {drawing_filename}.{outformat}\n")

    # Step 3  Render the template
    if arguments.step <= 3:

        print("\n\n=== STEP 3: Render the template with the BGP data ===")
        # Render the template with the BGP data
        # Tip: Look at the template and see what template variables its expecting you to send and see if you can
        # determine the type by looking at the logic

        rendered_config = bgp_rpt_template.render(
            location=arguments.location,
            bgp_list=data,
            all_peers_up=all_peers_up,
            ibgp_count=ibgp_count,
            ebgp_count=ebgp_count,
            drawing_filename=f"{drawing_filename}.{outformat}",
        )

        print("=============== RENDERED RESULT ===============")
        print(rendered_config)
        print("===============================================\n")

        # FINAL STEP: Save the file using a filename like XXX_Location_bgp_report_starter.md
        # Tip: the utils module has a function to help removes spaces and special characters and one of the CLI
        # options is for the location
        filename = replace_special_chars(arguments.location)
        # if rendered_config is empty don't save an empty report
        if rendered_config:
            save_file(
                f"{filename}_BGP_REPORT.md",
                rendered_config,
            )


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description",
        epilog="Usage: ' python gen_bgp_report.py' or python gen_bgp_report.py -l 'AMS Campus'",
    )

    parser.add_argument(
        "-s",
        "--step",
        type=int,
        help="Execute a specific step. Default: 0 which executes all steps",
        action="store",
        default=0,
    )

    parser.add_argument(
        "-t",
        "--title",
        help="Add Custom Title to report. Default: BGP_Report",
        action="store",
        default="BGP Report",
    )
    parser.add_argument(
        "-l",
        "--location",
        help="Location Default: GDL Campus",
        action="store",
        default="GDL Campus",
    )
    arguments = parser.parse_args()
    main()
