from google.appengine.ext import webapp
from google.appengine.api import users

import common
import template
import data

remdb = data.ReminderDB()

class Handler(common.UserPageHandler):
    def DoGet(self):
        self.tpl['reminders'] = []
        for rem in remdb.UpcomingReminders(self.user):
            self.tpl['reminders'].append(rem.AsDict())
        self.Reply("home.html")
