from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('device_config.j2')

data = {
    'hostname': 'EdgeRouter01',
    'uplink_ip': '192.0.2.1',
    'uplink_mask': '255.255.255.0',
    'ospf_router_id': '1.1.1.1',
    'loopback_net': '1.1.1.1 0.0.0.0',
    'snmp_community': 'public',
}

rendered_config = template.render(data)
print(rendered_config)
