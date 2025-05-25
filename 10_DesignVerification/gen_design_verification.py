#!/usr/bin/python -tt
# Project: demo_infrahub_sdk
# Filename: gen_design_verification.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/12/25"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"


import os
import pprint
import argparse
import datetime
from infrahub_sdk import InfrahubClientSync, Config

from utils import utils


def get_expected_vlans_ihub():
    config = Config(
        address="https://demo.infrahub.app",
        api_token="1842b798-22d1-28f2-d7ee-106521adfe49",
    )

    client = InfrahubClientSync(config=config)

    all_items = client.all(arguments.kind)

    if arguments.kind == "InfraVLAN":
        print("InfraVLAN")
        for vlan in all_items:
            print(vlan)
            print(f"VLAN ID: {vlan.vlan_id.value}, Name: {vlan.name.value}")

    if arguments.kind == "LocationGeneric":
        print("LocationGeneric")
        for item in all_items:
            print(item)
            print(item.name.value)
            # print(dir(item))
            # print(f"VLAN ID: {vlan.vlan_id.value}, Name: {vlan.name.value}")


def flatten_person(obj):
    result = {}
    for attr in [
        "id",
        "first_name",
        "last_name",
        "middle_name",
        "email",
        "mobile",
        "remote_worker",
        "default_location",
        "display_label",
        "hfid",
    ]:
        value = getattr(obj, attr, None)

        # If it's an InfraHub Attribute object, extract its `.value`
        if hasattr(value, "value"):
            result[attr] = value.value

        # If it's a list, preserve or stringify it
        elif isinstance(value, list):
            result[attr] = ", ".join(map(str, value))

        # Use scalar or None directly
        else:
            result[attr] = value
    return result


def flatten_vlans(obj):
    result = {}
    for attr in [
        "id",
        "description",
        "display_label",
        "gateway",
        "hfid",
        "name",
        "role",
        "site",
        "satus",
        "vlan_id",
    ]:
        value = getattr(obj, attr, None)

        # If it's an InfraHub Attribute object, extract its `.value`
        if hasattr(value, "value"):
            result[attr] = value.value

        # If it's a list, preserve or stringify it
        elif isinstance(value, list):
            result[attr] = ", ".join(map(str, value))

        # Use scalar or None directly
        else:
            result[attr] = value
    return result


def get_people():

    IH_SERVER = "https://demo.infrahub.app"
    IH_API_KEY = "1842b798-22d1-28f2-d7ee-106521adfe49"

    # Initialize Config with proper parameters
    config = Config(
        address=IH_SERVER,  # e.g. "https://demo.infrahub.app"
        api_token=IH_API_KEY,  # Not needed for demo server
    )

    client = InfrahubClientSync(config=config)

    # Example: Query all devices (assuming 'InfraDevice' is defined in your schema)
    # all_people = client.all("OrganizationPerson")
    all_people = client.all("InfraVLAN")
    print(all_people)
    print(dir(all_people[0]))
    for person in all_people:
        pprint.pprint(person.get_raw_graphql_data())
        # print(f"Device name: {device.last_name.value}")
        print()

    # people_dicts = [flatten_person(person) for person in all_people]
    # pprint.pprint(people_dicts)


def get_vlans():

    IH_SERVER = "https://demo.infrahub.app"
    IH_API_KEY = "1842b798-22d1-28f2-d7ee-106521adfe49"

    # Initialize Config with proper parameters
    config = Config(
        address=IH_SERVER,  # e.g. "https://demo.infrahub.app"
        api_token=IH_API_KEY,  # Not needed for demo server
    )

    client = InfrahubClientSync(config=config)

    # Example: Query all devices (assuming 'InfraDevice' is defined in your schema)
    all_vlans = client.all("InfraVLAN")
    # print(all_vlans)
    # print(dir(all_vlans[0]))
    # for vlan in all_vlans:
    # pprint.pprint(vlan.get_raw_graphql_data())
    # print(f"Device name: {device.last_name.value}")
    # print()

    vlan_dicts = [flatten_vlans(vlan) for vlan in all_vlans]
    # pprint.pprint(vlan_dicts)

    return vlan_dicts


def main():

    # ------------------------------------------ PAYLOAD SETUP -------------------------------------------------
    # Initialize payload dict for template
    payload_dict = dict()

    # Date stamp for Report if one already exists
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Format as human-readable string
    human_readable = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
    payload_dict.update({"timestamp": human_readable})

    # Get expected vlans at site from Authoratative Desig Store InfraHub
    vlans_lod = get_vlans()

    # Pull out the vlans of interes for our site (ORD)
    vlan_ids = []
    site_of_interest = "ord"
    namespace_of_interest = "ORD_Campus"

    payload_dict.update({"location": namespace_of_interest})

    for item in vlans_lod:
        site_obj = item.get("site")
        if site_obj:
            # Attempt to get a readable site name (adjust this based on your object)
            site_name = getattr(
                site_obj, "display_label", ""
            )  # Or 'name', or str(site_obj)
            if site_of_interest in site_name.lower():
                vlan_ids.append(item.get("vlan_id"))

    print(f"{namespace_of_interest} should have the following vlans: {vlan_ids}")
    payload_dict.update({"expected_vlans": vlan_ids})

    missing_vlans = list()
    for expected_vlan in vlan_ids:
        print(f"Checking for vlan {expected_vlan} at site {namespace_of_interest}")
        vlan_at_site, vlan_resp = utils.find_vlan_at_site(
            expected_vlan, namespace_of_interest
        )
        if vlan_at_site:
            print(f"\tVlan {expected_vlan} is Configured!")
        else:
            print(f"\tVlan {expected_vlan} is NOT Configured!")
            print(f"\tSite Configuration deviates from Design!")
            missing_vlans.append(expected_vlan)

    payload_dict.update({"missing_vlans": missing_vlans})

    # Use the "render in one" utility function
    template_file = "design_vs_implementation_report_template.j2"
    rendered_sow = utils.render_in_one(template_file, payload_dict, line_comment="==")

    # Save the Markdown file
    # Define the filename
    filename = f"{namespace_of_interest}_Design_vs_Implementation_Validation_{file_timestamp}.md"

    # Create output directory and set the full path
    rpt_fp = utils.create_output_dir_fp(os.getcwd(), arguments.output_dir, filename)

    # Save the rendered content to the file
    utils.save_file(rpt_fp, rendered_sow)
    print(f"\n\nSaved Validation Report Markdown file {filename} to \n\t{rpt_fp}\n")


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description", epilog="Usage: ' python test1.py' "
    )

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument(
        "-k",
        "--kind",
        help="Specify the kind for client.all",
        action="store",
        default="InfraVLAN",
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        help="output directory Markdown procedure files. Default is output.",
        action="store",
        default="output",
    )
    arguments = parser.parse_args()
    main()
