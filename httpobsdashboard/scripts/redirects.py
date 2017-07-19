from urllib.parse import urlparse
import requests

sites = set()
additions = set()

with open('output/current.txt', 'r') as f:
    for site in f.readlines():
        sites.add(site.strip())

# with open('output/additions.txt', 'r') as f:
#     for site in f.readlines():
#         sites.add(site.strip())
#
# print(sites)

with open('output/additions.txt', 'r') as f:
    for site in f.readlines():
        url = 'http://' + site.strip() + '/'
        try:
            r = requests.get(url)
        except:
            url = 'https://' + site.strip() + '/'
            r = requests.get(url, verify=False)

        hostname = urlparse(r.url).hostname
        if hostname not in sites:
            additions.add(hostname)

for site in additions:
    print(site)