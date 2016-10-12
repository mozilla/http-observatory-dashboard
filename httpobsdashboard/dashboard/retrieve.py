import os
import grequests
import requests
import sys
import time


HTTPOBS_API_URL = os.environ.get('HTTPOBS_API_URL') or 'https://http-observatory.security.mozilla.org/api/v1'
TLSOBS_API_URL = 'https://tls-observatory.services.mozilla.com/api/v1'


def mass_scan_priming(hosts):
    # Initiate the TLS Observatory scans
    rs = (grequests.post(TLSOBS_API_URL + '/scan', data={'rescan': 'false', 'target': host}) for host in hosts)
    grequests.map(rs)

    # Initiate the HTTP Observatory scans
    urls = [HTTPOBS_API_URL + '/analyze?host=' + host for host in hosts]
    rs = (grequests.post(url, data={'rescan': 'false'}) for url in urls)
    grequests.map(rs)


def retrieve(host):
    return {
        'httpobs': __get_http_observatory(host),
        'tlsobs': __get_tls_observatory(host)
    }


def __get_http_observatory(host):
    api_url = os.environ.get('HTTPOBS_API_URL') or 'https://http-observatory.security.mozilla.org/api/v1'

    r = {}
    try:
        # Initiate the scan
        r = {}
        url = api_url + '/analyze?host=' + host
        while r.get('scan', {}).get('state') not in ('ABORTED', 'FAILED', 'FINISHED'):
            r['scan'] = __poll(url, 'state', None, 'GET', None, None, 300, 0)

        # Retrieve the individual test results
        if r['scan']['state'] == 'FAILED':
             r['tests'] = {
                    'content-security-policy': {
                        'pass': None,
                        'score_description': 'Site down',
                        'score_modifier': 0
                    },
                    'contribute': {
                        'pass': False,
                        'score_modifier': 0
                    },
                    'strict-transport-security': {
                        'pass': None,
                        'score_description': 'Site down',
                        'score_modifier': 0
                    },
                    'subresource-integrity': {
                        'pass': None,
                        'score_description': 'Site down',
                        'score_modifier': 0
                    },
                    'x-content-type-options': {
                     'pass': None,
                     'score_description': 'Site down',
                     'score_modifier': 0
                    },
                    'x-frame-options': {
                        'pass': None,
                        'score_description': 'Site down',
                        'score_modifier': 0
                    },
                    'x-xss-protection': {
                        'pass': None,
                        'score_description': 'Site down',
                        'score_modifier': 0
                    }
             }
        else:
            url = api_url + '/getScanResults?scan=' + str(r['scan']['scan_id'])
            r['tests'] = __poll(url, 'content-security-policy')

    except requests.exceptions.RequestException:
        pass

    return r


def __get_tls_observatory(host):
    # First get the scan ID
    url = TLSOBS_API_URL + '/scan'

    r = __poll(url,
               key='scan_id',
               method='POST',
               data={
                   'rescan': 'false',
                   'target': host
               })

    # Then, use that scan_id to get the results
    url = TLSOBS_API_URL + '/results?id=' + str(r.get('scan_id'))
    r = __poll(url,
               key='completion_perc',
               values=[100])

    return r


def __poll(url, key, values=None, method='GET', headers=None, data=None, timeout=300, interval=1.0):
    if headers is None:
        headers = {}

    if data is None:
        data = {}

    # Create requests session
    s = requests.Session()
    s.headers.update(headers)

    # Set the start time, since we don't want to go longer than timeout seconds
    start_time = time.time()

    while True:
        # Retrieve the URL
        if method == 'POST':
            r = s.post(url, data=data, timeout=timeout).json()
        else:
            r = s.get(url, timeout=timeout).json()

        # See if error is in there; if so, we just NA everything
        if 'error' in r or time.time() - start_time > timeout:
            print('\nUnable to get result from the HTTP Observatory @ {url}. Error: {error}.'.format(error=r['error'],
                                                                                                     url=url))
            # If things error out in the HTTP Observatory analyzer
            if HTTPOBS_API_URL + '/analyze' in url:
                return {
                           'grade': None,
                           'state': 'FAILED'
                       }
            # The TLS Observatory
            elif TLSOBS_API_URL in url:
                return {
                    'tlsobs': {
                        'has_tls': None,
                        'pass': None
                    }
                }

            # Some unknown condition
            else:
                print('Exiting')
                sys.exit(1)

        # See if the key is one of the pollable values
        if values:
            if r[key] in values:
                return r
        else:
            if key in r:
                return r

        time.sleep(interval)
