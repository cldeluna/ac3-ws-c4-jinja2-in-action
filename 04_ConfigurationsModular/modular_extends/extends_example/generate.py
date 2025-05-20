from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("core_switch.j2")

data = {
    "hostname": "CoreSwitch01",
    "loopback_ip": "10.10.10.1",
    "ospf_router_id": "10.10.10.1",
    "network": "10.0.0.0 0.0.0.255",
}

rendered_config = template.render(data)
print(rendered_config)
