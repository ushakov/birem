from google.appengine.ext import webapp
from google.appengine.api import users

import template
import data

class ValidationFailed:
    def __init__(self, msg):
        self.msg = msg

    def get_message(self):
        return self.msg

def v_text(size):
    def validate(t):
        if len(t) > size:
            raise ValueError()
        return unicode(t)
    return validate

def v_bounded(low, high):
    def validate(s):
        d = int(s)
        if d < low or d > high:
            raise ValueError()
        return d
    return validate

FIELDS = [
    ('note', v_text(500), 'Note must be short text'),
    ('day', v_bounded(1,31), 'Day should name a day in the month (1-31)'),
    ('month',v_bounded(1,12), 'Month should be in 1-12'),
]

class Handler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
            return
        self.response.out.write(template.Render("add.html", {}))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
            return
        entry = data.Reminder()
        tpl = dict(self.request.params)
        for t in FIELDS:
            key = t[0]
            try:
                val = t[1](tpl[key])
                entry.__dict__[t[0]] = val
            except ValueError:
                tpl['error'] = t[2]
                break
            entry.put()
        self.response.out.write(template.Render("add.html", tpl))
