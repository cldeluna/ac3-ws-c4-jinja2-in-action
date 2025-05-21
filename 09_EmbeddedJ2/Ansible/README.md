# Configurations with Ansible

This showcases how Jinja2 templates are part of a larger ecosystem.  I believe you will see more and more of this as tools evolve.

Here you will need to focus on the template (probably) and the payload to send to the template.  Instantiating the environment will be done by the tool.

```bash
% tree
.
├── ansible.cfg
├── inventory
│   ├── host_vars
│   │   ├── prg-cor01.yml
│   │   └── prg-cor02.yml
│   └── hosts
├── main.py
├── playbooks
│   └── generate-configs.yml
├── pyproject.toml
├── README.md
└── templates
    ├── base.j2
    └── includes
        ├── aaa.j2
        ├── api.j2
        ├── domain.j2
        ├── interfaces.j2
        ├── mlag.j2
        ├── ntp.j2
        ├── ospf.j2
        └── ssh.j2

7 directories, 20 files
```

### Run the Playbook from the top level directory



```bash
uv run ansible-playbook -i inventory/hosts playbooks/generate-configs.yml
```

Or

```bash
ansible-playbook -i inventory/hosts playbooks/generate-configs.yml
```



#### Expected Output

![playbook_run](images/playbook_run.jpg)



```bash
%  uv run ansible-playbook -i inventory/hosts playbooks/generate-configs.yml


PLAY [Generate switch configurations] **********************************************************************************

TASK [Create config directory] *****************************************************************************************
ok: [prg-cor01]
ok: [prg-cor02]

TASK [Generate switch configs] *****************************************************************************************
changed: [prg-cor01]
changed: [prg-cor02]

PLAY RECAP *************************************************************************************************************
prg-cor01                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
prg-cor02                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

%
```





Ansible may work a little differently in our uv environment.

```python
uv venv

source .venv/bin/activate # Unix/MacOS

.venv\Scripts\activate # Windows

uv pip install ansible jmespath netaddr passlib pyyaml 

ansible --version # Should work

deactivate # When complete with exercise

```






### Expected Installation Output

```python
% uv venv
Using CPython 3.11.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
(mlag-ansible) claudiadeluna in ~/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/python/2025/mlag-ansible on main

% source .venv/bin/activate

% uv pip install ansible jmespath netaddr passlib pyyaml
Resolved 13 packages in 19ms
Installed 13 packages in 580ms
 + ansible==11.5.0
 + ansible-core==2.18.5
 + cffi==1.17.1
 + cryptography==44.0.3
 + jinja2==3.1.6
 + jmespath==1.0.1
 + markupsafe==3.0.2
 + netaddr==1.3.0
 + packaging==25.0
 + passlib==1.7.4
 + pycparser==2.22
 + pyyaml==6.0.2
 + resolvelib==1.0.1

(mlag-ansible) claudiadeluna in ~/scripts/python/2025/mlag-ansible on main
% ansible --version
ansible [core 2.18.5]
  config file = /Users/claudiadeluna/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/python/2025/mlag-ansible/ansible.cfg
  configured module search path = ['/Users/claudiadeluna/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /Users/claudiadeluna/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/python/2025/mlag-ansible/.venv/lib/python3.11/site-packages/ansible
  ansible collection location = /Users/claudiadeluna/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/python/2025/mlag-ansible/collections
  executable location = /Users/claudiadeluna/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/python/2025/mlag-ansible/.venv/bin/ansible
  python version = 3.11.12 (main, Apr  9 2025, 03:49:53) [Clang 20.1.0 ] (/Users/claudiadeluna/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/python/2025/mlag-ansible/.venv/bin/python3)
  jinja version = 3.1.6
  libyaml = True

```







