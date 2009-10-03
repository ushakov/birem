from google.appengine.ext import webapp
from google.appengine.api import users

import common
import template
import data

class Handler(common.UserPageHandler):
    def DoGet(self):
        self.Reply("upload.html")

    def DoPost(self):
        s = self.request.body
        self.tpl['debug'] = "File:\n" + s + "\n"
        for i in self.request.params:
            self.tpl['debug'] += i + ": " + self.request.params[i] + "\n"

        for i in self.request.headers:
            self.tpl['debug'] += i + ": " + self.request.headers[i] + "\n"

        for i in self.request.body_file:
            self.tpl['debug'] += i  + "\n"

        self.Reply("upload.html")
        
