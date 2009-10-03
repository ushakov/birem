from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users

import common
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

def v_year():
    def validate(s):
        if s == "":
            return None
        return int(s)
    return validate

def v_month():
    def validate(s):
        m = data.Months.Index(s)
        if not m:
            raise ValueError()
        return m
    return validate

FIELDS = [
    ('note', v_text(500), 'Note must be short text'),
    ('day', v_bounded(1,31), 'Day should name a day in the month (1-31)'),
    ('month',v_month(), 'Month should be in [Jan..Dec]'),
    ('year', v_year(), "Year should be four-digit or empty")
]

class Handler(common.UserPageHandler):
    def DoGet(self):
        params = dict(self.request.params)
        self.tpl['header'] = "Add a new reminder"
        if 'id' in params:
            try:
                entry = data.Reminder.get(params['id'])
                self.tpl.update(entry.AsDict())
                self.tpl['header'] = "Update reminder"
            except db.KindError:
                pass
        self.Reply("add.html")

    def DoPost(self):
        self.tpl['header'] = "Add a new reminder"
        self.tpl.update(dict(self.request.params))
        if 'id' in self.tpl:
            try:
                entry = data.Reminder.get(self.tpl['id'])
                self.tpl['header'] = "Update reminder"
            except db.KindError:
                entry = data.Reminder()
        else:
            entry = data.Reminder()
        for t in FIELDS:
            key = t[0]
            try:
                val = t[1](self.tpl[key])
                setattr(entry, t[0], val)
            except ValueError:
                self.tpl['error'] = t[2]
                break
        if 'error' not in self.tpl:
            entry.user = self.user
            entry.put()
            self.redirect("/manage")
            return
        self.Reply("add.html")
