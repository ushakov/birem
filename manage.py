from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users

import template
import data
import common

class Handler(common.UserPageHandler):
    def DoGet(self):
        if 'del' in self.request.params:
            try:
                entry = data.Reminder.get(self.request.params['del'])
                if entry:
                    entry.delete()
                    self.tpl['message'] = "Entry deleted"
            except db.KindError:
                pass
        rems = data.remdb.RemindersForUser(self.user)
        self.tpl['reminders'] = []
        for rem in rems:
            self.tpl['reminders'].append(rem.AsDict())
            
        self.Reply("manage.html")
