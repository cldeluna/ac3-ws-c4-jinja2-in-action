# Data Structure Woodchipper

The goal of this mini project is to look at different data structures and how they can be 
- passed into a template, and
- decomposed 

within a Jinja2 Template.

The solara module is used to present the information via a web interface which can be run locally 
on the student's laptop.

In the examples, by default, all payload is loaded into a variable named `loaded_data` which can be changed.
This variable in the python script can be a: 

- a string 
- a list
- a dictionary
- a complex data structure (list of dictionaries, dictionary of values including lists and dictionaries, etc.)

The data_woodchipper.py App illustrates data structures and their display in corresponding Jinja2 templates.

### Starting the App
Change into the 00_DataStructureChipper directory.
```bash
solara run data_woodchipper.py
```

When the web page comes up, a list of available files comes up.  These files contain various types of data structures.

Click on one of the buttons to select that type of file (CSV, JSON, YAML).  These are common file-based payload formats.

Once a file of data has been selected, the App will allow you to pick a variable name for the data.

Then the App will illustrate how the data in the file, which is now in the variable you defined gets 
passed to the variable used in the template.

The right side of the center pane will show the data itself and its type.
The left side of the center pane will show the corresponding template derived from the data type.
The bottom part of the center pane will show the rendered template.

---

#### Modules 
- jinja2
- solara
- pandas
- solara