# Procedure/Work Instructions Mini Project

## Getting Started

This mini project introduces some common strategies in templating.

- YAML Payload file 
  - Yes, you saw a local JSON payload in the Current State Report but this was extracted from a system.  Here we show a YAML file of "installation details".  We use YAML because it allows for comments.
  - In subsequent projects in this repository we will be extracting our "details" via API but sometimes that is not possible and a local YAML or JSON is a handy way to store these details and keep them under revision control!
  - We will use SuzieQs External Database (EXTDB) functionality to store these type of design details.  This is "off label" use of SuzieQ.  Products like OpsMill's InfraHub are targeting this gap in automation tools.
- Installation artefacts
  - In addition to the YAML file we have installation pictures based on the appliance models being deployed.  The YAML file indiciates which picture is to be used in the template.
  - Take a look at the YAML files so you can understand the structure and content

Please open the `gen_procedure_starter.py` script in your favorite editor and lets get to work!

```python
% python gen_procedure_starter.py 
YAML File Contents
{'mgmt_subnet': '', 'model': ''}


Saved installation Markdown file to 
```





```python
% uv pip install -e .
Resolved 106 packages in 22ms
      Built ac3-templating-workshop @ file:///Users/claudiadeluna/Indigo%20Wire%20Networks%20Dropbox/Claudia%20de%20Luna/scripts/python/2025/ac3_templating_workshop
Prepared 1 package in 626ms
Installed 1 package in 11ms
 + ac3-templating-workshop==0.1.0 (from file:///Users/claudiadeluna/Indigo%20Wire%20Networks%20Dropbox/Claudia%20de%20Luna/scripts/python/2025/ac3_templating_workshop)
claudiadeluna in ~/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/python/2025/ac3_templating_workshop on main
% cd 02_Procedure 
claudiadeluna in ~/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/python/2025/ac3_templating_workshop/02_Procedure on main
% uv run gen_procedure.py
usage: gen_procedure.py [-h] payload_file
gen_procedure.py: error: the following arguments are required: payload_file
claudiadeluna in ~/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/python/2025/ac3_templating_workshop/02_Procedure on main

```



## Overview

This mini project illustrates how to use a template to develop specific installation procedures for a particular location.

### Usage

```python
% python gen_procedure.py -h                              
usage: gen_procedure.py [-h] [-p PAYLOAD_FILE]

Script Description

options:
  -h, --help            show this help message and exit
  -p PAYLOAD_FILE, --payload_file PAYLOAD_FILE
                        YAML Payload file to use

Usage: 'python gen_procedure.py' The default payload is 'Installation_details.yml'. To use another payload file use the -p option.


```

The project has two YAML files with installation payload.  One for a model S600 and the other for a model S2000 appliance.

```python
% python gen_procedure.py -p Installation_details_S600.yml
```

This mini project will show how to send a dictionary to the template and explode out by key/value pairs.
This is another "lesson learned" and we will use this for all the remaining mini projects.

This mini project establishes the typical processing pattern:

- manipulate the data 
  - Calculate the IP, Gateway, and Mask in dotted decimal.

- put it in a payload dictionary
- send the payload to the template via the render call
- break out in the template

We also continue using utils module.

The following functions in the utils module are used:

- `get_first_ip` to calculate the gateway for the applicance configuraiton
- `get_mask_from_cidr` to calculate the mask in dotted decimal notation for the appliance configuration
- `get_fourth_ip` to calculate the IP (4th in subnet by convention) for the appliance configuration
- Step1: `jenv_filesystem` to safely establish the template file system including single line comments and white space control
- Step2: `load_jtemplate` to safely load the required report template
- Step 3 is done in-line in the script
- `save_file` to save the resulting procedure Markdown file

### Passing the payload

```python
YAML File Contents
{
 'appliance_location': 'Floor 1 MDF',
 'due_date': datetime.date(2024, 12, 4),
 'l3_dev': 'den-core01',
 'loc_type': 'branch',
 'location': 'DEN Office',
 'mgmt_int': 'GigabitEthernet1/0/47',
 'mgmt_subnet': '192.168.7.0/29',
 'mgmt_sw': 'den-as01',
 'mgmt_vlan': 60,
 'model': 'S600',
 'name': 'den-sec-app01.uwaco.net',
 'notes': 'Shelf may be a tight fit an may use up an extra RU',
 'photos': 'TBD',
 'power_plug': 'NEMA 5-15',
 'rack': 1,
 'rspan_range': '7XX',
 'ru': 12,
 'sh_email': 'ed@king-of-comedy.net',
 'sh_mobile': '555-666-5677',
 'smart_hands': 'Ed Herlihy',
 'span_int': 'TenGigabitEthernet1/1/21'
}

```



In the Current Sate Report mini project we saw how sending individual variables to the template could become "messy".  That would certainly be the case with these 20 variables.  Here we introduce the idea of sending a more complex data structure, a dictionary or a list of dictionaries.

In this mini project we will establish the pattern of sending our payload in dictionary.

Example:

payload_dict = {
  "ip_address": "192.168.0.1"
}


```
  rendered = template_obj.render(cfg=payload_dict)
```

We send our payload_dict to our template in the variable cfg (something short so we dont have to type so much!)

Now we can get the IP address by using the key of "ip_address" in the cfg dictionary.

Jinja2 Template using cfg variable:

