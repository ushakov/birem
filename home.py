from google.appengine.ext import webapp
from google.appengine.api import users

import common
import template
import data

class Handler(webapp.RequestHandler):
    user = None
    tpl = {}

    def Reply(self, tpl_name):
        self.response.out.write(template.Render(tpl_name, self.tpl))
    
    def get(self):
        self.tpl = {}
        self.user = users.get_current_user()
        if not self.user:
            self.tpl['loginurl'] = users.create_login_url("/")
            self.Reply("emptyhome.html")
            return
        common.FillCommon(self.tpl, self.user)
        self.tpl['reminders'] = []
        for rem in data.remdb.UpcomingReminders(self.user):
            self.tpl['reminders'].append(rem.AsDict())
        self.Reply("home.html")
