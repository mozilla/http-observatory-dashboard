from httpobsdashboard.conf import sites
import requests


START_TIME = 1470632400    # August 8th
URL = 'https://http-observatory.security.mozilla.org/api/v1/getHostHistory?host='

for group in sites:
    print(group + '\n' + '-' * len(group))

    for host in sites[group]:
        # Get the host history
        r = requests.get(URL + host).json()

        # Move on if no history is found
        if 'error' in r:
            continue

        # Remove anything before August 8th
        recent = [entry for entry in r if entry.get('end_time_unix_timestamp', 0) > START_TIME]

        # If nothing has changed at all in ages, just return the very most recent score
        if not recent:
            recent = [r[-1]]

        # Get the grades
        grades = [entry.get('grade') for entry in recent]

        # Print things out
        print('{0}: {1}'.format(host, ', '.join(grades)))

    print