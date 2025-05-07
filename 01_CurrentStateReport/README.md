# Current State Report Mini Project

## Getting Started

This project will start to familiarize you with the overall repository environment as well as some lessons learned.

Please open the `gen_bgp_report.py` script in your favorite editor and lets get to work!

```python
% uv run gen_bgp_report.py -h
usage: gen_bgp_report.py [-h] [-t TITLE] [-l LOCATION]

Script Description

options:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        Add Custom Title to report. Default: BGP_Report
  -l LOCATION, --location LOCATION
                        Location Default: GDL Campus

Usage: ' python gen_bgp_report.py' or python gen_bgp_report.py -l 'AMS Campus'

```



Tiips:

The script uses the [diagrams](https://pypi.org/project/diagrams/) module which requires the Graphviz application to be installed on your system.

[Diagrams Getting Started > Installation](https://diagrams.mingrammer.com/docs/getting-started/installation)



## Overview

This Python script uses the Diagrams module and JSON output from SuzieQ 
to generate a state report on the BGP Sessions for a particular location.

The report is generated in Markdown using the bgp_report_md.j2 Jinja2 template 
which can be found in the templates subdirectory of the 01_CurrentStateReport directory.

The script will take the BGP state output found in `GDL_bgp.json` and process the data in order to answer some 
key questions and generate a diagram of the sessions.

This payload file,  `GDL_bgp.json`, was generated via the SuzieQ cli:

```
bgp show namespace=GDL_Campus format=json outfile="/home/claudia/GDL_bgp.json"
```

The Current State Report mini project illustrates how to turn a JSON data payload into a "current state report".

Specifically, we take the JSON output of a SuzieQ bgp show command and process the data in order to:

- Understand the location of the report data and develop an appropriate heading
- Note if all the sessions are up
- Note the number of BGP sessions configured
- Detail if the sessions are iBGP or eBGP (including count of each)
- Generate a diagram of the peering relationships with relevant attributes for each (name, vrf, ASN, state)
- Create a Markdown report for all of this information.

This project will also establish a pattern that will be used throughout the class.  A repository with a **templates** folder where all the relevant Jinja2 templates can be found.   

Putting all your templates in a ***templates*** directory is a good practice and all the other mini projects 
will follow this strategy.

This project also illustrates how passing each variable can become too complex.  

In this example, each piece of data is in a variable (location, bgp_list, etc.).  All the variables are passed to the template in the render step.

```
    # Render the template with the BGP data
    rendered_config = bgp_rpt_template.render(
        location="GDL Campus",
        bgp_list=data,
        all_peers_up=all_peers_up,
        ibgp_count=ibgp_count,
        ebgp_count=ebgp_count,
        drawing_filename=f"{drawing_filename}.{outformat}"
    )
```

The template references each of those variables directly.

Note the template variable in line 1 `{{ location }}` below which matches the `location='GDL Campus` passed in the render step (line 3 above).

```
# BGP Report for Location {{ location }}

Location {{ location }} has {{ bgp_list|length }} BPG Sessions

{% if all_peers_up %}
All BGP Peering Sessions are Up!
{% else %}
Not all of the BGP Peering Sessions are up!
{% endif %}

{% if ibgp_count %}
There are {{ ibgp_count }} IBGP Sessions.
{% else %}
There are no IBGP Sessions.
{% endif %}

{% if ebgp_count %}
There are {{ ebgp_count }} EBGP Sessions.
{% else %}
There are no EBGP Sessions.
{% endif %}

![Diagram of BGP Sessions]({{ drawing_filename }})

{# This is a comment
{% for line in bgp_list %}
{{ line }}
{% endfor %}
#}
```

This is not a bad way to start but eventually you will need to do more complex rendering and this strategy gets cumbersome quickly.

In other mini projects we will always send a dictionary or a list of dictionaries.


---
### Modules

- jinja2
- diagrams

Note:  The diagrams module requires the installation of the Graphviz application

[Diagrams Getting Started > Installation](https://diagrams.mingrammer.com/docs/getting-started/installation)

Native installation for Windows Users without a package manager
https://forum.graphviz.org/t/new-simplified-installation-procedure-on-windows/224

---

### Alternatives

This project works on a local JSON file.
For issues with `diagrams` and GraphViz, the JPG file under the working_example directory can be moved up a level and used.
Note: Comment out the graph generation code.

One option would be to extract BGP information from Suzieq via a REST call.

```bash
├── 01_CurrentStateReport
│   ├── GDL_bgp.json
│   ├── README.md
│   ├── gen_bgp_report_starter.py
│   ├── templates
│   │   └── bgp_report_md.j2
│   └── working_example
│       ├── GDL_Campus_BGP_Diagram.jpg
│       ├── GDL_Campus_BGP_REPORT.md
│       └── gen_bgp_report.py
```

