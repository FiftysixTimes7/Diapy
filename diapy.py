import base64
import getpass
import hashlib
import os
import pickle
import pickletools
import random
import re
from datetime import datetime
from cryptography.fernet import Fernet

__version__ = '3.0.0a'


def _opened(func):
    def wrapper(*arg, **kw):
        if not arg[0].closed:
            return func(*arg, **kw)
        else:
            raise ValueError('File closed.')
    return wrapper


class Diary(object):
    # Class the instance which will be returned in get function.
    class Entry(object):
        def __init__(self, timestamp, content):
            self.timestamp = timestamp
            self.content = content

        def __str__(self):
            datetimeobj = datetime.fromtimestamp(self.timestamp)

            # Calculate date and weekday.
            date = datetimeobj.date()
            weekdays = ['Monday', 'Tuesday', 'Wednesday',
                        'Thursday', 'Friday', 'Saturday', 'Sunday']

            return str(datetimeobj) + ' ' + \
                weekdays[datetime.weekday(date) - 1] + '\n' + self.content

        __repr__ = __str__

    def __init__(self, path):
        self.path = path
        self.closed = False

        self._input_pwd('Please input the main password: ')

        # If path doesn't exist, create a new file.
        if not os.path.exists(self.path):
            with open(self.path, 'wb'):
                pass

        with open(self.path, 'rb') as f:
            text = f.read()

        # Check if this is a new file.
        if text == b'':
            self._content = {}
            self._save()
        else:
            f = Fernet(self._key)
            self._content = pickle.loads(
                f.decrypt(base64.urlsafe_b64encode(text)))

    @_opened
    def __getitem__(self, item):
        timestamp = self.key(item)
        if self._content.get(timestamp) is None:
            return None
        else:
            content = self._content[timestamp]
            return self.Entry(timestamp, content)

    def _input_pwd(self, text):
        pwd = getpass.getpass(text)

        self._key = base64.urlsafe_b64encode(
            hashlib.sha256(pwd.encode('utf-8')).digest())

    @_opened
    def change_pwd(self):
        self._input_pwd('Please input the new password: ')
        self._save()

    @_opened
    def _save(self):
        f = Fernet(self._key)
        with open(self.path, 'wb') as file:
            # Dump, optimize, encrypt, decode.
            file.write(base64.urlsafe_b64decode(f.encrypt(
                pickletools.optimize(pickle.dumps(self._content, 4)))))

    def close(self):
        self._key = None
        self._content = None
        self.closed = True

    @_opened
    def key(self, date=None):
        table = {}
        for key in self._content.keys():
            # Convert to an 8 digest int
            date = int(datetime.fromtimestamp(
                key).date().strftime('%Y%m%d'))
            table[date] = key

        if date:
            return table[date]
        else:
            return list(table.keys())

    @_opened
    def new(self, content, datetimeobj=None):
        if not datetimeobj:
            datetimeobj = datetime.now()

        date = int(datetimeobj.timestamp())
        self._content[date] = content
        self._save()

        print(self[date])

    @_opened
    def export_content(self):
        return self._content

    @_opened
    def import_content(self, content):
        print('This will over-write your current file. '
              'Do you want to continue?(y/n)')
        c = input()
        if c == 'y':
            self._content = content
            self._save()

    @_opened
    def random(self):
        return self[random.choice(list(self._content.keys()))]
