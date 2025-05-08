#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: utils
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "8/31/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import pprint
import re
import os
import csv
import yaml
import json

# import hvac # Used for Vault but not in final repo
import jinja2
import dotenv
import argparse
import datetime
import platform
import requests
import openpyxl
import ipaddress
import itertools

import pandas as pd

from diagrams import Diagram, Edge
from diagrams.generic.network import Router

# Disable  Unverified HTTPS request is being made to host messages
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)


def is_user_intf(intf):
    """
    Cisco centric interface test to see if an interface is a user interface
    (typically like 1/0/21) vs an uplink (typically like 1/1/1)
    :param intf:
    :return: boolean: true if it looks like a user interface per the pattern, false otherwise
    """

    if re.search(r".+\d\/0\/\d{1,2}", intf):
        return True
    else:
        return False


def load_json(filename):
    """
    Safely load a JSON file
    :param filename:
    :return:
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


def load_yaml(filename):
    """
    Load a YAML file safely
    :param filename:
    :return:
    """
    with open(filename, "r") as file:
        data = yaml.safe_load(file)

    return data


def load_csv(filename):
    """
    Given a path fo a file including filename, safely opens a CSV file and returns either None if it
    cannot open the file or returns the data in the file as a list (each element of the list is a row from
    the CSV file)
    :param filename: file to open
    :return: None or list
    """

    try:
        with open(filename, "r", encoding="utf-8-sig", newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            data = list(csv_reader)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def save_file(fn, text):
    """
    Simple funciton to save text to a file fn
    :param fn: filename or full path filename
    :param text:
    :return: fn
    """
    with open(fn, "w") as f:
        f.write(text)

    return fn


def save_json_payload(payload, filename):
    """
    Save a JSON payload to a file.

    Args:
    payload (dict): The JSON payload to be saved.
    filename (str): The name of the file to save the JSON payload to.

    Returns:
    None
    """
    try:
        with open(filename, "w") as json_file:
            json.dump(payload, json_file, indent=4)
        print(f"JSON payload successfully saved to {filename}")
    except IOError as e:
        print(f"Error writing to file: {e}")
    except json.JSONDecodeError as e:
        print(f"Error encoding JSON: {e}")


def check_and_create_directory(directory_path):
    """
    Simple function which check to see if a directory exists and if it does not it creates it
    :param directory_path:
    :return:
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return True
    return False


def lists_to_dicts(data):
    """
    Takes in a CSV file with a header row as the first row and one ore more 'data' rows and builds and returns
    a list of dictionaries
    :param data:
    :return:
    """
    headers = data[0]
    return [dict(zip(headers, row)) for row in data[1:]]


