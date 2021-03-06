import datetime

from google.appengine.ext import db

class Months:
    _MONTH_NAMES = [
        "???",
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"]

    @staticmethod
    def Index(s):
        for i, m in enumerate(Months._MONTH_NAMES):
            if i != 0 and m.lower() == s.lower():
                return i
        return None

    @staticmethod
    def Name(i):
        if i < 1 or i > 12:
            return None
        return Months._MONTH_NAMES[i]

class Weekdays:
    _WEEKDAY_NAMES = [
        "Mon", "Tue", "Wed", "Thu",
        "Fri", "Sat", "Sun"]

    @staticmethod
    def Name(i):
        if i < 0 or i > 6:
            return None
        return Weekdays._WEEKDAY_NAMES[i]

class Reminder(db.Model):
    user = db.UserProperty()
    note = db.StringProperty()
    month = db.IntegerProperty()
    day = db.IntegerProperty()
    year = db.IntegerProperty()

    def AsDict(self):
        result = {}
        result['id'] = self.key()
        result['user'] = self.user
        result['note'] = self.note
        result['month'] = Months.Name(self.month or 0)
        result['day'] = self.day
        result['year'] = self.year or ""
        date = self.NextDate()
        result['weekday'] = Weekdays.Name(date.weekday())
        return result

    def NextDate(self):
        today = datetime.datetime.utcnow().date()
        date = datetime.date(year = today.year, day = self.day, month = self.month)
        if date < today:
            date.replace(year = date.year + 1)
        return date

class ReminderDB:
    to_send = Reminder.gql("WHERE day=:day AND month=:month")
    for_user = Reminder.gql("WHERE user=:user ORDER BY month,day")
    upcoming_this_month = Reminder.gql("WHERE user=:user " 
                                       "AND month=:month AND day >= :day "
                                       "ORDER BY day")
    upcoming_next_month = Reminder.gql("WHERE user=:user " 
                                       "AND month=:nextmonth AND day <= :day "
                                       "ORDER BY day")
    at_date = Reminder.gql("WHERE user=:user "
                           "AND month=:month AND day=:day")

    all_at_date = Reminder.gql("WHERE month=:month AND day=:day")

    def UpcomingReminders(self, current_user):
        now = datetime.datetime.utcnow().date()
        next = now.month % 12 + 1
        self.upcoming_this_month.bind(month = now.month,
                                      day = now.day,
                                      user = current_user)
        self.upcoming_next_month.bind(nextmonth = next,
                                      day = now.day,
                                      user = current_user)
        for result in self.upcoming_this_month:
            yield result

        for result in self.upcoming_next_month:
            yield result

    def UsersToRemind(self, today=None):
        week = datetime.timedelta(weeks = 1)
        if today is None:
            today = datetime.datetime.utcnow().date()
        in_a_week = today + week
        self.all_at_date.bind(month = today.month,
                              day = today.day)
        rems_today = list(self.all_at_date)

        self.all_at_date.bind(month = in_a_week.month,
                              day = in_a_week.day)
        rems_in_a_week = list(self.all_at_date)

        users = {}
        for rem in rems_today:
            users[rem.user] = 1
        for rem in rems_in_a_week:
            users[rem.user] = 1
        return users.keys()

    def RemindersToSend(self, current_user, today = None):
        week = datetime.timedelta(weeks = 1)
        if today is None:
            today = datetime.datetime.utcnow().date()
        in_a_week = today + week
        self.at_date.bind(month = today.month,
                          day = today.day,
                          user = current_user)
        rems_today = list(self.at_date)

        self.at_date.bind(month = in_a_week.month,
                          day = in_a_week.day,
                          user = current_user)
        rems_in_a_week = list(self.at_date)

        if not rems_in_a_week and not rems_today:
            return

        self.upcoming_this_month.bind(month = today.month,
                                      day = today.day,
                                      user = current_user)
        if in_a_week.month != today.month:
            self.upcoming_next_month.bind(nextmonth = in_a_week.month,
                                          day = in_a_week.day,
                                          user = current_user)
            for rem in self.upcoming_this_month:
                yield rem
            for rem in self.upcoming_next_month:
                yield rem
        else:
            for rem in self.upcoming_this_month:
                if rem.day <= in_a_week.day:
                    yield rem
                else:
                    return

    def RemindersForUser(self, current_user):
        self.for_user.bind(user = current_user)
        return self.for_user

remdb = ReminderDB()
