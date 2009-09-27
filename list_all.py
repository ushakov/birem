from google.appengine.ext import webapp
from google.appengine.api import users

import template
import data

remdb = data.ReminderDB()

class Handler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
            return
        rems = remdb.RemindersForUser(user)
        tpl = {}
        tpl['user'] = user.nickname()
        tpl['logouturl'] = users.create_logout_url
        tpl['reminders'] = []
        for rem in rems:
            tpl['reminders'].append(rem.AsDict())
        self.response.out.write(template.Render("all.html", tpl))
