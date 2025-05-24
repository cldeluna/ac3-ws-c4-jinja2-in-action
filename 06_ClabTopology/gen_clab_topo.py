#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: gen_clab_topo.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "10/14/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"


import os
import re
import sys
import json
import zlib
import base64
import random
import argparse
import webbrowser
from logging import exception

# # This is necessary because I want to import functions in a file called utils.py and that file is one level up
# # from here
# # Get the absolute path of the top level main repository
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # Append the parent directory to sys.path so python searches that directory for the utils file
# sys.path.append(parent_dir)
# # Import the utils module (python script) one level up
# import utils

from utils import utils


def generate_topology(links):
    nodes = {}
    unique_links = set()

    for link in links:
        if not re.search("Management", link["ifname"]):
            for node in [link["hostname"], link["peerHostname"]]:
                if node not in nodes:
                    nodes[node] = {"kind": "ceos", "image": "ceos:latest"}
            unique_links.add(tuple(sorted([link["hostname"], link["peerHostname"]])))

    processed_links = []
    for i, (node1, node2) in enumerate(unique_links):
        processed_links.append(
            {"endpoints": [f"{node1}:eth{i + 1}", f"{node2}:eth{i + 1}"]}
        )

    return {"name": links[0]["namespace"], "nodes": nodes, "links": processed_links}


def yaml_to_mermaid(yaml_data, dir="TD"):
    mermaid_text = f"graph {dir};\n"

    # Define a custom sorting key function
    def sort_key(item):
        name = (
            item[0] if isinstance(item, tuple) else item["endpoints"][0].split(":")[0]
        )
        if "core" in name:
            return 0
        elif "dist" in name:
            return 1
        elif "acc" in name:
            return 2
        else:
            return 3

    # Sort nodes
    sorted_nodes = sorted(yaml_data["nodes"].items(), key=sort_key)

    # Add sorted nodes to the mermaid text
    for node, data in sorted_nodes:
        mermaid_text += f"    {node};\n"

    # Sort links
    sorted_links = sorted(yaml_data["links"], key=sort_key)

    # Add sorted links to the mermaid text
    for link in sorted_links:
        endpoints = link["endpoints"]
        e1 = endpoints[0].split(":")
        e2 = endpoints[1].split(":")
        mermaid_text += f"    {e1[0]} -->|{e1[1]} To {e2[1]}| {e2[0]};\n"

    return mermaid_text


def view_mermaid_diagram(mermaid_code: str) -> None:
    """
    Takes a Mermaid diagram code as input, pushes it to the Mermaid Live Editor API,
    and opens it in the default web browser.

    Args:
        mermaid_code (str): The Mermaid diagram code/payload

    Example:
        mermaid_code = '''
        graph TD
            A[Start] --> B[Process]
            B --> C[End]
        '''
        view_mermaid_diagram(mermaid_code)
    """
    # Create the JSON state object
    state = {
        "code": mermaid_code,
        "mermaid": {"theme": "default"},
        "updateEditor": True,
        "autoSync": True,
        "updateDiagram": True,
    }

    # Convert the state to JSON and encode it
    json_state = json.dumps(state)
    json_bytes = json_state.encode("utf-8")

    # Compress the JSON using zlib
    compressed = zlib.compress(json_bytes)

    # Encode the compressed data to base64
    base64_encoded = base64.urlsafe_b64encode(compressed).decode("utf-8")

    # Create the Mermaid Live Editor URL
    base_url = "https://mermaid.live/edit"
    full_url = f"{base_url}#pako:{base64_encoded}"

    # Open the URL in the default web browser
    webbrowser.open(full_url)

    return full_url


def main():
    """
    Generate a Containerlab topology from a SuzieQ LLDP output
    :return:
    """

    # Hate Digital Twins but can't deny there has to be a relationship
    rel_types = ["sis", "bro", "cuz"]
    random_rel = random.choice(rel_types)

    if arguments.local:
        local_filename = "topology_response_from_suzieq.json"
        print(f"\nUsing local file of SuzieQ BGP output payload: {local_filename}")
        payload = utils.load_json(local_filename)
    else:
        # Get topology for the provided namespace from SuzieQ REST

        try:
            response = utils.get_topology(arguments.namespace)

            if response.ok:
                # Saving the response so we hae a local copy of the data, just in case

                if response.json():
                    utils.save_json_payload(
                        response.json(),
                        f"topology_response_from_suzieq_{utils.file_timestamp()}.json",
                    )
            else:
                print(f"{response.status_code} Reason: {response.reason} ")
        except Exception as e:
            exit(
                f"\n\nAborting Run! Cannot access SuzieQ API! Status Code: "
                f"\nPlease make sure you have an .env file at the top level of your repository and a valid SuzieQ token in "
                f"the environment variable SQ_API_TOKEN. \n"
            )

        payload = response.json()

    # Generate the topology data using the local function generate_topology
    topology_data = generate_topology(payload)
    topology_data.update({"name": f"{arguments.namespace}_digital_{random_rel}"})

    # Render the Jinja2 template
    clab_topology = utils.render_in_one(
        "lldp_topology_template.j2", topology_data, search_dir="templates"
    )

    # Check to make sure the topology has data (nodes and links)
    if topology_data["nodes"] and topology_data["links"]:

        # Save the YAML topology to a file if we have node and link data
        filename = f"{arguments.namespace.lower()}_digital_{random_rel}.clab.yml"

        # Create output directory and set the full path
        topology_fp = utils.create_output_dir_fp(
            os.getcwd(), arguments.output_dir, filename
        )

        with open(topology_fp, "w") as f:
            f.write(clab_topology)

        print(
            f"\nContainerlab Topology file saved to {filename} in output directory:\n\t{topology_fp}\n"
        )
    else:
        print(
            "\nToplogy has no node or link data. Please review the topology links. Management0 interfaces are dropped"
        )
        print(topology_data)
        # Exit script. No sense in generating Mermaid content if the -g option was selected
        exit("Aborting Run\n")

    # Optional action to generate a Mermaid Graph of the topology
    if arguments.graph:

        print(
            "\nGenerating Mermaid Diagram! Your default browser should launch into the Mermaid Live Editor."
        )
        print("Tip: If the diagram does not appear, click the FULL SCREEN button.\n")

        # Generate Mermaid text from the updated YAML
        mermaid_code = yaml_to_mermaid(topology_data, dir="RL")

        # Generate the mermaid payload and open in local browser
        mermaid_url = view_mermaid_diagram(mermaid_code)
        print(
            "\nCopy this URL into your browser if your browser does not launch automatically.\n"
        )
        print(mermaid_url)
        print()


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description", epilog="Usage: ' python gen_clab_topo.py' "
    )

    parser.add_argument(
        "-g",
        "--graph",
        help="Graph the topology in Mermaid Live Editor. Default: False (do not graph)",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        help="output directory for containerlab topology file. Default is clab_topology_output",
        action="store",
        default="clab_topology_output",
    )

    parser.add_argument(
        "-n",
        "--namespace",
        help="Defines the namespace from which to pull topology data from SuzieQ. Default: 'GDL_Campus'",
        action="store",
        default="GDL_Campus",
    )

    parser.add_argument(
        "-l",
        "--local",
        help="Use local data file. Default: False",
        action="store_true",
        default=False,
    )

    arguments = parser.parse_args()
    main()
