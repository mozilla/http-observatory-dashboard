import collections
import json
import os.path


__dirname = os.path.abspath(os.path.dirname(__file__))


# Open the JSON configuration files
with open(os.path.join(__dirname, 'deviations.json'), 'r') as __deviations_f:
    deviations = json.load(__deviations_f)
#deviations = __deviations_json['sites']

with open(os.path.join(__dirname, 'sites.complete.json'), 'r') as __sites_f:
    __sites_json = json.load(__sites_f, object_pairs_hook=collections.OrderedDict)
sites = __sites_json['sites']
