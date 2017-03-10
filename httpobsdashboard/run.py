import datetime
import httpobsdashboard.conf
import httpobsdashboard.dashboard
import json
import nested_dict
import os.path
import sys

from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[-1] not in ['json-generate', 'www-generate']:
        print('Must run with either json-generate or www-generate')
        sys.exit()

    today = str(datetime.datetime.now()).split('.')[0]
    __dirname = os.path.abspath(os.path.dirname(__file__))

    if sys.argv[1] == 'json-generate':
        # Create a sites object to store results in, and a shorter _sites pointer to the JSON
        sites = nested_dict.nested_dict()
        _sites = httpobsdashboard.conf.sites

        # First prime all the sites (to speed up scans)
        all_hosts = []
        for group in _sites:
            for sub_group in _sites[group]:
                for host in _sites[group][sub_group]:
                    all_hosts.append(host)

        if httpobsdashboard.conf.debug:
            print('Initiating mass scan')

        httpobsdashboard.dashboard.mass_scan_priming(all_hosts)

        # group == category (like Bounty Site)
        # sub_group == section name (like Addons)

        # Then go retrieve the results
        for group in _sites:
            if httpobsdashboard.conf.debug:
                print('Scanning group: {groupName}'.format(groupName=group))

            for sub_group in _sites[group]:
                for host in _sites[group][sub_group]:
                    # Now retrieve all the results
                    response = httpobsdashboard.dashboard.retrieve(host)
                    analysis = httpobsdashboard.dashboard.analyze(host, response)

                    # Store the results
                    sites[group][sub_group][host] = analysis

        # Once this is done, we need to calculate statistics
        stats = {}
        passing = quantity = percentage = ungraded = 0
        for group in sites:
            stats[group] = {
                'passing': 0,
                'quantity': 0,
                'percentage': 0,
                'ungraded': 0,
            }

            for sub_group in sites[group]:
                for host, analysis in sites[group][sub_group].items():
                    # keep track of sites that have opted out
                    if analysis.get('httpobs', {}).get('grade') is None:
                        stats[group]['ungraded'] += 1
                        ungraded += 1

                    # increment the counter if it means the minimum score
                    elif analysis.get('httpobs', {}).get('score', 0) >= httpobsdashboard.conf.statsForManagersMinScore:
                        stats[group]['passing'] += 1
                        passing += 1

                    stats[group]['quantity'] += 1
                    quantity += 1

            # calculate the percentage
            if stats[group]['passing'] != 0:
                stats[group]['percentage'] = int(stats[group]['passing']
                                                 / (stats[group]['quantity'] - stats[group]['ungraded'])
                                                 * 100)

        # Now calculate overall stats
        stats['Overall'] = {
            'passing': passing,
            'quantity': quantity,
            'percentage': int((passing) / (quantity - ungraded) * 100),
            'ungraded': ungraded
        }

        # Write the results to disk
        with open(os.path.join(__dirname, 'dist', 'data', 'sites.json'), 'w') as f:
            json.dump(sites, f)
        with open(os.path.join(__dirname, 'dist', 'data', 'stats.json'), 'w') as f:
            json.dump(stats, f)

    elif sys.argv[1] == 'www-generate':
        with open(os.path.join(__dirname, 'dist', 'data', 'sites.json'), 'r') as f:
            sites = json.load(f, object_pairs_hook=OrderedDict)
        with open(os.path.join(__dirname, 'dist', 'data', 'stats.json'), 'r') as f:
            stats = json.load(f, object_pairs_hook=OrderedDict)

        # Information to pass into the rendererererer
        config = {
            'DATE': today,
            'config': httpobsdashboard.conf.config,
            'sites': sites,
            'stats': stats
        }

        # Render the page templates
        env = Environment(loader=FileSystemLoader(os.path.join(__dirname, 'templates')))
        template = env.get_template('index.html')
        with open(os.path.join(__dirname, 'dist', 'index.html'), 'w') as f:
            f.write(template.render(**config))
