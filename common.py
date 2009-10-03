from google.appengine.ext import webapp
from google.appengine.api import users

import template

def FillCommon(tpl, user):
    tpl['user'] = user.nickname()
    tpl['logouturl'] = users.create_logout_url("/")

class UserPageHandler(webapp.RequestHandler):
    user = None
    tpl = {}

    def Reply(self, tpl_name):
        self.response.out.write(template.Render(tpl_name, self.tpl))
    
    def get(self):
        self.tpl = {}
        self.user = users.get_current_user()
        if not self.user:
            self.redirect("/")
            return
        FillCommon(self.tpl, self.user)
        self.DoGet()

    def post(self):
        self.tpl = {}
        self.user = users.get_current_user()
        if not self.user:
            self.redirect("/")
            return
        FillCommon(self.tpl, self.user)
        self.DoPost()