def jenv_filesystem(
    search_dir="templates", line_comment="##", ktn=False, lsb=False, tb=False
):
    """

    RECOMMENDED when getting started!
    This assumes that there is a directory called "templates" where all the Jinja Templates .j2 files are located.

    his will load templates from a directory in the file system (templates by default)

    env = jenv_filesystem()

    If, for example, you put your templates in a directory called jinja_temps you would call this function like so:

    env = jenv_filesystem(fp="jinja_temps")

    The path can be relative or absolute. Relative paths are relative to the current working directory.

    print(env)
    <jinja2.environment.Environment object at 0x105d730d0>

    dir(env)
    ['__annotations__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
    '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
    '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
    '__subclasshook__', '__weakref__', '_compile', '_filter_test_common', '_generate', '_load_template', '_parse',
    '_tokenize', 'add_extension', 'auto_reload', 'autoescape', 'block_end_string', 'block_start_string',
    'bytecode_cache', 'cache', 'call_filter', 'call_test', 'code_generator_class', 'comment_end_string',
    'comment_start_string', 'compile', 'compile_expression', 'compile_templates', 'concat', 'context_class',
    'extend', 'extensions', 'filters', 'finalize', 'from_string', 'get_or_select_template', 'get_template',
    'getattr', 'getitem', 'globals', 'handle_exception', 'is_async', 'iter_extensions', 'join_path',
    'keep_trailing_newline', 'lex', 'lexer', 'line_comment_prefix', 'line_statement_prefix', 'linked_to',
    'list_templates', 'loader', 'lstrip_blocks', 'make_globals', 'newline_sequence', 'optimized', 'overlay',
    'overlayed', 'parse', 'policies', 'preprocess', 'sandboxed', 'select_template', 'shared', 'template_class',
    'tests', 'trim_blocks', 'undefined', 'variable_end_string', 'variable_start_string']

    Enable Debugging
    # env = Environment(extensions=['jinja2.ext.debug'])

    ! line comment prefix sets the prefix for single-line comments
    Valid options are '//', '#', ';', '--', '##'
    Important notes:

    The line comment only works for single-line comments
    Everything after the prefix to the end of the line becomes a comment
    Block comments {# #} still work regardless of your line comment setting
    Choose a prefix that won't appear naturally in your template content
    The prefix must appear at the start of the line to be treated as a comment


    ! Generally I leave this alone to default to {% %}  I like the unambiguity
    line_statement_prefix="",

    ! Undefined default
    undefined=jinja2.runtime.Undefined
    -Silently evaluates to an undefined object
    -Printing it results in an empty string
    -Operations on it raise an UndefinedError

    ! Error out if
    undefined=jinja2.runtime.StrictUndefined (recommended)
    -Most strict option
    -Raises an UndefinedError immediately when you try to access any undefined variable
    -Good for development to catch missing variables early

    !For highly nested structures
    undefined=jinja2.runtime.ChainableUndefined
    -Allows you to chain attributes and items that return another undefined object
    -Only raises an error when you try to print or convert to a string
    U-seful when you have deeply nested structures

    ! Debugging undefined
    undefined=jinja2.runtime.DebugUndefined
    -Returns the name of the undefined variable as a string
    -Helpful for debugging templates
    -Won't raise errors, but makes it obvious what's missing

    ! Custom Undefined
    class CustomUndefined(Undefined):
        def _fail_with_undefined_error(self, *args, **kwargs):
            return f'[Missing: {self._undefined_name}]'

        __str__ = _fail_with_undefined_error

    undefined=jinja2.runtime.CustomUndefined

    -You can create your own undefined class
    -Useful for custom error handling or logging

    :param fp: the template directory path (relative or absolute)
    :return: the jinja2 environment object containing all the templates in the provided directory
    """

    valid_line_comment_prefixes = ["//", "#", ";", "--", "##", "=", "==", "!"]
    # In case an invalid or blank line comment is provided to the function
    if line_comment not in valid_line_comment_prefixes:
        line_comment = "##"

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(search_dir, encoding="utf-8"),
        line_comment_prefix=line_comment,  # Only works for single-line comments
        keep_trailing_newline=ktn,  # Default is False True preserve trailing newline in templates
        trim_blocks=tb,  # True remove first newline after a block Default is False
        lstrip_blocks=lsb,  # True remove leading spaces and tabs from block tags Default is False
        undefined=jinja2.runtime.Undefined,  # Default is Undefined - undefined variables render as empty string
    )

    return env


def load_jtemplate(jenv_obj, template_file_name):
    """
    This function takes two arguments:
    1. A Jinja2 Environment Object
    2. A Jinja2 Template Filename
    :param jenv_obj: Jinja2 Environment Object
    :param template_file_name: Jinja2 Template Filename
    :return: template_obj which will either be the requested template object or False
    """
    template_obj = False

    try:
        template_obj = jenv_obj.get_template(template_file_name)
    except jinja2.exceptions.TemplateNotFound as fn:
        print(f"ERROR: Template {template_file_name} not found!")
        print(f"Available Templates in the Environment are:")
        for line in jenv_obj.list_templates():
            if ".j2" in line:
                print(f"\t- {line}")
    except Exception as e:
        print(f"ERROR: {e}")

    return template_obj


