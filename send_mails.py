#!/usr/bin/python

import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import users

from google.appengine.api.labs import taskqueue

import datetime

import template
import data

mailqueue = taskqueue.Queue("mail")

class DispatchHandler(webapp.RequestHandler):
    def get(self):
        request_params = {}
        today = None
        if self.request.params.get('date'):
            param = self.request.params.get('date') 
            today = datetime.datetime.strptime(param, "%d-%m-%Y").date()
            request_params['date'] = param
        users = data.remdb.UsersToRemind(today)
        for user in users:
            request_params['user'] = user.email()
            task = taskqueue.Task(url="/mail/send", params=request_params)
            mailqueue.add(task)


class SendMailHandler(webapp.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        email = self.request.params['user']
        if not email:
            self.response.set_status("500")
            return
        try:
            user = users.User(email)
        except UserNotFoundError:
            self.response.set_status("500")
            return

        tpl = {}
        if self.request.params.get('date'):
            param = self.request.params.get('date') 
            today = datetime.datetime.strptime(param, "%d-%m-%Y").date()
        else:
            today = datetime.datetime.utcnow().date()
        tpl['date'] = {}
        tpl['date']['day'] = today.day
        tpl['date']['month'] = data.Months.Name(today.month)
        tpl['date']['year'] = today.year
        tpl['date']['weekday'] = data.Weekdays.Name(today.weekday)

        tpl['user'] = user.nickname()
        
        tpl['reminders'] = []
        for rem in data.remdb.RemindersToSend(user, today):
            if rem.day == today.day and rem.month == today.month:
                tpl['today'] = rem.AsDict()
            else:
                tpl['reminders'].append(rem.AsDict())

        mail_text = template.Render("mail.tpl", tpl)
        subject = template.Render("subject.tpl", tpl)
        mail.send_mail("ushmax@gmail.com", user.email(),
                       subject,
                       mail_text)
            
urlmap = [('/mail/dispatch', DispatchHandler),
          ('/mail/send', SendMailHandler)]

def main():
  application = webapp.WSGIApplication(urlmap,
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
