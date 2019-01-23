from types import SimpleNamespace

from jinja2 import Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader('param_data'),
                  trim_blocks=True,
                  lstrip_blocks=True)

# Load the nc params data
with open('param_data/axis_nc.yaml', 'r') as fd:
    data = yaml.safe_load(fd)
nc_params = []
for param, info in data.items():
    ns = SimpleNamespace(
        stConfig=param,
        MC_AxisParameter=info['mc'],
        is_bool=(info['type'] == 'bool'))
    camelcase = ''.join(txt.capitalize() for txt in param.split('_'))
    ns.fb_write = 'fbWrite' + camelcase
    ns.fb_write_done = ns.fb_write + '.Done'
    ns.fb_write_busy = ns.fb_write + '.Busy'
    ns.fb_write_error = ns.fb_write + '.Error'
    ns.fb_read = 'fbRead' + camelcase
    ns.fb_read_valid = ns.fb_read + '.Valid'
    ns.fb_read_busy = ns.fb_read + '.Busy'
    ns.fb_read_error = ns.fb_read + '.Error'
    nc_params.append(ns)

# Make the axis write nc file
template = env.get_template('FB_AxisWriteNC.TcPOU')
stream = template.stream(nc_params=nc_params)
stream.dump('TestProject/POUs/FB_AxisWriteNC.TcPOU')

# Make the axis read nc file
template = env.get_template('FB_AxisReadNC.TcPOU')
stream = template.stream(nc_params=nc_params)
stream.dump('TestProject/POUs/FB_AxisReadNC.TcPOU')

# Make the axis write CoE file
# Make the axis read CoE file
