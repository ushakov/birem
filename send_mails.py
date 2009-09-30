from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
import datetime

import template
import data

_UUID = "526f04e1-8d3c-4001-987d-8f598100dde5"

remdb = data.ReminderDB()

class Handler(webapp.RequestHandler):
    def get(self):
        if ('key' not in self.request.params or
            self.request.params != _UUID):
            self.response.set_status(403)
            return

        users = remdb.UsersToRemind()
        for user in users:
            tpl = {}
            tpl['reminders'] = []
            today = datetime.date.today()
            tpl['date'] = {}
            tpl['date']['day'] = today.day
            tpl['date']['month'] = data.Months.Name(today.month)
            tpl['date']['year'] = today.year
            tpl['date']['weekday'] = today.weekday

            for rem in remdb.RemindersToSend(user):
                if rem.day == today.day && rem.month == today.month:
                    tpl['today'] = rem.AsDict()
                else:
                    tpl['reminders'].append(rem.AsDict())
            mail = template.Render("mail.html", tpl)
            
