#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diary Managing System
Version Release 2.2.3
"""

__author__ = 'FiftysixTimes7(PTJ)'
__version__ = 'Release 2.2.3'


class Diary(object):
    # Class the instance which will be returned in get function.
    class DiarySpecific(object):
        def __init__(self, path, content, tags, mood, date, time, location, weather, temperature, file):
            self._path = path
            self.content = content
            self.tags = tags
            self.mood = mood
            self.date = date
            self.time = time
            self.location = location
            self.weather = weather
            self.temperature = temperature
            self.file = file

        def __str__(self):
            r = ''

            # Calculate date and weekday.
            import datetime
            date = datetime.datetime.strptime(self.date, '%Y%m%d')
            date = datetime.date(date.year, date.month, date.day)
            week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            r += 'Date: ' + str(date) + ' ' + week[datetime.date.weekday(date)] + '\n'
            r += 'Time: ' + self.time + '\n'
            r += 'Location: ' + str(self.location) + '\n'
            r += 'Weather: ' + self.weather + '\n'
            r += 'Temperature: ' + str(self.temperature) + ' Degree Celsius\n'
            r += 'Mood: ' + self.mood + '\n'
            if self.file:
                r += 'Extra-File: ' + self.file['name'] + '\n'
            r += 'Tags: ' + str(self.tags) + '\n'
            r += 'Content: ' + self.content
            return r

        __repr__ = __str__

        def save_file(self):
            if not self.file:
                raise FileNotFoundError('No file for this diary.')
            else:
                with open(self._path[:self._path.strip('\\').rfind('\\') + 1] + self.file['name'], 'wb') as f:
                    f.write(self.file['content'])

    def __init__(self, path):
        self.path = path

        # Call several function to open file.
        self._input_pwd('Please input the main password: ')
        self._open_file()
        self.check()

    def __getitem__(self, item):
        return self.get(item)

    def _input_pwd(self, text):
        # Input password.
        import msvcrt
        pwd = b''
        print(text, end='\r')
        while True:
            t = msvcrt.getch()
            if t == b'\r':
                break
            elif t == b'\x08':
                pwd = pwd[:-1]
            else:
                pwd += t
            print(text, '*' * len(pwd), end=' \r')
        print()

        # Process password to key.
        import hashlib
        import base64
        self._key = base64.urlsafe_b64encode(hashlib.sha256(pwd).digest())

    def change_pwd(self):
        self.check()
        self._input_pwd('Please input the new password: ')
        self._status = 'Unsaved'

    def _crypt(self, mode, text):
        from cryptography.fernet import Fernet
        f = Fernet(self._key)
        if mode in ['Encrypt', 'e', 'E', 'encrypt']:
            return f.encrypt(text)
        if mode in ['Decrypt', 'd', 'D', 'decrypt']:
            return f.decrypt(text)

    def _open_file(self):
        import os
        import pickle
        import zlib
        import base64
        # Extract data.
        if not os.path.exists(self.path):
            with open(self.path, 'wb'):
                pass
        with open(self.path, 'rb') as f:
            text = f.read()

        # Check if this is a new file.
        if text == b'':
            import datetime
            info = input('Diary info: ')
            self._content = {'info': info, 'date': str(datetime.date.today()),
                             'version': __version__, 'data': {}}
            self._status = 'Unsaved'
        else:
            text = self._crypt('d', base64.urlsafe_b64encode(text))
            self._content = pickle.loads(zlib.decompress(text))

            # Print information.
            print(f'Diary Managing System Version {__version__}')
            print('File:', self._content['info'], self._content['date'])

            self._status = 'Saved'

    def save(self):
        self.check()

        # Edit version.
        if self._content['version'] != __version__:
            self._content['version'] = __version__

        import pickle
        import pickletools
        import zlib
        import base64
        with open(self.path, 'wb') as f:
            # Dump, optimize, compress, encrypt, decode.
            f.write(base64.urlsafe_b64decode(self._crypt('e', zlib.compress(
                pickletools.optimize(pickle.dumps(self._content, 4))))))
        self._status = 'Saved'

    def close(self):
        # Check if saved.
        if self._status == 'Unsaved':
            import msvcrt
            print('Do you want to save the file before closing it?(y/n/c(cancel))')
            c = msvcrt.getch()
            print(c.decode('utf-8'))
            if c == b'y':
                self.save()
            elif c == b'c':
                return

        # Delete data.
        self._key = None
        self._content = None
        self._status = 'Closed'

    def check(self):
        if self._status == 'Closed':
            raise ValueError('File closed.')
        elif not hasattr(self, '_key') or not isinstance(self._key, bytes):
            raise ValueError('Key error.')
        elif not hasattr(self, '_content') or not isinstance(self._content, dict):
            raise ValueError('Context error.')
        else:
            # Version check.
            v = self._content.get('version')
            if not v:
                v = self._content['info']
                v = v[v.rfind(' ', 0, v.rfind(' ')) + 1:]
            if v != __version__:
                print(f'''Warning: File created by DMS v{v} may not be open properly on current version.
Please adjust the file manually.
If you update the file correctly, the version will auto change into current one.
You can use the export_all() and import_all() to export/import data.''')
                self._status = 'Unsaved'
            return self._status

    def get(self, dates):
        self.check()

        if isinstance(dates, int):
            dates = str(dates)
        if isinstance(dates, str):
            if self._content['data'].get(dates) is None:
                return None
            d = self._content['data'][dates]
            return self.DiarySpecific(self.path, d['content'], d['tags'], d['mood'], dates, d['time'],
                                      d['location'], d['weather'], d['temperature'], d['file'])
        else:
            # Get several dates in a list.
            r = []
            for date in dates:
                if isinstance(date, int):
                    date = str(date)
                if self._content['data'].get(date) is None:
                    r.append(None)
                d = self._content['data'][date]
                r.append(self.DiarySpecific(self.path, d['content'], d['tags'], d['mood'], date, d['time'],
                                            d['location'], d['weather'], d['temperature'], d['file']))

    def ls(self, mode, value=None, specific=True):
        self.check()
        r = {}

        # Check the value.
        if isinstance(value, int):
            value = str(value)
            if len(value) == 1:
                value = '0' + value

        if mode == 'year':
            if value is None:
                for k in self._content['data']:
                    if k[:4] not in r:
                        r[k[:4]] = [k]
                    else:
                        r[k[:4]].append(k)
            else:
                for k in self._content['data']:
                    if k[:4] == value:
                        if k[4:6] not in r:
                            r[k[4:6]] = [k]
                        else:
                            r[k[4:6]].append(k)
        elif mode == 'month':
            if value is None:
                for k in self._content['data']:
                    if k[4:6] not in r:
                        r[k[4:6]] = [k]
                    else:
                        r[k[4:6]].append(k)
            else:
                for k in self._content['data']:
                    if k[6:] == value:
                        if k[6:] not in r:
                            r[k[6:]] = [k]
                        else:
                            r[k[6:]].append(k)
        elif mode == 'date':
            if value is None:
                for k in self._content['data']:
                    if k[6:] not in r:
                        r[k[6:]] = [k]
                    else:
                        r[k[6:]].append(k)
            else:
                for k in self._content['data']:
                    if k[6:] == value:
                        if k[6:] not in r:
                            r[k[6:]] = [k]
                        else:
                            r[k[6:]].append(k)
        elif mode == 'tags':
            if value is None:
                for k in self._content['data']:
                    for t in self._content['data'][k]['tags']:
                        if t not in r:
                            r[t] = [k]
                        else:
                            r[t].append(k)
            else:
                for k in self._content['data']:
                    for t in self._content['data'][k]['tags']:
                        if t == value:
                            if t not in r:
                                r[t] = [k]
                            else:
                                r[t].append(k)
        elif mode == 'mood':
            if value is None:
                for k in self._content['data']:
                    if self._content['data'][k]['mood'] not in r:
                        r[self._content['data'][k]['mood']] = [k]
                    else:
                        r[self._content['data'][k]['mood']].append(k)
            else:
                for k in self._content['data']:
                    if self._content['data'][k]['mood'] == value:
                        if self._content['data'][k]['mood'] not in r:
                            r[self._content['data'][k]['mood']] = [k]
                        else:
                            r[self._content['data'][k]['mood']].append(k)
        elif mode == 'location':
            if value is None:
                for k in self._content['data']:
                    if self._content['data'][k]['location'] not in r:
                        r[self._content['data'][k]['location']] = [k]
                    else:
                        r[self._content['data'][k]['location']].append(k)
            else:
                for k in self._content['data']:
                    if self._content['data'][k]['location'] == value:
                        if self._content['data'][k]['location'] not in r:
                            r[self._content['data'][k]['location']] = [k]
                        else:
                            r[self._content['data'][k]['location']].append(k)
        elif mode == 'weather':
            if value is None:
                for k in self._content['data']:
                    if self._content['data'][k]['weather'] not in r:
                        r[self._content['data'][k]['weather']] = [k]
                    else:
                        r[self._content['data'][k]['weather']].append(k)
            else:
                for k in self._content['data']:
                    if self._content['data'][k]['weather'] == value:
                        if self._content['data'][k]['weather'] not in r:
                            r[self._content['data'][k]['weather']] = [k]
                        else:
                            r[self._content['data'][k]['weather']].append(k)

        if not specific:
            for k in r:
                r[k] = len(r[k])

        return r

    def edit(self, date, key, value):
        self.check()
        if not isinstance(date, str):
            date = str(date)
            self._content['data'][date][key] = value
        self._status = 'Unsaved'

    def delete(self, date):
        self.check()
        if not isinstance(date, str):
            date = str(date)
        self._status = 'Unsaved'
        return self._content['data'].pop(date)

    def new(self, content, tags, mood, date=None, time=None, location=None, weather=None, temperature=None,
            file=None):
        import re
        self.check()

        def get_time(mode):
            import datetime
            dateobj = datetime.datetime.now()
            if mode == 'date':
                return str(dateobj.year) + str(dateobj.month).rjust(2, '0') + str(dateobj.day).rjust(2, '0')
            elif mode == 'time':
                return str(dateobj.hour).rjust(2, '0') + ':' + str(dateobj.minute).rjust(2, '0')

        if time is None:
            time = get_time('time')
        elif re.match(r'\d{2}:\d{2}', time) is None:
            raise ValueError('Expected form of time: M:S, got: ' + time)

        def url_get(url):
            from urllib import request
            c = 10
            while True:
                try:
                    with request.urlopen(url) as f:
                        txt = f.read()
                    return txt
                except:
                    if c <= 0:
                        c = input('Url:' + url + ' fetch error.' +
                                  ' Do you want to try another 10 times? y/n ')
                        if c in ['y', 'yes', 'Y' 'Yes']:
                            c = 10
                            continue
                        else:
                            break
                    c = c - 1
                    continue

        def get_ip():
            import re
            txt = url_get('http://ip.chinaz.com/getip.aspx')
            return re.search(rb'\d+\.\d+\.\d+\.\d+', txt).group().decode('utf-8')

        def get_location():
            # Accurate to city.
            txt = url_get('http://ip.taobao.com/service/getIpInfo.php?ip=' + get_ip()).decode('utf-8')
            import json
            d = json.loads(txt)
            address = d['data']['country'] + d['data']['city']
            return address

        if location is None:
            location = get_location()

        def get_weather(mode):
            from geopy.geocoders import Nominatim
            import geopy.exc
            locator = Nominatim()
            try:
                loc = locator.geocode(location)
            except geopy.exc:
                # When geocoders are not working and raising an error:
                if isinstance(location, dict):
                    if location.get('latitude') is None or location.get('logitude') is None:
                        loc = None
                    else:
                        from collections import namedtuple
                        LocWrap = namedtuple('LocWrap', ['latitude', 'longitude'])
                        loc = LocWrap(location['latitude'], location['longitude'])
                else:
                    loc = None

            # Check if the get_location function returns the proper value and the locator can locate the address.
            import msvcrt
            while not loc:
                print('Locate failed. Searched address: ' + location)
                print('Retry(r) or Skip(s) or Type address(a) or Type latitude and longitude(l)?')
                c = msvcrt.getch()
                print(c.decode('utf-8'))
                if c == b'r':
                    loc = locator.geocode(location)
                    continue
                elif c == b's':
                    if mode == 'weather':
                        return input('Please type the weather: ')
                    elif mode == 'temperature':
                        return input('Please type the temperature: ')
                elif c == b'a':
                    loc = locator.geocode(input('Please input the address: '))
                elif c == b'l':
                    loc = dict()
                    loc['latitude'] = input('Please input the latitude: ')
                    loc['longitude'] = input('Please input the longitude: ')
                    break

            txt = url_get('http://api.openweathermap.org/data/2.5/weather?lang=zh_cn&units=metric' +
                          '&appid=fad990484bb470678c2cd31936006982&lat=' + str(loc.latitude) +
                          '&lon=' + str(loc.longitude)).decode('utf-8')
            import json
            txt = json.loads(txt)
            if mode == 'weather':
                return txt['weather'][0]['description']
            elif mode == 'temperature':
                return str(txt['main']['temp'])

        r = dict()

        r['time'] = time

        r['location'] = location

        if weather is None:
            r['weather'] = get_weather('weather')
        else:
            r['weather'] = weather

        if temperature is None:
            r['temperature'] = get_weather('temperature')
        else:
            r['temperature'] = temperature

        r['tags'] = tags
        r['content'] = content
        r['mood'] = mood

        if file:
            import os
            if os.path.isfile(file):
                text = {'name': file[file.strip('\\').rfind('\\') + 1:]}
                with open(file, 'rb') as f:
                    text['content'] = f.read()
            else:
                print('File not exist. Will not add file into diary.')
                text = {}
        else:
            text = {}
        r['file'] = text

        if date is None:
            date = get_time('date')
            self._content['data'][date] = r
        else:
            if not isinstance(date, str):
                date = str(date)
            if re.match(r'\d{8}', date) is None:
                raise ValueError('Expected form of date: yyyyMMdd, got: ' + date)
            self._content['data'][date] = r

        self._status = 'Unsaved'

        print(self.get(date))

    def recollect(self):
        self.check()
        r = {}
        from datetime import datetime, timedelta
        t = datetime.today()
        t1 = t - timedelta(weeks=1)

        s = str(t1.year) + str(t1.month).rjust(2, '0') + str(t1.day).rjust(2, '0')
        r['a week ago'] = self.get(s)

        if t.month == 1:
            s = str(t.year - 1) + '12' + str(t.day).rjust(2, '0')
        else:
            s = str(t.year) + str(t.month - 1).rjust(2, '0') + str(t.day).rjust(2, '0')
        r['a month ago'] = self.get(s)

        min_year = int(sorted(list(self.ls('year').keys()), key=int)[0])
        for year in range(min_year, t.year):
            s = str(year) + str(t.month).rjust(2, '0') + str(t.day).rjust(2, '0')
            r['today in {}'.format(year)] = self.get(s)

        # Pop None.
        keys = list(r.keys())
        for k in keys:
            if r[k] is None:
                r.pop(k)
        return r

    def export_all(self):
        self.check()
        r = self._content

        # Ask if export the key.
        import msvcrt
        print('Do you want to export the key?(y/n)')
        c = msvcrt.getch()
        print(c.decode('utf-8'))
        if c == b'y':
            r['key'] = self._key

        return r

    def import_all(self, content):
        self.check()

        # Confirm.
        import msvcrt
        print('This will over-write your current file. Do you want to continue?(y/n)')
        c = msvcrt.getch()
        print(c.decode('utf-8'))
        if c == b'y':
            if content.get('key'):
                # Ask if import the key.
                import msvcrt
                print('Do you want to import the key?(y/n)')
                c = msvcrt.getch()
                print(c.decode('utf-8'))
                if c == b'y':
                    self._key = content.pop('key')
            self._content = content
            self._status = 'Unsaved'

    def get_random(self):
        self.check()
        import random
        return self.get(random.choice(list(self._content['data'].keys())))