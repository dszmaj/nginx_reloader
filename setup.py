#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'watchdog',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='nginx_reloader',
    version='0.1.0',
    description="Given path to config directory gracefully reloads nginx workers with no interruption of service.",
    long_description=readme + '\n\n' + history,
    author="Dominik Szmaj",
    author_email='dszmaj@gmail.com',
    url='https://github.com/dszmaj/nginx_reloader',
    packages=[
        'nginx_reloader',
    ],
    package_dir={'nginx_reloader':
                 'nginx_reloader'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='nginx',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={'console_scripts': [
        'nginxreloadin = nginx_reloader.nginx_reloader:main',
    ]},
    test_suite='tests',
    tests_require=test_requirements
)
