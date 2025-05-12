# Change Request

In this mini project, we will craft the body of a change request and optionally create a standard 
change request on a Developer instance of Service Now.

By default the `gen_new_vlan_cr.py` script will load the data in the file `payload.csv` and using the template `new_vlan_cr_template.j2` (can you guess where it is?) will craft the text of a change request.

```python
% python gen_new_vlan_cr.py -h
usage: gen_new_vlan_cr.py [-h] [-f PAYLOAD_FILE] [-c] [-s SNOW_PDI] [-u USERNAME] [-p PASSWORD]

Script Description

options:
  -h, --help            show this help message and exit
  -f PAYLOAD_FILE, --payload_file PAYLOAD_FILE
                        Change details payload file. Default is payload.csv in current directory
  -c, --create_cr       Create Change Request in SNOW. Default is False so no CR in SNOW will be created.
  -s SNOW_PDI, --snow_pdi SNOW_PDI
                        Service Now (SNOW) Personal Developer Instance. Default: 'dev224081.service-now.com'
  -u USERNAME, --username USERNAME
                        Service Now (SNOW) Personal Developer Instance Username. Default: admin
  -p PASSWORD, --password PASSWORD
                        Service Now (SNOW) Personal Developer Instance password. Default: empty string ()

Usage: ' python gen_new_vlan_cr.py'

```

Executing the script with all the default values (and no Service Now CR creation):

```python
% python gen_new_vlan_cr.py   
Saved resulting CR file in current directory to LAX_Campus_NewVlan300_SNOW_STDCR.txt

```

SNOW credentials can be obtained from Claudia, Lucas, or Mike!

Output TXT file:

```markdown
=== Standard Change Request for new vlan 300 at LAX_Campus


Requesting new vlan 300 be configured and routed on device lax-csw03.
Route subnet 203.0.113.0/24
Please create SVI with IP 203.0.113.1


Vlan name: BLDAUTO_203.0.113.0/24

Requesting completion by: 2024-11-12
```

With the default values, the script merely generates the text of the request which could be emailed or pasted into a Change Request system.

### Creating a Service Now Change Request

Using the `-c` option will execute the portion of the script which creates a Service Now Change Request ticket.

When the -c option is used, the -p option is required and the -u option can also be used to change the username.

```python
% python gen_new_vlan_cr.py -c -s "dev224081.service-now.com" -p "PDI SNOW PWD"
Saved resulting CR file in current directory to LAX_Campus_NewVlan300_SNOW_STDCR.txt
Standard Change Request created successfully: 201
Created Standard Change Request CHG0030014
```

![Screen Shot 2024-11-07 at 7.27.19 AM](./images/Screen Shot 2024-11-07 at 7.27.19 AM.png)

## Creating a ServiceNow (SNOW) Personal Developer Instance for Testing



Personal Developer Instance of Service Now

https://developer.servicenow.com/dev.do

Installation [Guidance](https://www.perplexity.ai/page/creating-a-servicenow-develope-k17hf2WyQWGAOL_SniG4zA)


---
### Modules

- jinja2
- requests
- httpx
- python-dotenv (to store the Vault address and token)
- hvac ([HashiCorp Vault](https://hvac.readthedocs.io/en/stable/overview.html#)) (to store the SNOW credentials) (currently not in use)



---

### Alternatives

The CR creation is disabled by default.

Payload data is in a local CSV file.

```bash
├── 04_ChangeRequest
│   ├── README.md
│   ├── gen_new_vlan_cr.py
│   ├── payload.csv
│   └── templates
│       └── new_vlan_cr_template.j2

```