def render_in_one(
    template_file_name, payload_dict, search_dir="templates", line_comment="!"
):
    """
    Inspired by:
    https://daniel.feldroy.com/posts/jinja2-quick-load-function

    This is the all-in-one version of the Jinja2 process
    1. Create environment (using the jenv_filesystem function)
    2. Load template (using the load_jtemplate function)
    3. Render template with data

    :return: rendered text as a string (class 'str')
    """

    valid_line_comment_prefixes = ["//", "#", ";", "--", "##", "=", "==", "!"]
    # In case an invalid or blank line comment is provided to the function
    if line_comment not in valid_line_comment_prefixes:
        line_comment = "##"

    jenv = jenv_filesystem(search_dir=search_dir, line_comment=line_comment)

    jtemplate = load_jtemplate(jenv, template_file_name=template_file_name)

    # The templates must use a variable called "payload_dict"
    return jtemplate.render(cfg=payload_dict)


def get_mask_from_cidr(cidr):
    """
    Given a subnet in cidr notation return the network mask in dotted notation
    :param cidr:
    :return:  mask in dotted notation
    """
    network = ipaddress.IPv4Network(cidr, strict=False)
    return str(network.netmask)


def get_first_ip(cidr):
    """
    Given a subnet in cidr notation return the first valid IP
    :param cidr:
    :return: First valid IP
    """
    network = ipaddress.IPv4Network(cidr, strict=False)
    first_ip = network.network_address + 1
    return str(first_ip)


def get_fourth_ip(cidr):
    """
    Given a subnet in cidr notation return the fourth valid IP
    Note: this should really just be one function which takes in the offset from the network
    :param cidr:
    :return:
    """
    network = ipaddress.IPv4Network(cidr, strict=False)
    fourth_ip = next(itertools.islice(network.hosts(), 3, 4), None)
    return str(fourth_ip) if fourth_ip else None


def add_business_days(start_date, business_days):
    """
    This helper function takes a start date and the number of business days to add. It iterates through the calendar,
    skipping weekends, until it has counted the specified number of business days.

    :param start_date:
    :param business_days:
    :return:
    """
    end_date = start_date
    while business_days > 0:
        end_date += datetime.timedelta(days=1)
        if end_date.weekday() < 5:  # Monday to Friday are 0 to 4
            business_days -= 1
    return end_date


def calculate_future_business_date(business_days):
    """
    This is the main function that uses today's date as the starting point and calls add_business_days
    to calculate the future date.

    To use this function, simply call calculate_future_business_date with the number of business days
    you want to add to today's date. For example:

    ** perplexity
    :param business_days:
    :return:
    """
    today = datetime.date.today()
    return add_business_days(today, business_days)


def create_std_cr_snow(snow_dict):
    """
    Example of function using Vault for SNOW creds
    :param snow_dict:
    :return:
    """

    VAULT_ADDR = "http://127.0.0.1:8200"
    ROOT_TOKEN = "hvs.SR1x9c4pdbFFxr2L6BjxBJL9"

    # ServiceNow instance details
    username, password, snow_instance = get_secret(VAULT_ADDR, ROOT_TOKEN)

    pprint.pp(snow_dict)

    template = "b9c8d15147810200e90d87e8dee490f6"

    # API endpoint
    url = f"https://{snow_instance}/api/now/table/change_request"

    # Headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Payload (adjust fields as needed)
    payload = {
        "short_description": snow_dict["short_desc"],
        "template": template,  # Sys ID of the template you want to use
        "description": snow_dict["desc"],
        "test_plan": snow_dict["test_plan"],
        "justification": snow_dict["justification"],
        "implementation_plan": snow_dict["implementation_plan"],
        "risk_impact_analysis": snow_dict["risk_impact_analysis"],
        "backout_plan": snow_dict["backout_plan"],
        # "work_notes": "These are my work notes",
        # Add other fields as required
    }

    # Send POST request
    response = requests.post(
        url, auth=(username, password), headers=headers, data=json.dumps(payload)
    )

    # Check response
    if response.status_code == 201:
        print("Standard Change Request created successfully")
        # pprint.pprint(response.json())
    else:
        print(f"Error creating Standard Change Request: {response.status_code}")
        # print(response.text)

    return response