```
IP Address is {{ cfg['ip_address'] }}
```

We could send `payload=payload_dict` and then get the ip via `payload['ip_address']`.

Jinja2 Template using payload variable:

```
IP Address is {{ payload['ip_address'] }}
```

Another option is to send the payload directly. 

```
  rendered = template_obj.render(payload_dict)
```

This probably seems very attractive.  Jinja2 will "unpack" the variable (**) so you can use the "key" directly in your template like below.

```
IP Address is {{ 'ip_address' }}
```

While attractive, this "un-named" approach makes troubleshooting more difficult.  If you don't know all the keys (of course you can list them in your script) or want to look at what is getting passed to your template, this method does not directly support that.

For this reason, I always recommend passing a named variable like `cfg`.   While the un-named strategy exposes the keys directly, it is harder to troubleshoot and handle lists.

Worst case, you can have a template with:

```
Payload {{ cfg }}
```

which will output your data structure once rendered.



---
### Modules 

- Utils

  - jinja2

  - PyYAML

---

### Alternatives

All files are local for this mini project.



```bash
├── 02_Procedure
│   ├── Installation_details_S2000.yml
│   ├── Installation_details_S600.yml
│   ├── Installation_details_template.yml
│   ├── README.md
│   ├── gen_procedure_starter.py
│   ├── images
│   │   ├── ORDR_S2000_Sensor.jpg
│   │   ├── ORDR_S600_Sensor.jpg
│   │   └── istockphoto-519363862-612x612.jpeg
│   ├── templates
│   │   └── installation_procedure_md_template.j2
│   └── working_example
│       ├── GDL Office_ORDR_Appliance_Installation_20241113-110428.md
│       └── gen_procedure.py
```







```python
claudia@Claudias-Mac-mini-m1 02_Procedure % uv sync
Resolved 110 packages in 0.75ms
Audited 105 packages in 0.05ms
claudia@Claudias-Mac-mini-m1 02_Procedure % uv run gen_procedure.py
Traceback (most recent call last):
  File "/Users/claudia/Indigo Wire Networks Dropbox/Claudia de Luna/Mac/Downloads/clones/ac3-ws-c4-jinja2-in-action/02_Procedure/gen_procedure.py", line 36, in <module>
    from utils import utils
ModuleNotFoundError: No module named 'utils'
claudia@Claudias-Mac-mini-m1 02_Procedure % cd ..
claudia@Claudias-Mac-mini-m1 ac3-ws-c4-jinja2-in-action % uv pip install -e .
Resolved 106 packages in 528ms
      Built ac3-templating-workshop @ file:///Users/claudia/Indigo%20Wire%20Networks%2
Prepared 1 package in 671ms
Installed 1 package in 1ms
 + ac3-templating-workshop==0.1.0 (from file:///Users/claudia/Indigo%20Wire%20Networks%20Dropbox/Claudia%20de%20Luna/Mac/Downloads/clones/ac3-ws-c4-jinja2-in-action)
claudia@Claudias-Mac-mini-m1 ac3-ws-c4-jinja2-in-action % cd 02_Procedure
claudia@Claudias-Mac-mini-m1 02_Procedure % uv run gen_procedure.py
usage: gen_procedure.py [-h] payload_file
gen_procedure.py: error: the following arguments are required: payload_file
claudia@Claudias-Mac-mini-m1 02_Procedure % uv run gen_procedure.py Installation_details_S2000.yml
YAML File Contents
{'appliance_location': 'TBD',
 'due_date': datetime.date(2024, 12, 4),
 'l3_dev': 'gdl-core01',
 'loc_type': 'campus',
 'location': 'GDL Office',
 'mgmt_int': 'GigabitEthernet1/0/21',
 'mgmt_subnet': '192.168.1.0/29',
 'mgmt_sw': 'gdl-as01',
 'mgmt_vlan': 31,
 'model': 'S2000',
 'name': 'gdl-sec-app01.uwaco.net',
 'notes': 'Plenty of room above the core device in Rack 5',
 'photos': 'TBD',
 'power_plug': 'NEMA 5-15',
 'rack': 5,
 'rspan_range': '7XX',
 'ru': 31,
 'sh_email': 'rupert@king-of-comedy.net',
 'sh_mobile': 'pay phone 3 located in Times Square 555-555-5555',
 'smart_hands': 'Rupert Pupkin',
 'span_int': 'TenGigabitEthernet1/1/17'}


Saved installation Markdown file to /Users/claudia/Indigo Wire Networks Dropbox/Claudia de Luna/Mac/Downloads/clones/ac3-ws-c4-jinja2-in-action/02_Procedure/GDL Office_ORDR_Appliance_Installation_20250508-160543.md

claudia@Claudias-Mac-mini-m1 02_Procedure %
```

Rank	Airport	IATA / ICAO
1.	Václav Havel Airport Prague	PRG / LKPR
2.	Brno–Tuřany Airport	BRQ / LKTB
3.	Leoš Janáček Airport Ostrava	OSR / LKMT
4.	Karlovy Vary Airport	KLV / LKKV


```
 1497  cd ..
 1498  uv pip install -e .
 1499  uv sync
 1500  uv pip install -e .
 1501  cd 02_Procedure
 1502  uv run gen_procedure.py
 1503  uv run gen_procedure.py Installation_details_S2000.yml

```