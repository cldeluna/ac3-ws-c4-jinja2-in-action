#!/usr/bin/python -tt
# Project: ac2_templating_workshop
# Filename: data_woodchipper
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "10/6/24"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"


import os
import re
import yaml
import json
import jinja2
import random
import pathlib
import textwrap
import pprint
import pandas as pd
import solara
from solara.components.file_drop import FileInfo


# Declare reactive variables at the top level. Components using these variables
# will be re-executed when their values change.

data = solara.reactive("")
filename = solara.reactive("")
template_string = solara.reactive("")
rendered_string = solara.reactive("")
variable_name_input = solara.reactive("")


# Defining locally because we have not introduced the utils import strategy yet
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


def validate_variable_name(name):
    # Check if the name is a valid Python identifier
    pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
    return bool(pattern.match(name))


@solara.component
def PythonVariableInput(DEFAULT_VARIABLE_NAME):
    variable_name, set_variable_name = solara.use_state(DEFAULT_VARIABLE_NAME)
    is_valid, set_is_valid = solara.use_state(True)
    show_details = solara.use_reactive(False)

    def handle_input(value):
        set_variable_name(value)
        set_is_valid(validate_variable_name(value))

    solara.InputText(
        label="Enter a valid Python variable name used to store the data in the selected file",
        value=variable_name,
        on_value=handle_input,
        error=not is_valid,
        continuous_update=True,
    )

    if not is_valid:
        solara.Error(
            "Invalid variable name. Please use only letters, numbers, and underscores, and start with a letter or underscore."
        )
    elif variable_name:
        solara.Success(f"Valid variable name: {variable_name}")

    def toggle_details():
        show_details.value = not show_details.value

    solara.Button("Toggle Details", on_click=toggle_details)

    if variable_name and not show_details.value:
        solara.Markdown(
            f"""
        You can use this variable in your Python script like this:
        ```python
        {variable_name} = "All the data in the selected file"
        print({variable_name})
        
        ```
        """
        )

        # Jinja2 template example
        jinja2_template = jinja2.Template(
            """

        This is a Jinja2 template using the data in the variable you provided.
        
        You can use it like this in your template:

        {% raw %}
        {{ loaded_data }}
        {% endraw %}
        """
        )

        rendered_template = jinja2_template.render(loaded_data=variable_name)

        solara.Markdown(
            f"""
        You can send the data in your variable **{variable_name}** to a template for rendering.
        
        In this example the j2 template itself uses the variable "loaded_data".
        
        You are passing the data in **{variable_name}** to the variable "loaded_data" in the template.
        ```python
        
        template.render(loaded_data={variable_name})

        ```
        
        """
        )

        solara.Markdown(
            f"""
        ```python
        {rendered_template}
        ```
        """
        )

        # solara.Text(rendered_template)

        variable_name_input.set(variable_name)


@solara.component
def FilePicker(on_pick):
    current_dir = solara.use_reactive(pathlib.Path.cwd())

    def on_file_open(path):
        on_pick(str(path))

    solara.FileBrowser(
        directory=current_dir, on_file_open=on_file_open, can_select=False
    )


@solara.component
def FileDrop():
    content, set_content = solara.use_state(b"")
    filename, set_filename = solara.use_state("")
    size, set_size = solara.use_state(0)

    def on_file(f: FileInfo):
        set_filename(f["name"])
        set_size(f["size"])
        set_content(f["file_obj"].read(100))

    solara.FileDrop(
        label="Drag and drop a file here to read the first 100 bytes.",
        on_file=on_file,
        lazy=True,  # We will only read the first 100 bytes
    )
    if content:
        solara.Info(f"File {filename} has total length: {size}\n, first 100 bytes:")
        solara.Preformatted("\n".join(textwrap.wrap(repr(content))))


@solara.component
def SaveToFile():
    text = template_string.value

    def save_to_file():
        with open("sample_template.j2", "w") as file:
            file.write(text)

    # solara.InputText(label="Enter text", value=text)
    solara.Button("Save to file", on_click=save_to_file)


