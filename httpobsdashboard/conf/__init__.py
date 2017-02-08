import collections
import json
import os.path

__dirname = os.path.abspath(os.path.dirname(__file__))

# Open the JSON configuration files
with open(os.path.join(__dirname, 'site-deviations.json'), 'r') as __f:
    site_deviations = json.load(__f)

with open(os.path.join(__dirname, 'sites.json'), 'r') as __f:
    __sites_json = json.load(__f, object_pairs_hook=collections.OrderedDict)
    sites = __sites_json['sites']

with open(os.path.join(__dirname, 'deviations.json'), 'r') as __f:
    deviations = json.load(__f)

# Set all the JSON values as global values
with open(os.path.join(__dirname, 'config.json'), 'r') as __f:
    config = json.load(__f)

    for k, v in config.items():
        globals()[k] = v

__all__ = list(config.keys()) + ['deviations', 'site_deviations', 'sites']
