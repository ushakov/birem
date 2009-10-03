from google.appengine.ext import webapp
from google.appengine.api import users

import common
import template
import data

class Handler(common.UserPageHandler):
    def DoGet(self):
        self.Reply("upload.html")

    def DoPost(self):
        s = self.request.get("csv")
        self.tpl['debug'] = "File:\n" + s + "\n"
        self.Reply("upload.html")
        