# Hashicorp Local Vault
def get_secret(URL, ROOT_TOKEN, PATH="dev_snow/config"):
    """
    Note: not used in repo currently
    Function to extract secrets from a local dev Vault instance
    :param URL:  Vault URL
    :param ROOT_TOKEN:  Vault Root Toke
    :param PATH: Secret path
    :return: username, password, instance
    """

    # Create a client instance
    client = hvac.Client(url=URL, token=ROOT_TOKEN)

    # Check if client is authenticated
    if client.is_authenticated():
        # Read the secret
        secret = client.secrets.kv.v2.read_secret_version(path=PATH)

        # Extract username and password
        username = secret["data"]["data"]["username"]
        password = secret["data"]["data"]["password"]
        instance = secret["data"]["data"]["instance"]

        return username, password, instance
    else:
        raise Exception("Vault authentication failed")


def get_username():
    """
    Cross os function to get username from Mac OSX, Windows, and Linux.
    If can't get from ENV VAR looks at home directory.
    :return:  system username
    """
    system = platform.system().lower()

    if system == "darwin" or system == "linux":
        return os.environ.get("USER")
    elif system == "windows":
        return os.environ.get("USERNAME")
    else:
        return os.path.expanduser("~").split(os.sep)[-1]


def replace_special_chars(text):
    """
    eplace spaces and special characters in the provided text string with underscores
    :param text:
    :return: string with underscores replacing anything that is not alphanumeric.
    """

    return re.sub(r"[^a-zA-Z0-9]", "_", text)


def set_os_env(var_name, var_value):
    """
    Sets an environment variable using the Python built in os module

    :param var_name:
    :param var_value:
    :return:
    """
    os.environ[var_name] = var_value


def get_os_env(var_name):
    """
    Returns the requested environment variable
    :param var_name: the environment variable to fetch from memory
    :return: the variable or blank string
    """

    try:
        return os.environ[var_name]
    except:
        return ""


def try_sq_rest_call(uri_path, url_options, debug=False):
    """
    REUSABLE BASE SuzieQ API REST Call
    :param uri_path:
    :param url_options:
    :param debug:
    :return:  complete response
    """

    # Load Environment variables from .env containing Suzieq REST API Token
    dotenv.load_dotenv()

    API_ACCESS_TOKEN = os.getenv("SQ_API_TOKEN")
    API_ENDPOINT = "ac2-suzieq.cloudmylab.net"

    url = f"https://{API_ENDPOINT}:8443{uri_path}?{url_options}"

    payload = "\r\n"
    headers = {
        "Content-Type": "text/plain",
        "Authorization": f"Bearer {API_ACCESS_TOKEN}",
    }

    if debug:
        print(f"URL is {url}")

    # Send API request, return as JSON
    response = dict()
    try:
        # response = requests.get(url).json()
        response = requests.get(url, headers=headers, data=payload, verify=False)

    except Exception as e:
        print(e)
        print(
            "Connection to SuzieQ REST API Failed.  Please confirm the REST API is running!"
        )
        print(e)
        # st.stop()
        response = False

    if debug:
        print(f"Response is {response}")
        if response.json():
            print(response.json())
        else:
            print("No data returned for REST call")

    # Returns full response object
    return response


def get_namespace_list():
    """
    This function pulls all the namespaces available in SuzieQ.
    :return: a list of the namesapces and the full response
    """

    # Initialize
    namespace_list = list()

    # Trick to get a unique list of namespaces for the pull down
    URI_PATH = "/api/v2/device/unique"
    URL_OPTIONS = f"columns=namespace&ignore_neverpoll=true"
    ns_response = try_sq_rest_call(URI_PATH, URL_OPTIONS)

    # Create a list of namespaces from the list of dictionaries
    if ns_response.status_code == 200:
        if ns_response.json():
            namespace_list = [line["namespace"] for line in ns_response.json()]
    else:
        print(f"Problem with accessing SuzieQ REST API")
        print(f"OK Response: {ns_response.ok}")
        print(f"Status Code: {ns_response.status_code}")
        print(f"Reason: {ns_response.reason}")
        print(ns_response.json())
        print(
            "Please make sure you have a .env file (rename the .env_sample) at the root of the repository "
            "with the correct API Token."
        )
        print("Token can be obtained from any of the instructors.")

    return namespace_list, ns_response


