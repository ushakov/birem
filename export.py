from google.appengine.ext import webapp
from google.appengine.api import users

import csv
import StringIO

import data
import common

remdb = data.ReminderDB()

class Handler(common.UserPageHandler):
    def DoGet(self):
        rems = remdb.RemindersForUser(self.user)
        self.tpl['lines'] = []
        for rem in rems:
            stringfile = StringIO.StringIO()
            formatter = csv.writer(stringfile)
            values = []
            values.append(rem.day)
            values.append(rem.month)
            if rem.year is not None:
                values.append(rem.year)
            else:
                values.append("")
            if rem.note is not None:
                values.append(rem.note.encode("utf-8"))
            else:
                values.append("")
            formatter.writerow(values)
            csv_line = stringfile.getvalue()
            self.tpl['lines'].append(csv_line)
        self.response.headers["Content-Type"] = "text/csv"
        self.response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        self.Reply("export.html")
