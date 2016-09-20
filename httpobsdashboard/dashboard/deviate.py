import httpobsdashboard.conf


REASONS = {
    'API': {
        'httpobs': {
            'tests': {
                'content-security-policy': {
                    'pass': None,
                    'score_description': 'APIs don\'t contain active content and don\'t need CSP.',
                    'score_modifier': 0
                },
                'subresource-integrity': {
                    'pass': None,
                    'score_description': 'APIs don\'t utilize subresources.',
                    'score_modifier': 0
                },
                'x-frame-options': {
                    'pass': None,
                    'score_description': 'APIs don\'t have content to frame.',
                    'score_modifier': 0
                },
                'x-xss-protection': {
                    'pass': None,
                    'score_description': 'APIs don\'t contain active content and don\'t need XXSSP.',
                    'score_modifier': 0
                },
            }
        }
    },
    'Cloud Services': {
        'httpobs': {
            'scan': {
                'grade': None
            }
        }
    },
    'Windows XP Support': {
        'tlsobs': {
            'pass': True
        }
    }
}


def __destructive_merge(d1: dict, d2: dict, path=None) -> dict:
    """Recursively merges d2 into d1, overwriting existing values"""
    if path is None:
        path = []

    for key in d2:
        if key in d1:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                __destructive_merge(d1[key], d2[key], path + [str(key)])
            else:
                d1[key] = d2[key]
        else:
            d1[key] = d2[key]
    return d1


def deviate(host, results: dict) -> dict:
    # See if the host is in deviations.json
    deviations = httpobsdashboard.conf.deviations.get(host, [])

    for deviation in deviations:
        results = __destructive_merge(results, REASONS[deviation])

    return results