def get_device_list(nsx):
    """
    This function pulls the device data for a namespace in SuzieQ.
    :param nsx:
    :return: a list of the devices in the namespace and the complete response
    """

    # Initialize
    device_list = list()

    # Get unique list of devices in the given namespace
    URI_PATH = "/api/v2/device/unique"
    URL_OPTIONS = f"namespace={nsx}&columns=hostname&ignore_neverpoll=true"
    response = try_sq_rest_call(URI_PATH, URL_OPTIONS, debug=False)

    # Create a list of namespaces from the list of dictionaries
    if response.status_code == 200:
        if response.json():
            device_list = [line["hostname"] for line in response.json()]
    else:
        print(f"Problem with accessing SuzieQ REST API")
        print(f"OK Response: {response.ok}")
        print(f"Status Code: {response.status_code}")
        print(f"Reason: {response.reason}")
        print(response.json())
        exit("Aborting Run! Check credentials.")

    return device_list, response


def get_topology(namespace, via="lldp"):
    """
    This function pulls the LLDP topology data for a namespace in SuzieQ.

    :param namespace:
    :param via:
    :return: the complete API response
    """

    URI_PATH = "/api/v2/topology/show"
    URL_OPTIONS = (
        f"view=latest&namespace={namespace}&columns=default&via={via}&reverse=false"
    )

    # https://172.16.14.4:8443/api/v2/topology/show?view=latest&namespace=GDL_Campus&columns=default&via=lldp&reverse=false

    response = try_sq_rest_call(URI_PATH, URL_OPTIONS, debug=False)

    # Create a list of namespaces from the list of dictionaries
    if response.status_code == 200:
        pass
        # if response.json():
        # print(response.json())
    else:
        print(f"Problem with accessing SuzieQ REST API")
        print(f"OK Response: {response.ok}")
        print(f"Status Code: {response.status_code}")
        print(f"Reason: {response.reason}")
        print(response.json())
        exit("Aborting Run! Check credentials.")

    return response


def extract_numeric_portion(interface):
    """
    Used in the Containerlab topology build to extract the numeric portion of an interface

    :param interface:
    :return:
    """

    match = re.search(r"\d+(?:/\d+)*$", interface)
    if match:
        return match.group(0)
    return None


# ------------------ SUZIEQ EXTERNAL DB TABLE API CALLS --------------------------------
def check_critical_vlan(vlanx, nsx, debug=False):
    """
    Check that a given vlanx is not in the critical_vlan extdb.
    If it is a critical vlan then it cannot be changed via self-service.

    Return True if it is a critical vlan and False if not

    """

    # https://server.uwaco.com:8443/api/v2/extdb/show?ext_table=critical_vlans&view=latest&namespace=GDL_Campus
    # &columns=default&reverse=false&include_deleted=false&show_exceptions=false

    URI_PATH = "/api/v2/extdb/show"

    URL_OPTIONS = f"ext_table=critical_vlans&view=latest&namespace={nsx}&columns=default&reverse=false&include_deleted=false&show_exceptions=false"

    # Send API request, return as JSON
    sq_api_response = try_sq_rest_call(URI_PATH, URL_OPTIONS, debug=debug)
    if debug:
        print(f"check_critical_vlan passed {vlanx} and namespace {nsx}")
        print(URI_PATH)
        print(URL_OPTIONS)

    return sq_api_response


def get_extdb(extdbx, nsx, debug=False):
    """
    This function pulls the data from the given namespace in the given external db table

    :param extdb:
    :param nsx:
    :param debug:
    :return: the response dictionary including the .json() data
    """

    # https://server.uwaco.com:8443/api/v2/extdb/show?ext_table=critical_vlans&view=latest&namespace=1420_Dubai
    # &columns=default&reverse=false&include_deleted=false&show_exceptions=false

    URI_PATH = "/api/v2/extdb/show"

    URL_OPTIONS = f"ext_table={extdbx}&view=latest&namespace={nsx}&columns=default&reverse=false&include_deleted=false&show_exceptions=false"

    # Send API request, return as JSON
    sq_api_response = try_sq_rest_call(URI_PATH, URL_OPTIONS, debug=debug)
    if debug:
        print(URI_PATH)
        print(URL_OPTIONS)

    return sq_api_response


