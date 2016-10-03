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
    # Find the right TLS Observatory Analyzer
    result = {}
    for analysis in raw_output.get('tlsobs', {}).get('analysis', {}):
        if analysis.get('analyzer') == 'mozillaEvaluationWorker':
            result = analysis['result']

    # Add a pass/fail thing to the TLS Observatory
    raw_output['tlsobs']['pass'] = True if result.get('level', '').lower() in ['modern', 'intermediate'] else False

    # Apply any deviations that might exist
    deviated_output = deviate(host, raw_output)

    # Clean up some output
    result['level'] = result.get('level', '').capitalize().replace('Non compliant', 'Non-compliant')
    if not deviated_output['tlsobs']['has_tls']:
        result['level'] = 'No HTTPS'

    # Make SRI N/A if there are no external scripts
    if deviated_output['httpobs']['tests']['subresource-integrity'].get('result') in \
            ['sri-not-implemented-but-all-scripts-loaded-from-secure-origin',
             'sri-not-implemented-but-no-scripts-loaded']:
        deviated_output['httpobs']['tests']['subresource-integrity']['pass'] = None

    # Rescore the site
    score = max(0, 100 + sum([test['score_modifier'] for test in deviated_output['httpobs']['tests'].values()]))
    grade = GRADE_CHART[min(100, score)] if deviated_output['httpobs']['scan']['grade'] else None

    return {
        'httpobs': {
            'grade': grade,
            'score': score,
            'tests': deviated_output['httpobs']['tests']
        },
        'tlsobs': {
            'data': deviated_output['tlsobs'],
            'grade': result.get('level', '?'),
            'pass': deviated_output['tlsobs']['pass']
        }
    }
