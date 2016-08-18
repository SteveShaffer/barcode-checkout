import os
from datetime import datetime

import jinja2


je = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


def relativedate(value):
    if not value:
        return ''

    diff = (datetime.now() - value).total_seconds()
    if diff < 60:  # TODO: Recurse?
        value = int(diff)
        unit = 'second'
    elif diff < 60 * 60:
        value = int(diff/60)
        unit = 'minute'
    elif diff < 24 * 60 * 60:
        value = int(diff/24/60)
        unit = 'hour'
    elif diff < 7 * 24 * 60 * 60:
        value = int(diff/7/24/60)
        unit = 'day'
    else:
        return value.strftime('%b %d, %Y')
    if value > 1:
        unit += 's'
    return '{} {} ago'.format(value, unit)

je.filters['relativedate'] = relativedate


def render(template, values={}):
    template = je.get_template(template + '.html')
    return template.render(values)
