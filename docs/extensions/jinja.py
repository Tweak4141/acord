"""
Allows us to use jinja within our .rst files

We can use this to our advantage as generated rst is processed afterwards
"""
import inspect
from sphinx.application import Sphinx
import acord

SHARED_PROPERTIES = ['Config', 'construct', 'copy', 'dict', 'from_orm', 
                     'json', 'parse_file', 'parse_obj', 'parse_raw', 'schema', 
                     'schema_json', 'update_forward_refs', 'validate']


def filter_properties(cls):
    elements = dir(cls)
    filtered = []

    for element in elements:
        if element.startswith("_") or element in SHARED_PROPERTIES:
            continue
        filtered.append(element)

    return filtered

def is_function(cls):
    if inspect.isfunction(cls):
        return True
    return True


def worker(app: Sphinx, docname: str, source: list):
    if app.builder.format != "html":
        return

    src = source[0]
    rendered_source = app.builder.templates.render_string(
        src, {
            "acord": acord,
            "getattr": getattr,
            "dir": dir,
            "disallow": ["final", ],
            "filter_properties": filter_properties,
            "is_function": is_function
        }
    )

    source[0] = rendered_source


def setup(app: Sphinx):
    app.connect("source-read", worker)
