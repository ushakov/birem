#!/usr/bin/python

import wsgiref.handlers
from google.appengine.ext import webapp

import home
import add
import manage

urlmap = [('/', home.Handler),
          ('/add', add.Handler),
          ('/manage', manage.Handler)]
def main():
  application = webapp.WSGIApplication(urlmap,
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
