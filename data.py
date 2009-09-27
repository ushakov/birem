import datetime

from google.appengine.ext import db

class Reminder(db.Model):
    user = db.UserProperty()
    note = db.StringProperty()
    month = db.IntegerProperty()
    day = db.IntegerProperty()
    year = db.IntegerProperty()
    remind_hour = db.IntegerProperty()

    _MONTH_NAMES = [
        "",
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"]

    def AsDict(self):
        result = {}
        result['user'] = self.user
        result['note'] = self.note
        result['month'] = self._MONTH_NAMES[self.month]
        result['day'] = self.day
        result['year'] = self.year or "--"
        result['remind_hour'] = self.remind_hour + ":00 GMT"

class ReminderDB:
    to_send = Reminder.gql("WHERE day=:day AND month=:month AND hour=:hour")
    for_user = Reminder.gql("WHERE user=:user ORDER BY month,day")
    upcoming_this_month = Reminder.gql("WHERE user=:user " 
                                       "AND month=:month AND day >= :day "
                                       "ORDER BY day")
    upcoming_next_month = Reminder.gql("WHERE user=:user " 
                                       "AND month=:nextmonth AND day <= :day "
                                       "ORDER BY day")

    def RemindersToSend(self):
        now = datetime.datetime.today()
        return self.to_send.bind(day = now.day, month = now.month, hour = now.hour)

    def UpcomingReminders(self, current_user):
        now = datetime.datetime.today()
        next = now.month % 12 + 1
        this_month = self.upcoming_this_month.bind(month = now.month,
                                                   day = now.day,
                                                   user = current_user)
        next_month = self.upcoming_next_month.bind(month = next,
                                                   day = now.day,
                                                   user = current_user)
        if this_month is not None:
            for result in this_month:
                yield result

        if next_month is not None:
            for result in next_month:
                yield result

    def RemindersForUser(self, current_user):
        return self.for_user.bind(user = current_user)
