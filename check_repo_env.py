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

def suggest_fix():
    print()
    print("💡 Suggested fix:")
    print("   From the top-level repository directory, run:")
    print("     uv pip install -e .")
    print("   Make sure your pyproject.toml declares jinja2 as a dependency.")

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


def main():
    print("🔍 Checking repository environment...\n")
    check_python_version()
    check_virtualenv()
    check_jinja2()
    test_utils_import()


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' uv run check_repo_env.py' ")
    arguments = parser.parse_args()
    main()
