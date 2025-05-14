#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: template_env
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "8/31/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import jinja2
import utils


def jenv_filesystem(search_dir="templates"):
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

    ! Generally I leave this alone to default to {% %}  I like the unambiguity
    line_statement_prefix="",

    ! Error out if
    undefined=jinja2.runtime.StrictUndefined

    :param fp: the template directory path (relative or absolute)
    :return: the jinja2 environment object containing all the templates in the provided directory
    """

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(search_dir, encoding="utf-8"),
        line_comment_prefix="#",
        keep_trailing_newline=False,  # Default is False
        trim_blocks=True,  # Removes lines
        lstrip_blocks=True,
        undefined=jinja2.runtime.Undefined,  # Default is Undefined - undefined variables render as empty string
    )

    print(env)
    print(dir(env))
    print(env.list_templates())

    return env


def jenv_pkgloader(fp="ac2_templating_workshop"):
    """
    As you would expect, this requires a python package to be defined.
    :param fp:
    :return:
    """

    env = jinja2.Environment(loader=jinja2.PackageLoader(fp))

    print(env)
    print(dir(env))
    print(env.list_templates())

    return env


def jenv_string(template_string, template_vars):

    rendered_string_template = False

    rendered_string_template = (
        jinja2.Environment()
        .from_string(template_string)
        .render(template_vars=template_vars)
    )

    return rendered_string_template


def load_jtemplate(jenv_obj, template_file_name="test_list.j2"):
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
        print(f"ERROR: Template {fn} not found!")
        print(f"Available Templates in the Environment are:")
        for line in jenv_obj.list_templates():
            print(f"\t- {line}")
    except Exception as e:
        print(f"ERROR: {e}")

    return template_obj


def load_mydictvar():
    mydictvar = {
        "hostname": "switch01",
        "ip": "192.168.10.5",
        "mask": "255.255.255.0",
        "gw": "192.168.10.1",
        "vlans": [100, 200, 300, 400],
    }
    return mydictvar


def load_mylistvar():
    return [1, 2, 3, 4, 66, 78, 90]


def test_string_template():
    string_template = """
    ## String Template
            {{ template_vars }} 

            """

    mydictvar = load_mydictvar()
    rend_str = jenv_string(string_template, template_vars=mydictvar)

    print(rend_str)


def main():

    env_obj = jenv_filesystem()

    env_obj.add_extension("jinja2.ext.debug")

    # env_obj = jenv_pkgloader()

    # env = Environment(extensions=['jinja2.ext.debug'])

    """
    
    <Template 'test.j2'>
    
    dir(template_obj
    ['__annotations__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', 
    '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', 
    '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
    '__str__', '__subclasshook__', '__weakref__', '_debug_info', '_from_namespace', '_get_default_module', 
    '_get_default_module_async', '_module', '_uptodate', 'blocks', 'debug_info', 'environment', 'environment_class', 
    filename', 'from_code', 'from_module_dict', 'generate', 'generate_async', 'get_corresponding_lineno', 'globals', 
    'is_up_to_date', 'make_module', 'make_module_async', 'module', 'name', 'new_context', 'render', 'render_async', 
    'root_render_func', 'stream']

    """

    mylistvar = load_mylistvar()

    template_obj = load_jtemplate(env_obj, template_file_name="test_list.j2")

    if template_obj:
        print(template_obj)
        print(dir(template_obj))
        print(template_obj.filename)
        print(template_obj.environment)
        print(template_obj.debug_info)
        print(template_obj.blocks)
        print(template_obj.name)
        print(template_obj.new_context())
        print(template_obj.stream())
        print(template_obj.render(mylistvar=mylistvar))

    env_obj.tests["usr_intf"] = utils.is_user_intf

    template_obj = load_jtemplate(env_obj, template_file_name="test_tests.j2")
    rendered = template_obj.render(val="TwoGigabitEthernet1/0/23")
    print(rendered)

    # Filters

    # For Loops

    template_obj = load_jtemplate(env_obj, template_file_name="control_structures.j2")

    rendered = template_obj.render(intf_list=["TwoGigabitEthernet1/0/23"], maxstack="0")
    print(rendered)


# Standard call to the main() function.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script Description", epilog="Usage: ' python template_env' "
    )

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    # parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',default=False)
    arguments = parser.parse_args()
    main()