@solara.component
def SaveRenderedToFile():
    text = rendered_string.value

    def save_to_file():
        with open("rendered_template.txt", "w") as file:
            file.write(text)

    # solara.InputText(label="Enter text", value=text)
    solara.Button("Save to file", on_click=save_to_file)


@solara.component
def StateDisplay():
    """
    Utility to display state for troubleshooting
    :return:
    """
    solara.Markdown("## Current State Values")
    solara.Markdown(f"**data:** {data.value}")


def FileLoadPage():
    selected_file, set_selected_file = solara.use_state(None)
    file_content, set_file_content = solara.use_state(None)

    def get_files():
        data_dir_fp = os.path.join(os.getcwd(), "sample_data_structures")
        allowed_extensions = (".json", ".csv", ".yaml", ".yml")
        return [
            f for f in os.listdir(data_dir_fp) if f.lower().endswith(allowed_extensions)
        ]

    def load_file(file_name):
        filename.set(file_name)
        file_fp = os.path.join(os.getcwd(), "sample_data_structures", file_name)
        set_selected_file(file_fp)
        file_extension = os.path.splitext(file_name)[1].lower()

        try:
            if file_extension == ".csv":
                solara.Text("File is CSV")
                df = pd.read_csv(file_fp)
                set_file_content(df)
            elif file_extension == ".json":
                solara.Text("File is JSON")
                with open(file_fp, "r") as f:
                    data = json.load(f)
                set_file_content(data)
            elif file_extension in (".yaml", ".yml"):
                solara.Text("File is YAML")
                with open(file_fp, "r") as f:
                    data = yaml.safe_load(f)
                set_file_content(data)
        except Exception as e:
            set_file_content(f"Error loading file: {str(e)}")

    solara.Markdown("## File Load Page")

    solara.Markdown("### Available Files")
    for file in sorted(get_files(), key=len):
        solara.Button(file, on_click=lambda f=file: load_file(f))

    if selected_file:
        solara.Markdown(f"### Selected File: {filename.value}")

        if isinstance(file_content, pd.DataFrame):
            solara.DataFrame(file_content)
        elif isinstance(file_content, (dict, list)):
            solara.Markdown("```json\n" + json.dumps(file_content, indent=2) + "\n```", style="max-height: 200px; overflow-y: auto;")
        else:
            solara.Markdown(str(file_content), style="max-height: 200px; overflow-y: auto;")

        if set_file_content:
            data.set(file_content)


