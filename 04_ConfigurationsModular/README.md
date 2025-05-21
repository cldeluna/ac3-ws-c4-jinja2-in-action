# Configuration Templates

These mini-projects have a number of examples to showcase the different strategies.

- Monolithic
- **Modular** <-- We are HERE
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

Because each "feature" has its own template its is easy to generate individual feature updates.

Jinja has two approaches to support this "modularity":

1. Inheritance (extends)
2. includes

## Modular - Inheritance (extends) Model

With inheritance you define a base template with {% block <name> %} and child templates.

### Simple Example

```python
% tree extends_example 
extends_example
├── base_device.j2
├── core_switch.j2
└── generate.py

1 directory, 3 files

```

![simple_extends_block_2025-05-21_05-40-19](images/simple_extends_block_2025-05-21_05-40-19.jpg)

### A more complex example

**modular_extends_config_generator.p**y

This script uses the follow templates:

``` % tree templates    
templates
├── mod_inherit_aaa.j2
├── mod_inherit_base.j2
├── mod_inherit_interfaces.j2
├── mod_inherit_ospf.j2
```

Notice it is more work to "put it all together" using the extends block strategy.

## Modular - Include Model

The include method allows you to set up a sort of scaffolding for your templates.

```python
% uv run modular_include_config_generator.py
```


