# Configuration Templates

These mini-projects have a number of examples to showcase the different strategies.

- Monolithic
- Modular <-- We are HERE
  - Using Jinja2 Inheritance
  - Using Jinja2 Includes




## Modular

The modular strategy gives you the a'la carte option in two different flavors.

You can break out your configurations as you like including
- base
- user interface
- uplinks (by model if you like)
- NAC servers
- TACACS servers
- tty configuration
- routing
- acls
- ....

Each one can now be updated individually without having to modify the one big template, for the most part.

Jinja has two approaches to support this "modularity":

1. Inheritance (extends)
2. includes

## Modular - Inheritance (extends) Model

With inheritance you define a base template with {% block <name> %} and child templates.

base_switch_config.j2 (base)

- ​	user_interface_config.j2 (child template extends "base_switch_config.j2")
- ​	tacacs_server_config.j2 (child template extends "base_switch_config.j2")

The price for that is you need one (or more) overarching templates to put it all together.

```python
{# base_switch_config_block_extends.j2 #}
hostname {{ hostname }}

vlan {{ user_vlan }}
 name USER_VLAN

{% block user_interface %}
{# This block will be overridden by child templates #}
{% endblock %}

{% block tacacs_config %}
{# This block will be overridden by child templates #}
{% endblock %}

```



Example child template which extends base (above).

```python
{# user_interface_config_extends.j2 #}
{% extends "base_switch_config_block_extends.j2" %}

{% block user_interface %}
interface {{ user_interface }}
 description User Access Port
 switchport mode access
 switchport access vlan {{ user_vlan }}
 spanning-tree portfast
 spanning-tree bpduguard enable
{% endblock %}
```



## Modular - Include Model

The include method allows you to set up a sort of scaffolding for your templates.

```python
% python modular_sw_cfg_include.py -h
usage: modular_sw_cfg_include.py [-h]

Script Description

options:
  -h, --help  show this help message and exit

Usage: ' python modular_sw_cfg_include.py'

```



main_switch_config_include.j2 ("scaffolding")

- base_switch_config_include.j2 (base/global configuration section)
- tacacs_server_config_include.j2 (tacacs configuration section)
- user_interface_config_include.j2 (user interface section)

Includes main template **main_switch_config_include.j2** "bundles" all the sub-templates.

```python
{#- main_switch_config_include.j2 -#}
!Main Switch Configuration Template (Includes)

! Include base with global commands
{% include "base_switch_config_include.j2" %}

! Include user interfaces
{% block user_interface %}
{% include "user_interface_config_include.j2" %}
{% endblock %}

! Include aaa/tacacs
{% block tacacs_config %}
{% include "tacacs_server_config_include.j2" %}
{% endblock %}
```

Example sub-template:

```python
{#- user_interface_config_include.j2 -#}
interface {{ user_interface }}
 description User Access Port
 switchport mode access
 switchport access vlan {{ user_vlan }}
 spanning-tree portfast
 spanning-tree bpduguard enable
```

I prefer the includes model as its cleaner (to me).  The inheritance model was built to support HTML pages and I find it is more cumbersome for developing device configurations but both models can work so it really comes down to what works for you!

WARNING
These templates are for example only. They have not been tested andy may not work!


---
### Modules

- jinja2


---

### Alternatives

All files are local for this mini project.

```bash
── 04_ConfigurationsModular
│   ├── README.md
│   ├── modular
│   │   ├── modular_sw_cfg_extends.py
│   │   ├── modular_sw_cfg_include.py
│   │   └── templates
│   │       ├── base_switch_config_block_extends.j2
│   │       ├── base_switch_config_include.j2
│   │       ├── main_switch_config_include.j2
│   │       ├── tacacs_server_config_extends.j2
│   │       ├── tacacs_server_config_include.j2
│   │       ├── user_interface_config_extends.j2
│   │       └── user_interface_config_include.j2

```