def find_vlan_on_switch(vlanx, switchx):
    """
    Call to SuzieQ Vlan how for a switch and vlan.

    :param vlanx:
    :param switchx:
    :return: a boolean indicating true if the vlan is configured on the switch and false otherwise,
             and the complete API response
    """
    vlan_configured_on_sw = False

    URI_PATH = "/api/v2/vlan/show"
    URL_OPTIONS = f"hostname={switchx}&view=latest&columns=default&vlan={vlanx}"

    sq_api_response = try_sq_rest_call(URI_PATH, URL_OPTIONS, debug=False)

    if not re.search("NOT FOUND", switchx):
        if sq_api_response.json():
            vlan_configured_on_sw = True
        else:
            pass
            # print(f"Vlan {vlanx} is NOT configured on switch {switchx}")
    else:
        pass
        # print("Switch is NOT FOUND")

    return vlan_configured_on_sw, sq_api_response


def check_stp_switch(vlanx, switch):
    """
    Call to SuzieQ STP show for a switch and vlan.

    :param vlanx:
    :param switch:
    :return: a boolean indicating true if the vlan has root on the switch and false otherwise,
             and the complete API response
    """

    # Set Boolean indicating the provided vlan has root on an interface
    vlan_has_stp_root = False

    URI_PATH = "/api/v2/stp/show"
    URL_OPTIONS = f"hostname={switch}&view=latest&columns=default&vlan={vlanx}&portType=network&reverse=false&include_deleted=false"

    sq_api_response = try_sq_rest_call(URI_PATH, URL_OPTIONS, debug=False)

    response_json = sq_api_response.json()

    if not re.search("NOT FOUND", switch):
        if sq_api_response.ok:
            for line in response_json:
                if line["portRole"] == "root":
                    vlan_has_stp_root = True
                    break

    return vlan_has_stp_root, sq_api_response


def file_timestamp(dat_tim_delim="-"):
    """
    Returns the current time in a format suitable for file timestamps
    :return:
    """
    return datetime.datetime.now().strftime(f"%Y%m%d{dat_tim_delim}%H%M%S")


def human_readable_timestamp():
    """
    Returns the current time in a human readable format suitable for documentation
    :return:
    """
    return datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")


def extract_excel_to_csv(file_path):
    """
    Function which takes in an EXCEL file with one or more tabs and extracts each tab into a CSV.
    Used to extract the design data for the 08 Capstone project.

    :param file_path:
    :return:
    """

    # Load the workbook
    workbook = openpyxl.load_workbook(file_path)

    # Get the current timestamp
    timestamp = file_timestamp(dat_tim_delim="_")

    # Create a directory to save CSVs if it doesn't exist
    os.makedirs("csv_outputs", exist_ok=True)

    # Iterate over each sheet in the workbook
    for sheet_name in workbook.sheetnames:
        # Read the data from the sheet
        sheet = workbook[sheet_name]
        data = list(sheet.values)

        # Convert to a DataFrame, using the first row as column names
        df = pd.DataFrame(data[1:], columns=data[0])

        # Save the DataFrame to a CSV file with a timestamp
        csv_file_name = f"csv_outputs/{sheet_name}_{timestamp}.csv"
        df.to_csv(csv_file_name, index=False)
        print(f"Saved {csv_file_name}")


