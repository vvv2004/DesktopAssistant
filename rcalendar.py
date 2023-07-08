import datetime
from enum import Enum
import datetime as dt
from exceptions.calendarex import InvalidType
from typing import List


# TODO
# Notifications about reminders
# Create JSON database that stores reminders, or use Firebase
# Migrate reminders
# Use schedule with Firebase
# Delete past reminders


class ReminderType(Enum):
    TASK = 1
    EVENT = 2
    REMINDER = 3


class Reminder:
    def __init__(self, rtype: ReminderType, title: str, description: str,
                 date: dt.date, time: datetime.time):
        self.type = rtype
        self.title = title
        self.description = description
        self.date = date
        self.time = time

    def remind(self, days_until):
        message = f'You have an {self.type} for {days_until}!' \
                  f'{self.description}'
        return message


def determine_type(rtype: str) -> ReminderType:
    uinput = rtype.lower()

    if uinput == 'event':
        return ReminderType.EVENT
    elif uinput == 'task':
        return ReminderType.TASK
    elif uinput == 'reminder':
        return ReminderType.REMINDER
    else:
        raise InvalidType('The type inputted is INVALID!')


month_to_string = [None, 'January', 'February', 'March',
                   'April', 'May', 'June',
                   'July', 'August', 'September',
                   'October', 'November', 'December']


class Calendar:
    def __init__(self):
        self._reminders: List[Reminder] = []
        self._past_reminders: List[Reminder] = []  # TODO

    def order_reminders(self):
        self._reminders.sort(key=lambda x: x.date)

    def add_reminder(self, rtype: str, title: str, description: str,
                     date: datetime.date, time=None):
        new_reminder = Reminder(determine_type(rtype), title, description, date, time)
        self._reminders.append(new_reminder)

    def check_all_reminders(self):
        # The database will delete reminders that are more than a year old
        first_month = self._past_reminders[0].date.month

    def check_upcoming_reminders(self, number_of_months: int):
        date = datetime.date.today()
        z = 0

        # ignoring past reminders
        while self._reminders[z].date.month != date.month:
            z += 1

        for i in range(number_of_months):
            current_month = date.month
            current_month_string = month_to_string[current_month]
            print(current_month_string)

            if self._reminders is None:
                print('No upcoming reminders')
                break

            while self._reminders[z].date.month == current_month:
                reminder = self._reminders[z]
                print(f'{reminder.type.__str__()}: {reminder.title} - {reminder.description}')
                print(f'Date: {reminder.date.day:02}:{reminder.date.month:02}:'
                      f'{reminder.date.year:02}\n')
                z += 1

                if z < self._reminders.__sizeof__():
                    if self._reminders[z].date.month != current_month:
                        break
                    continue
                else:
                    break

            # getting the next month, if the month is = 12, change the year
            if date.month == 12:
                date = date.replace(year=date.year + 1, month=1)
            else:
                date = date.replace(month=date.month + 1)