@solara.component
def Page():
    """
    Main Function of the script which defines the areas of the web App
    - Left pane (sidebar)
    - Center column for file selection
    - Center variable input

    :return:
    """

    with solara.Sidebar():
        solara.Markdown("# Data Structure Wood Chipper ☀️")

        image_folder_fp = os.path.join(os.getcwd(), "images")
        image_folder_path = pathlib.Path(image_folder_fp)
        png_files = list(image_folder_path.glob("*.png"))

        # Specify the path to your local image
        # image_file = "openart-image_5IOK-dXK_1728224733825_raw.png"
        image_file = random.choice(png_files)
        image_fp = os.path.join(os.getcwd(), "images", image_file)
        image_path = pathlib.Path(image_fp)

        # Display the image in the sidebar
        solara.Image(image_path, width="100%")

    with solara.Column():

        template_str = ""
        FileLoadPage()

        # used to display Solara state
        # StateDisplay()

        loaded_data = data.value

        if isinstance(loaded_data, pd.DataFrame):
            solara.Text("Matched Dataframe")
            if loaded_data.empty:
                there_is_data = False
            else:
                there_is_data = True
        elif loaded_data:
            there_is_data = True
        else:
            there_is_data = False

        if there_is_data:

            PythonVariableInput("loaded_data")
            variable_name = variable_name_input.value
            solara.Markdown("---")

            # Create two side-by-side areas
            with solara.Columns([1, 1]):
                # ----------------------------------------------------------------------------------------------------
                # First column
                with solara.Card("Data"):
                    solara.Markdown("---")
                    solara.Info("Data in File")

                    pretty_data = pprint.pformat(loaded_data, indent=2)
                    markdown_text = f"```python\n{pretty_data}\n```"

                    # If the data is a string create a Jinja2 template
                    if type(loaded_data) == str:
                        solara.Markdown(
                            f"Variable **{variable_name}** is of type 'String'<br>"
                        )
                        solara.Text(loaded_data)

                    # If its a list, iterate over the list elements
                    if type(loaded_data) == list:
                        solara.Markdown(
                            f"Variable **{variable_name}** is of type 'List'<br>"
                        )
                        # solara.Text(str(loaded_data))
                        solara.Markdown(markdown_text, style="max-height: 200px; overflow-y: auto;")

                    if type(loaded_data) == dict:
                        solara.Markdown(
                            f"Variable **{variable_name}** is of type 'Dict'<br>"
                        )
                        # solara.Text(str(loaded_data))
                        solara.Markdown(markdown_text, style="max-height: 200px; overflow-y: auto;")

                    if isinstance(loaded_data, pd.DataFrame):
                        solara.Markdown(
                            f"Variable **{variable_name}** is of type 'pd.DataFrame'<br>"
                        )
                        # solara.Text(str(loaded_data))
                        solara.Markdown(markdown_text)

                # ----------------------------------------------------------------------------------------------------
                # Second column
                with solara.Card("Jinja2 Template"):
                    solara.Markdown("---")
                    solara.Info("Jinja2 Template")

                    # If the data is a string create a Jinja2 template
                    if type(loaded_data) == str:
                        template_str = """
                        
Rendering a single variable passed to the template called "loaded data"

{{ loaded_data }}

                        """

                        # solara.Text(template_str)
                        solara.Markdown(f"```bash\n{template_str}\n```")

                    # If its a list, iterate over the list elements
                    if type(loaded_data) == list:
                        template_str = """

Raw data
{{ loaded_data }}

Iterating through list
{% for item in loaded_data %}
{{ item }}
{% endfor %}

                        """

                        template_str_wrongvar = """

Raw data
{{ someother_variable }}

Iterating through list
{% for item in someother_var %}
{{ item }}
{% endfor %}

                       """

                        # Display the template string
                        solara.Markdown(f"```bash\n{template_str}\n```")

                    if type(loaded_data) == dict:
                        template_str = """


Raw data
{{ loaded_data }}

Iterating through key, value pairs 
{% for key, value in loaded_data.items() %}
  KEY: {{ key }}
  VALUE: {{ value }}
                            
{% endfor %}

                        """

                        # Display the template string
                        solara.Markdown(f"```bash\n{template_str}\n```")

                    if isinstance(loaded_data, pd.DataFrame):
                        # Conver to list
                        converted_loaded_data = loaded_data.values.tolist()
                        lod = loaded_data.to_dict("records")
                        loaded_data = lod
                        template_str = """

Raw data
{{ loaded_data }}

Iterating through list (formerly a dataframe)
{% for item in loaded_data %}
{{ item }}
{% endfor %}

                        """

                        # print(converted_loaded_data)
                        # print(lod)

                        # Display the template string
                        solara.Markdown(f"```bash\n{template_str}\n```")

                    if template_str:
                        template_string.set(template_str)
                        SaveToFile()

            # Content below the side-by-side areas
            solara.Success("Rendered Template")

            template = jinja2.Template(template_str)
            rendered_output = template.render(loaded_data=loaded_data)

            rendered_string.set(rendered_output)

            # Display the rendered output
            solara.Markdown(f"```bash\n{rendered_output}\n```")

            SaveRenderedToFile()


# The following line is required only when running the code in a Jupyter notebook:
# Page()
