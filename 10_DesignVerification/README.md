# Design vs Implementation

Hopefully by now this whole process has become tedious and the most interesting part is working with the data.

In this mini project we will look at the Design Data (Yes...Intent) stored in our Design Source of Truth, OpsMill InfraHub, and compare it to an implementation.

We will take the Chicago ORD Campus, 
1. determine which vlans it should have configured by design,   
2. gather the actual vlans configued via our observability platform, SuzieQ

and report on any findings of missing vlans.

```
uv run gen_design_verification.py
```

#### Options
```
claudia@Claudias-MacBook-AirM415 10_DesignVerification % uv run gen_design_verification.py -h
usage: gen_design_verification.py [-h] [-k KIND] [-o OUTPUT_DIR]

Script Description

options:
  -h, --help            show this help message and exit
  -k KIND, --kind KIND  Specify the kind for client.all
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        output directory Markdown procedure files. Default is output.

Usage: ' python test1.py'
```

### Modules
Infrahub SDK