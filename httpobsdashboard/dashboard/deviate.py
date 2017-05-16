import httpobsdashboard.conf


def __destructive_merge(d1, d2, path=None):
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


def deviate(host, results):
    # See if the host is in site-deviations.json
    deviations = httpobsdashboard.conf.site_deviations.get(host, [])

    for deviation in deviations:
        results = __destructive_merge(results, httpobsdashboard.conf.deviations[deviation])

    return results

def get_score_deviation(host):
    # See if the host has any score deviations
    deviations = httpobsdashboard.conf.site_deviations.get(host, [])

    for deviation in deviations:
        if httpobsdashboard.conf.deviations[deviation].get('httpobs', {}).get('scan', {}).get('score'):
            return httpobsdashboard.conf.deviations[deviation]['httpobs']['scan']['score']

    return None
