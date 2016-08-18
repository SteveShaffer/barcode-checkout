import os

import jinja2


je = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


def render(template, values={}):
    template = je.get_template(template + '.html')
    return template.render(values)