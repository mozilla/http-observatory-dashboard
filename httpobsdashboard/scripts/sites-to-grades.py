from httpobsdashboard.dashboard.deviate import deviate
from httpobs.scanner.local import scan

import os.path


if __name__ == '__main__':
    __dirname = os.path.abspath(os.path.dirname(__file__))

    all_hosts = []
    with open('complete-site-list.txt', 'r') as f:
        for line in f:
            all_hosts.append(line.strip())

    # Then go retrieve the results
    for host in all_hosts:
        if '*' in host:
            print(','.join((host, 'N/A')))
            continue

        try:
            results = {
                'httpobs': scan(host)
            }

            results = deviate(host, results)

            if 'error' in results['httpobs']:
                print(','.join((host, 'error')))

            else:
                grade = results['httpobs']['scan']['grade']

                if grade is None:
                    grade = 'requested exemption'

                print(','.join((host, grade)))
        except (KeyboardInterrupt, SystemExit):
            print('Error: caught keyboard interrupt')
            raise
        except:
            raise
            print(','.join((host, '??')))
