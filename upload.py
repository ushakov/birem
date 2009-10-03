from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users

import csv

import common
import template
import data

def GetMonthFromCSV(input):
    try:
        month = int(input)
        if month < 1 or month > 12:
            return None
        return month
    except ValueError:
        pass

    month = data.Months.Index(input)
    if month:
        return month

    return None

def GetNumber(input):
    try:
        return int(input)
    except ValueError:
        return None

class Handler(common.UserPageHandler):
    def DoGet(self):
        self.Reply("upload.html")

    def DoPost(self):
        uploaded_file = self.request.get("csv")
        uploaded_lines = uploaded_file.split("\n")
        if not uploaded_lines[-1]:
            uploaded_lines = uploaded_lines[:-1]
        csv_reader = csv.reader(uploaded_lines)
        line_no = 1
        entries_ok = 0
        for line in csv_reader:
            # ensure there are enough elements in line
            line.extend([""] * 5)
            rem = None
            if line[4]:
                key = line[4]
                try:
                    rem = data.Reminder.get(key)
                    if rem is None or rem.user != self.user:
                        rem = None
                except db.KindError:
                    rem = None
                except db.BadRequestError:
                    rem = None
            if rem is None:
                rem = data.Reminder()
            rem.user = self.user
            rem.day = GetNumber(line[0])
            rem.month = GetMonthFromCSV(line[1])
            rem.year = GetNumber(line[2])
            rem.note = line[3].decode("utf-8")
            if rem.day is None or rem.month is None:
                error = {}
                error['line'] = line_no
                error['day'] = line[0]
                error['month'] = line[1]
                error['year'] = line[2]
                error['comment'] = line[3]
                errors = self.tpl.setdefault('errors', [])
                errors.append(error)
            else:
                rem.put()
                entries_ok += 1
            line_no += 1

        self.tpl['done'] = entries_ok
        self.Reply("uploaddone.html")
        