def high_level_design_diagram():
    """
    Used to generate a "dummy" diagram for the 08 Design Document
    Note: Not part of the venv for the repot by default
    import matplotlib.pyplot as plt
    import networkx as nx
    :return:
    """
    # Create a directory named 'images' if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Create a basic network topology graph
    G = nx.Graph()

    # Adding nodes (representing devices)
    devices = ["Router", "Switch1", "Switch2", "Server", "PC1", "PC2", "Laptop"]
    G.add_nodes_from(devices)

    # Adding edges (representing connections)
    edges = [
        ("Router", "Switch1"),
        ("Router", "Switch2"),
        ("Switch1", "Server"),
        ("Switch1", "PC1"),
        ("Switch2", "PC2"),
        ("Switch2", "Laptop"),
    ]
    G.add_edges_from(edges)

    # Position nodes using a spring layout
    pos = nx.spring_layout(G)

    # Draw the nodes and edges
    plt.figure(figsize=(10, 7))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="skyblue",
        node_size=3000,
        font_size=12,
        font_weight="bold",
        edge_color="gray",
    )

    # Set title
    plt.title("General Network Topology")

    # Save the image in the 'images' directory
    plt.savefig("high_level_design.jpg", format="jpg", bbox_inches="tight")
    plt.close()


def create_bgp_diagram(bgp_sessions, filename="bgp_sessions", outformat="png"):
    """
    Given a list of dictionaries in bgp_sessions with local and peer information, draw a diagram which
    shows each peering session including state and ASN
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


def get_template_selection(options):
    """
    Example Only - Currently Not Used
    Function to enumerate templates in the templates directory for interactive user selection
    :param options:
    :return: selected template
    """
    # Display numbered options
    for index, item in enumerate(options, start=1):
        print(f"{index}. {item}")

    # Get user input and validate
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def get_neo_data(start_date=None, end_date=None, api_key="YOUR_API_KEY"):
    """
    A python function which extracts near earth orbit objects from a nasa data set
    nd returns a JSON file with near earth objects for today's date

    Requires an API Key available for free at the URL below:
    https://api.nasa.gov/

    :param start_date:
    :param end_date:
    :param api_key:
    :return:
    """
    # If no dates provided, use today's date
    if not start_date:
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if not end_date:
        end_date = start_date

    # NASA NeoWs API endpoint
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}"

    # Make the API request
    response = requests.get(url)

    print(f"\nLooking at the NEO database for date range: {start_date} to {end_date}\n")

    if response.status_code == 200:
        data = response.json()

        # Write the data to a JSON file
        filename = f"nasa_near_earth_objects_{file_timestamp()}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"NEO data saved to {filename}")
        return data
    else:
        print(f"Error: Unable to retrieve data. Status code: {response.status_code}")
        return None


def json_to_yaml(input_json_file, output_yaml_file):
    """
    Function which reads in a JSON file and saves it as YAML
    :param input_json_file:
    :param output_yaml_file:
    :return:
    """
    # Read the JSON file
    with open(input_json_file, "r") as json_file:
        json_data = json.load(json_file)

    # Write the data to a YAML file
    with open(output_yaml_file, "w") as yaml_file:
        yaml.dump(json_data, yaml_file, default_flow_style=False)

    print(f"\nSuccessfully converted {input_json_file} to {output_yaml_file}\n")


def sort_filenames_by_length(filenames):
    """
    Sort a list of filenames based on their length in ascending order.

    Args:
    filenames (list): A list of filename strings

    Returns:
    list: A new list of filenames sorted by their length
    """
    return sorted(filenames, key=len)


def main():
    print(
        "\nThis script contains commonly used functions and is intended to serve as a utility module for other "
        "scripts in the repository."
    )
    print("It is not intended to be executed directly.\n")

    # neodata = get_neo_data(api_key="")
    #
    # neo_dict = dict()
    # for list in neodata['near_earth_objects']['2024-11-15']:
    #     # print(list)
    #     neo_dict.update({list['id']:
    #         {"id": list['id'],
    #         "name": list['name'],
    #         "est_max_diameter_m": list['estimated_diameter']['meters']['estimated_diameter_max'],
    #         "is_ele": list['is_potentially_hazardous_asteroid'],  # Extintion level event,
    #         "jpl_url": list['nasa_jpl_url'],
    #         },
    #     })
    #
    # pprint.pprint(neo_dict)
    #
    # save_json_payload(neo_dict, "json_nasa_near_earth_objects_dict.json")
    # json_to_yaml("json_nasa_near_earth_objects_dict.json", "yaml_nasa_near_earth_objects_dict.yml")


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description", epilog="Usage: import utils "
    )
    arguments = parser.parse_args()
    main()
