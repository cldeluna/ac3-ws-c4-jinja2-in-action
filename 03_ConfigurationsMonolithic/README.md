# Configuration Templates Monolithic Style

The next two mini projects have a number of examples to showcase the different strategies.

- **Monolithic** <-- We are here
- Modular
  - Using Jinja2 Inheritance
  - Using Jinja2 Includes

## Monolithic

With the monolitic strategy, templates are define in their entirety based on 

- Vendor
- Function
- Region
- Hardware model
- Location type

This has a simplicity that is very attractive and easy to grasp conceptually as well as in code.
You have one master template for an access switch, a branch office switch, etc.  Some will have templates based on region, etc.  If you set up your templates and data with enough logic you can get rid of regional templates (strongly recommend).  The goal is to minimize (erradicate really) redundant data. Also know as DRY "Don't Repeat Yourself"!

Its a great place to start and lends itself to taking your current templates and "Jinjaizing" them.

In the monolitic example you will find a Python script which generates device configurations from the `new_switch.csv` file using the DNAC (aka Catalyst Center) base sample template which can be found (as ususal) in the templates directory.

```python
% tree
.
├── README.md
├── cfg_output
├── gen_monolithic_sw_cfg.py
├── new_switches.csv
└── templates
    ├── dnac_baseconfig_sampleJinjaTemplate.txt
    ├── dnac_baseconfig_sample_template.j2
    └── vendor
        └── cisco
            ├── aci
            ├── ios
            ├── ios-xe
            ├── ios-xr
            └── nxos

10 directories, 10 files
```

This introduces another common strategy, which you saw to some degree in the 02_Procedure mini project.  Bring in payload (REST, JSON, YAML, XLSX, CSV etc.) and then add key/value pairs.

In this case, we want to timestamp each template so we know when it was generated, so we calculate a human readable timestamp and add that key/value pair to our payload dictionary.

We bring in a temporary enable secret and add that to the payload.

We calculate the number of user interfaces based on the model number so we know how many interfaces to configure.

Full disclosure:  I've cheated here as this template assumes all the user interfaces are the same so the range command can be used.  In real life, you often have specific configurations, if only vlans, for each interface.

```bash
% uv run gen_monolithic_sw_cfg.py 

Generating configurations for switches in CSV file new_switches.csv

        Generating configuration for lax-asw01_20250521-052556.txt
        Generating configuration for lax-asw02_20250521-052556.txt
        Generating configuration for lax-asw03_20250521-052556.txt
        Generating configuration for lax-asw04_20250521-052556.txt

Saved files in /Users/claudiadeluna/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/python/2025/ac3_templating_workshop/03_ConfigurationsMonolithic/cfg_output

```



Use the `--help` option for more information about the command line arguments.

```python
% uv run gen_monolithic_sw_cfg.py --help
usage: gen_monolithic_sw_cfg.py [-h] [-p PAYLOAD_FILE] [-o OUTPUT_DIR] [-s SECRET_TEMP] [-t TIMEZONE]

Script Description

options:
  -h, --help            show this help message and exit
  -p PAYLOAD_FILE, --payload_file PAYLOAD_FILE
                        CSV Payload file to use Default is new_switches.csv
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        output directory for configuration files Default is cfg_output
  -s SECRET_TEMP, --secret_temp SECRET_TEMP
                        Temporary enable secret and login password
  -t TIMEZONE, --timezone TIMEZONE
                        Timezone defaults to America/Los_Angeles

Usage: ' python monolithic_sw_cfg.py or uv run monolithic_sw_cfg.py # Assumes a CSV file new_switches.csv with new switch payload'
```



