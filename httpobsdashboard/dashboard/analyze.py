import time

from httpobsdashboard.conf import tlsObs, trackingDeltaDays
from httpobsdashboard.dashboard.deviate import deviate


GRADE_CHART = {
    100: 'A+',
    95: 'A',
    90: 'A',
    85: 'A',
    80: 'B',
    75: 'B',
    70: 'B',
    65: 'B',
    60: 'C',
    55: 'C',
    50: 'C',
    45: 'C',
    40: 'D',
    35: 'D',
    30: 'D',
    25: 'D',
    20: 'F',
    15: 'F',
    10: 'F',
    5: 'F',
    0: 'F'
}


def analyze(host, raw_output):
    # Apply any deviations that might exist
    deviated_output = deviate(host, raw_output)

    # Make SRI N/A if there are no external scripts
    if deviated_output['httpobs']['tests']['subresource-integrity'].get('result') in \
            ['sri-not-implemented-but-all-scripts-loaded-from-secure-origin',
             'sri-not-implemented-but-no-scripts-loaded']:
        deviated_output['httpobs']['tests']['subresource-integrity']['pass'] = None

    # Calculate the score delta
    deltax = delta = 0
    if deviated_output['httpobs']['scan']['history']:
        now = int(time.time())
        for entry in deviated_output['httpobs']['scan']['history']:
            if now - entry.get('end_time_unix_timestamp', 0) < trackingDeltaDays * 24 * 60 * 60:
                deltax = (
                    deviated_output['httpobs']['scan']['history'][-1].get('score', 0) - entry.get('score', 0))
                break

        delta = (deviated_output['httpobs']['scan']['history'][-1].get('score', 0) -
                 deviated_output['httpobs']['scan']['history'][0].get('score', 0))

    # Rescore the site
    score = max(0, 100 + sum([test['score_modifier'] for test in deviated_output['httpobs']['tests'].values()]))
    grade = GRADE_CHART[min(100, score - score % 5)] if deviated_output['httpobs']['scan']['grade'] else None

    # Handle the TLS Observatory checks
    if tlsObs:
        # Find the right TLS Observatory Analyzer
        result = {}
        for analysis in deviated_output.get('tlsobs', {}).get('analysis', {}):
            if analysis.get('analyzer') == 'mozillaEvaluationWorker':
                result = analysis['result']

        # Add a pass/fail thing to the TLS Observatory
        deviated_output['tlsobs']['pass'] = True if result.get('level', '').lower() in ['modern',
                                                                                        'intermediate'] else False

        # Clean up some output
        deviated_output['tlsobs']['level'] = result.get('level', '') \
            .capitalize() \
            .replace('Non compliant', 'Non-compliant')
        if not deviated_output['tlsobs']['has_tls']:
            deviated_output['tlsobs']['level'] = 'No HTTPS'
    else:
        # If we aren't scanning with the TLS Observatory, we kind of have to fudge things a little bit

        # We use the HSTS test as a proxy to determine if HTTPS is working
        if deviated_output['httpobs']['tests']['strict-transport-security'].get('result') not in \
                ['hsts-not-implemented-no-https', 'hsts-invalid-cert']:
            deviated_output['tlsobs'] = {
                'has_tls': True,
                'level': None,
                'pass': True,
            }
        else:
            deviated_output['tlsobs'] = {
                'has_tls': False,
                'level': None,
                'pass': False,
            }

    # Remove unneeded content from the JSON output
    for k, v in deviated_output['httpobs']['tests'].items():
        if k not in ['contribute'] and 'output' in v:
            del (v['output'])

        for key in ['expectation', 'name', 'result', 'score_modifier']:
            if key in v:
                del (v[key])

    # Trim things up a bit so that the results are not HUGE
    return {
        'httpobs': {
            'delta': delta,
            'deltax': deltax,
            'grade': grade,
            'score': score,
            'tests': deviated_output['httpobs']['tests']
        },
        'tlsobs': {
            'grade': deviated_output['tlsobs']['level'],
            'pass': deviated_output['tlsobs']['pass'],
            'tls': deviated_output['tlsobs']['has_tls']
        }
    }
