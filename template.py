import os
from google.appengine.ext.webapp import template

TEMPLATE_DIR="templates"

def Render(file, values):
    fname = os.path.join(os.path.dirname(__file__), TEMPLATE_DIR, file)
    return template.render(fname, values)
    
