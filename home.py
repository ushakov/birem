from google.appengine.ext import webapp
from google.appengine.api import users

import template
import data

remdb = data.ReminderDB()

class Handler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            d = {"loginurl": users.create_login_url("/")}
            self.response.out.write(template.Render("emptyhome.html", d))
            return
        tpl = {}
        tpl['user'] = user.nickname()
        tpl['logouturl'] = users.create_logout_url
        
        tpl['birthdays'] = []
        for rem in remdb.UpcomingReminders(user):
            tpl['birthdays'].append(rem.AsDict())

        self.response.out.write(template.Render("home.html", tpl))
