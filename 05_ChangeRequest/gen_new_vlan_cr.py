#!/usr/bin/python -tt
# Project: ac3_templating_workshop
# Filename: gen_new_vlan_cr.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "10/11/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import os
import sys
import pprint
import json
import webbrowser
import requests


from utils import utils


def create_std_cr_snow(
    instance,
    username,
    password,
    payload,
    template_id="b9c8d15147810200e90d87e8dee490f6",
):
    """

    Given the FQDN of a live Service Now Personal Developer Instance and the accompanying credentials,
    this function will create a change request with the provided payload.

    :param instance: FQDN of developer instance
    :param username: instance username
    :param password: instance password
    :param payload: ticket payload
    :param template_id: SNOW CR template ID
    :return:
    """

    # ServiceNow instance details

    # API endpoint
    url = f"https://{instance}/api/now/table/change_request"

    # Headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Send POST request
    try:
        response = requests.post(
            url, auth=(username, password), headers=headers, data=json.dumps(payload)
        )
    except Exception as e:
        print("\nERROR in request! Please verify your SNOW URL and credentials!\n")
        print(e)
        exit("\nAborting Run!\n")
    # Check response
    # A 201 status code is returned when a new resource is created
    if response.status_code == 201:
        print(f"Standard Change Request created successfully: {response.status_code}")
        # pprint.pprint(response.json())
    else:
        print(f"Error creating Standard Change Request: {response.status_code}")
        # print(response.text)

    return response


def main():
    """
    This script will load new vlan payload information in a CSV file and create text describing the desired work
    to enable the vlan and its SVI.

    :return:
    """

    payload_data = utils.load_csv(arguments.payload_file)

    # Turn payload data into a list of dictionaries
    payload_lod = utils.lists_to_dicts(payload_data)

    # This works for one or more vlans to be defined
    for details_dict in payload_lod:

        # Assumption:  You are doing one vlan per CR
        # Is a better assumption one CR for n Vlans??  That's a business process decision.

        # Start data manipulation
        # assuming SLA is 3 days, calculate due date from day of submittal (assuming submitted today)
        requested_by_date = utils.calculate_future_business_date(3)

        # create the vlan name based on standard types (user, server, building_automation
        # is this the safest way to test for type???
        if details_dict["type"] == "user":
            vlan_name = f"USER_{details_dict['subnet_cidr']}"
        elif details_dict["type"] == "server":
            vlan_name = f"SRV_{details_dict['subnet_cidr']}"
        elif details_dict["type"] == "building_automation":
            vlan_name = f"BLDAUTO_{details_dict['subnet_cidr']}"
        else:
            print("Vlan name cannot be set. Aborting execution!")
            sys.exit()

        # Update the payload dictionary (details_dict here) for this
        details_dict.update(
            {
                "requested_by_date": requested_by_date,
                "vlan_name": vlan_name,
                "svi_ip": utils.get_first_ip(details_dict["subnet_cidr"]),
            }
        )

        # We will use our "render in one" function to
        # - create the environment
        # - load the template
        # - render the template with our payload
        rendered_string = utils.render_in_one("new_vlan_cr_template.j2", details_dict)

        # Lets save our rendered output
        # Crafting a somewhat meaningful filename
        filename = f"{details_dict['location']}_NewVlan{details_dict['new_vlan']}_SNOW_STDCR.txt"

        # Create output directory and set the full path
        cr_text_fp = utils.create_output_dir_fp(
            os.getcwd(), arguments.output_dir, filename
        )

        # Saving the output to a text file
        utils.save_file(cr_text_fp, rendered_string)

        print(
            f"Saved resulting CR text to {filename} in {arguments.output_dir} directory"
        )

        # Craft CR short description

        short_desccription = (
            f"AC3 {utils.get_username()} "
            f"Vlan Work Set new Vlan {details_dict['new_vlan']} "
            f"for subnet {details_dict['subnet_cidr']} on {details_dict['gateway_device']} "
        )

        if arguments.create_cr and arguments.password:
            # Need to create CR in SNOW
            #     keys = ["instance", "username", "password", "template", "short_desc", "desc", "test_plan", ]
            cr_payload = {
                "short_description": short_desccription,
                "description": rendered_string,
                "test_plan": "ping",
                "justification": "Building automation project",
                "implementation_plan": "Just do it",
                "risk_impact_analysis": "net new so risk minimal, no active users",
                "backout_plan": "undo the work",
                "template_id": "b9c8d15147810200e90d87e8dee490f6",
            }

            utils.set_os_env("pdi_uname", arguments.username)
            utils.set_os_env("pdi_pwd", arguments.password)

            username = utils.get_os_env("pdi_uname")
            password = utils.get_os_env("pdi_pwd")

            resp = create_std_cr_snow(
                arguments.snow_pdi, username, password, cr_payload
            )

            if resp:

                resp_dict = resp.json()
                url_top = f"https://{arguments.snow_pdi}/"

                # Open default browser to Service Now URL
                webbrowser.open(url_top)

                print(
                    f"Created Standard Change Request {resp_dict['result']['task_effective_number']}"
                )
                # print(resp.url)
                # print(resp.links)

            else:
                print("Limited response returned")

        if arguments.create_cr and not arguments.password:
            print(
                f"ERROR! Please enter a password (-p) for SNOW PDI and update the username (-u) if its not 'admin'"
            )


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description",
        epilog="Usage: ' python gen_new_vlan_cr.py'  or 'uv run gen_new_vlan_cr.py' ",
    )

    parser.add_argument(
        "-f",
        "--payload_file",
        help="Change details payload file. Default is payload.csv in current directory",
        action="store",
        default="payload.csv",
    )
    parser.add_argument(
        "-c",
        "--create_cr",
        help="Create Change Request in SNOW. Default is False so no CR in SNOW will be created.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-s",
        "--snow_pdi",
        help="Service Now (SNOW) Personal Developer Instance. Default: 'dev224081.service-now.com'",
        action="store",
        default="dev224081.service-now.com",
    )
    parser.add_argument(
        "-u",
        "--username",
        help="Service Now (SNOW) Personal Developer Instance Username. Default: admin",
        action="store",
        default="admin",
    )
    parser.add_argument(
        "-p",
        "--password",
        help="Service Now (SNOW) Personal Developer Instance password. Default: empty string",
        action="store",
        default="",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="output directory CR text. Default is output",
        action="store",
        default="output",
    )

    arguments = parser.parse_args()
    main()
