import csv
import sys

class Reminder(object):
    def __init__(self):
        self.day = None
        self.month = None
        self.year = None
        self.comment = None

def ParseReminder(input):
    (date, year, comm) = input.split(' ', 2)
    (month, day) = date.split('-')
    if year == "-":
        year = None
    reminder = Reminder()
    reminder.day = day
    reminder.month = month
    reminder.year = year
    reminder.comment = comm
    return reminder

def WriteLine(writer, reminder):
    row = []
    row.append(reminder.day)
    row.append(reminder.month)
    if reminder.year:
        row.append(reminder.year)
    else:
        row.append("")
    row.append(reminder.comment)
    writer.writerow(row)

def main(args):
    inp = open(args[1], "r")
    out = csv.writer(open(args[2], "w"))
    for line in inp:
        line = line.strip()
        reminder = ParseReminder(line)
        WriteLine(out, reminder)
        
    

if __name__ == "__main__":
    main(sys.argv)
