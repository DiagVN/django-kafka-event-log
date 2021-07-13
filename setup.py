#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import setuptools
from setuptools import setup
from setuptools.command.install import install

# must match git tag to release
VERSION = '0.1.6'


def readme():
    """print long description"""
    with open('README.rst') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = f'Git tag: {tag} does not match the version of this app: {VERSION}'
            sys.exit(info)


setup(
    name='django-kafka-event-log',
    version=VERSION,
    description='A Django app to store an event and publish the event to Kafka',
    long_description=readme(),
    author='Diag',
    author_email='ngu.truong@diag.vn',
    url="https://github.com/DiagVN/django-kafka-event-log",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=setuptools.find_packages(where="./"),
    keywords='django kafka event-log',
    python_requires='>=3',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
