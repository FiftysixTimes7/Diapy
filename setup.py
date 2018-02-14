#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='Diapy',
    version='2.3.1',
    description='A rough diary manager based on python.',
    url='https://github.com/FiftysixTimes7/Diapy',
    author='FiftysixTimes7(PTJ)',
    author_email='pangtj26@163.com',
    license='MIT',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Utilities'],
    keywords='diary',
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['cryptography']
)
