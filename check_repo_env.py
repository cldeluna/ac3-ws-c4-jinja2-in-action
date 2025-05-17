#!/usr/bin/python -tt
# Project: ac3_templating_workshop
# Filename: check_repo_env.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/17/25"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import sys
import os
import shutil


def check_python_version():
    print("🐍 Python version in use:")
    print(f"   {sys.version}")
    print()

def check_virtualenv():
    print("✅ Virtual environment is currently set to:")
    print(f"   {sys.prefix}")
    print()

def check_jinja2():
    try:
        import jinja2
        print("✅ 'jinja2' module is available.")
        print(f"   Version: {jinja2.__version__}")
    except ImportError:
        print("❌ 'jinja2' is not installed in the current environment.")
        suggest_fix()

def suggest_fix(package_name):
    print()
    print(f"💡 Suggested fix for missing '{package_name}':")
    print("   From the top-level repository directory, run:")
    print("     uv pip install -e .")
    print(f"   Make sure your pyproject.toml includes '{package_name}' under [project.dependencies]")


def suggest_fix_utils():
    print()
    print("💡 Suggested fix for utils import:")
    print("   - Check that you're running this script from the top-level of the repo.")
    print("   - If you're using editable installs, run:")
    print("       uv pip install -e .")

def test_utils_import():
    print("\n🔧 Testing import from local 'utils' package...")

    try:
        import utils.utils  # Change to `import utils` if logic is in __init__.py
        print("✅ Successfully imported 'utils.utils'")
    except ModuleNotFoundError as e:
        print("❌ Failed to import 'utils.utils'")
        print(f"   Error: {e}")
        suggest_fix_utils()
    except Exception as e:
        print("❌ Import error in 'utils.utils'")
        print(f"   Error: {e}")
        suggest_fix_utils()


def check_ansible():
    print("\n🛠️ Checking for Ansible...")
    try:
        import ansible
        version = getattr(ansible, '__version__', 'unknown')
        print(f"✅ 'ansible' module is available. Version: {version}")
    except ImportError:
        print("❌ 'ansible' is not installed in the current environment.")
        suggest_fix("ansible")


def check_diagrams_and_graphviz():
    print("\n📊 Checking for 'diagrams' and 'graphviz' modules...")

    # Check Python package: diagrams
    try:
        import diagrams
        print("✅ 'diagrams' module is available.")
    except ImportError:
        print("❌ 'diagrams' is not installed.")
        suggest_fix("diagrams")

    # Check Python package: graphviz
    try:
        import graphviz
        print("✅ 'graphviz' module is available.")
    except ImportError:
        print("❌ 'graphviz' is not installed.")
        suggest_fix("graphviz")

    # Check system 'dot' command (optional but useful for rendering)
    dot_path = shutil.which("dot")
    if dot_path:
        print(f"✅ 'dot' command (Graphviz binary) found at: {dot_path}")
    else:
        print("⚠️  'dot' system binary not found in PATH. Rendering with 'diagrams' may fail.")
        print("   ➤ Visit https://graphviz.org/download/ to install it.")


def check_requests_and_people_in_space():
    print("\n🌐 Checking 'requests' module and space API...")

    try:
        import requests
        print("✅ 'requests' module is available.")
        url = "http://api.open-notify.org/astros.json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            num_people = data.get("number", "unknown")
            print(f"🚀 There are currently {num_people} people in space.")
        else:
            print(f"⚠️  Unable to fetch astronaut data. Status code: {response.status_code}")
    except ImportError:
        print("❌ 'requests' is not installed.")
        suggest_fix("requests")
    except Exception as e:
        print(f"⚠️  Error querying the people-in-space API: {e}")


def main():
    print("🔍 Checking repository environment...\n")
    check_python_version()
    check_virtualenv()
    check_jinja2()
    check_ansible()
    check_diagrams_and_graphviz()
    check_requests_and_people_in_space()
    test_utils_import()


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' uv run check_repo_env.py' ")
    arguments = parser.parse_args()
    main()
