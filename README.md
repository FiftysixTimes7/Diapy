# diapy
>Version 3.0.0

A small diary manager based on python.

Diapy uses `cryptography.fernet` to encrypt your top secret.

## Installation
Simple, crude.

    pip install diapy
	
## Usage
Firstly, you need to create a new diary file. Or you can open an exist file. There isn't much difference.

    >>> from diapy import Diary
    >>> d = Diary('new.diary')
    Please input the main password: # Enter your password here! No one will see it.
    >>>
You can keep your today's diary without inputing dates.

    >>> d.new('Today is a good day!')
    2018-08-12 18:37:02 Sunday
    Today is a good day!
    >>>
If you have written a diary on the same day, you will be asked to choose.

    >>> d.new('I forget writing diary or not.')
    You have written a diary today:
    2018-08-12 18:37:02 Sunday
    Today is a good day!

    Do you want to overwrite, discard changes or merge them together?
    (overwrite/discard/merge) Default: discard
    merge # If you input merge, diapy will keep your diary after the previous one. The time will use the current one.
    2018-08-12 19:18:07 Sunday
    Today is a good day!
    I forget writing diary or not.
If you forget to write a diary yesterday, you can give a datetime object to the function.

    >>> from datetime import datetime
    >>> yesterday = datetime(2018, 8, 11, 19, 34)
    >>> d.new('OOPS, I forgot to write my diary yesterday!', yesterday)
    2018-08-11 19:34:00 Saturday
    OOPS, I forgot to write my diary yesterday!
    >>>
You can access your diary by a 8 digit key.

    >>> d[20180812]
    2018-08-12 18:37:02 Sunday
    Today is a good day!
    >>>
Actually, it returns an `Entry` object.

    >>> e = d[20180812]
    >>> e.timestamp
    1534072687
    >>> e.content
    'Today is a good day!\nI forget writing diary or not.'
    >>>
If you wonders how many diaries you have written, you can use the `key` function.

    >>> d.key()
    [20180812, 20180811]
    >>>
You can change your password.
(Not working if you forget your password. 2333)

    >>> d.change_pwd()
    Please input the new password: 
    >>>
To get a random diary entry.

    >>> d.random()
    2018-08-12 19:18:07 Sunday
    Today is a good day!
    I forget writing diary or not.
    >>>
Search text in your diaries.

    >>> d.search('day')
    2018-08-12 19:18:07 Sunday
    Today is a good day!
    I forget writing diary or not.

    2018-08-11 19:34:00 Saturday
    OOPS, I forgot to write my diary yesterday!

    >>>
Exporting and importing diaries. It is often used when you wanted to do something directly to your diary. It is **not recommended** in most cases.

**Notice! It will expose your secrets! Import operation will overwrite your current diary!**

    >>> d._content
    {1534072687: 'Today is a good day!\nI forget writing diary or not.', 1533987240: 'OOPS, I forgot to write my diary yesterday!'}
    >>> d._content = {1534072687: 'Today is a bad day!\nI forget writing diary or not.', \
    ...     1533987240: 'OOPS, I forgot to write my diary yesterday!'}
    >>>
When all done, save changes by the close function.

**Don't exit without the close function! Or your changes will not be saved.**

    >>> d.close()
    >>>
## About
I am a secondary school student in China, and **I know my English is not very good**. So if someone wants to **improve this** I will thank a lot!
## About(Chinese)

## Contributing
I know, my code is bad too... You can improve it any time you want. I will wait for your pull requests!

## Donating
...OK. That's unbeleavable that you will donate to my rough code...

I don't even have an account for donating 233. If you want to encourage me, you can choose to give me some advice.~
