#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: stp_verification_app.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "11/10/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"


import os
import sys
import pandas as pd
import datetime
import streamlit as st


# # This is necessary because I want to import functions in a file called utils.py and that file is one level up
# # from here
# # Get the absolute path of the top level main repository
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # Append the parent directory to sys.path so python searches that directory for the utils file
# sys.path.append(parent_dir)
# # Import the utils module (python script) one level up
# import utils


from utils import utils


def generate_report(selected_switches, vlan_id):
    """Generate a markdown report based on selected switches and VLAN ID."""
    report = f"""
# Network Configuration Report

## VLAN Configuration
**VLAN ID:** {vlan_id}

## Selected Switches
"""
    for switch in selected_switches:
        report += f"- {switch}\n"

    report += "\n## Configuration Summary\n"
    if selected_switches:
        report += f"VLAN {vlan_id} should be configured on {len(selected_switches)} switch{'es' if len(selected_switches) > 1 else ''}."
    else:
        report += "No switches selected for configuration."

    report += f"""

VLAN {vlan_id} should be 
- configured on each switch, 
- should have a properly formatted name, 
- should be participating in Spanning Tree and 
- have a root interface

"""
    return report


def main():

    # Date stamp for Report if one already exists
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Format as human-readable string
    human_readable = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")

    selected_switches = list()
    namespace_list = list()
    selected_ns = list()

    # Set page title
    st.set_page_config(page_title="Vlan Provisioning Verification Tool", layout="wide")

    # Add header
    st.title("Vlan Provisioning Verification Tool")

    # Lets check to see if SQ is running
    sq_health_check = utils.get_sq_health()
    if not sq_health_check:
        st.error("Cannot connect to SuzieQ API. Please check server and connectivity.")
        st.write(sq_health_check)
        st.stop()

    # Initialize session state for inputs
    if "namespace" not in st.session_state:
        st.session_state.namespace = ""
    if "device_list" not in st.session_state:
        st.session_state.device_list = list()
    if "vlan_id" not in st.session_state:
        st.session_state.vlan_id = 1

    # Create two columns for inputs
    col1, col2 = st.columns(2)

    with col1:

        # Get Namespaces
        namespace_list, full_response = utils.get_namespace_list()
        if full_response.ok:
            pass
        else:
            st.error(
                f"Aborting Run! Cannot access SuzieQ API! Status Code: "
                f"{full_response.status_code} Reason: {full_response.reason} "
            )
            st.info(
                f"Please make sure you have a .env file at the top level of your repository and a valdi token in "
                f"the environment variable SQ_API_TOKEN."
            )
            st.info("There is an .env_sample file which can be renamed to .env and updated with the valid token.")
            st.stop()

        try:

            selected_ns = st.selectbox(
                "Select Location",
                namespace_list,
                help="Choose the location where you want to verify the VLAN configuration",
                placeholder="Choose a location",
                index=None,
                key="namespace",
            )
        except:
            st.write("Select Location")

        if selected_ns:
            # Sample list of switches (you can modify this list)
            available_switches, full_response = utils.get_device_list(selected_ns)

            # Create multi-select for switches
            selected_switches = st.multiselect(
                "Select Switches",
                available_switches,
                help="Choose the switches where you want to configure the VLAN",
                key="device_list",
            )

        # Create VLAN ID input
        vlan_id = st.number_input(
            "VLAN ID",
            min_value=1,
            max_value=4094,
            # value=1,
            help="Enter a VLAN ID between 2 and 4094",
            key="vlan_id",
        )

    with col2:
        st.write(st.session_state)

    # Add a separator
    st.divider()

    # Generate and display report

    selected_switches = st.session_state.device_list
    vlan_id = st.session_state.vlan_id
    location = st.session_state.namespace

    if selected_switches and vlan_id != 1:

        # Add a generate button (for future functionality)
        if st.button("Verify Configuration"):

            st.header("Configuration Report")
            header_summary = generate_report(selected_switches, vlan_id)
            st.markdown(header_summary)

            rpt_dict = dict()

            rpt_dict.update({"timestamp": human_readable})
            rpt_dict.update({"vlan_id": vlan_id})
            rpt_dict.update({"location": location})

            vlan_configured_bool = True
            stp_root_bool = True

            sw_missing_vlan_list = list()
            stp_problem_list = list()

            for sw in selected_switches:
                # Check to see if the vlan is configured on each switch
                vlan_on_sw, vlan_resp = utils.find_vlan_on_switch(vlan_id, sw)

                if vlan_resp.ok:
                    if vlan_on_sw:
                        st.write(f"Vlan {vlan_id} Configured on Switch {sw}")
                    else:
                        st.write(f"Vlan {vlan_id} NOT on Switch {sw}")
                        vlan_configured_bool = False
                        sw_missing_vlan_list.append(sw)
                    # Saving the response so we hae a local copy of the data, just in case
                    if vlan_resp.json():
                        utils.save_json_payload(vlan_resp.json(), "vlan_response_from_suzieq.json")

                # Check to see if the vlan is participating in spanning tree
                stp_root_on_sw_bool, stp_resp = utils.check_stp_switch(vlan_id, sw)

                if stp_resp.ok:

                    df = pd.DataFrame(stp_resp.json())
                    if stp_root_on_sw_bool:
                        st.write(f"Vlan {vlan_id} participating in STP and has root {sw}")
                    else:
                        st.write(f"Vlan {vlan_id} STP has no root on {sw}")
                        stp_root_bool = False
                        stp_problem_list.append(sw)
                    st.write(df)

                    # Saving the response so we hae a local copy of the data, just in case
                    if stp_resp.json():
                        utils.save_json_payload(vlan_resp.json(), "stp_response_from_suzieq.json")

            if vlan_configured_bool:
                msg = f":thumbsup: Vlan {vlan_id} is configured on all switches!"
                st.success(msg)
            else:
                msg = f":thumbsdown: CONFIGURATION is INCOMPLETE.  {len(sw_missing_vlan_list)} switch(s) missing vlan {vlan_id}"
                st.error(msg)
                for sw in sw_missing_vlan_list:
                    st.write(f"- {sw}")
            rpt_dict.update({"vlan_cfg": msg})

            if stp_root_bool:
                msg = f":thumbsup: Vlan {vlan_id} has root on all switches!"
                st.success(msg)
            else:
                # TODO: Check to see if it IS the root!
                msg = f":thumbsdown: STP ERROR.  {len(stp_problem_list)} switch(s) without STP root on vlan {vlan_id}"
                st.error(msg)
                for sw in stp_problem_list:
                    st.write(f"- {sw}")
            rpt_dict.update({"stp_root": msg})
            # TODO: Check to see if the vlan name is per guideline (has the subnet)

            rpt_dict.update({"header_summary": header_summary})

            # Template stp_verification_template.j2
            # template = "stp_verification_template.j2"
            template = "other_template_var.j2"

            # Define the filename
            filename = (
                f"{st.session_state.namespace}_STP_Verification_{file_timestamp}.md"
            )
            # Create the full path to the new file
            verification_rpt_fp = os.path.join(os.getcwd(), filename)

            rendered = utils.render_in_one(template, rpt_dict)

            # Save the rendered content to the file
            utils.save_file(verification_rpt_fp, rendered)
            st.info(f"Saved Verification Markdown file to {verification_rpt_fp}")


if __name__ == "__main__":
    main()
