# diapy
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
You can save your today's diary without inputing dates.

    >>> d.new('Today is a good day!')
    >>>
If you forget to write a diary yesterday, you can give a datetime object to the function.

    >>> from datetime import datetime
    >>> yesterday = datetime(2018, 8, 11, 19, 34)
    >>> d.new('OOPS, I forgot to write my diary yesterday!', yesterday)
    2018-08-11 19:34:00 Friday
    OOPS, I forgot to write my diary yesterday!
    >>>
You can access your diary by a 8 digit number.

    >>> d[20180812]
    2018-08-12 18:37:02 Saturday
    Today is a good day!
You can change your password.
(Not working if you forget your password. 2333)

    >>> d.change_pwd()
    Please input the new password: 
    >>>
Exporting and importing diaries. It is often used when you wanted to do something directly to your diary.

**Notice! It will expose your secrets! Import operation will overwrite your current diary!**

    >>> d.export_content()
    {1534070222: 'Today is a good day!'}
    >>> d.import_content({1534070222: 'Today is a bad day!'})
    >>>
To get a random diary entry.

    >>> d.random()
    2018-08-12 18:37:02 Saturday
    Today is a good day!
    >>>
When all done, you can close the file. (Or you can just close the terminal.)

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
