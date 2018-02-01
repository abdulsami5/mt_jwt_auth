#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'Django>1.9', 'pyJWT', 'djangorestframework'
]

setup_requirements = [
    # TODO(pss): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='mt_jwt_auth',
    version='0.1.0',
    description="JWT authentication for Django based multi-tenant (microservices)  services",
    long_description=readme + '\n\n' + history,
    author="pss",
    author_email='pogorelov.ss@gmail.com',
    url='https://github.com/Decorist/mt_jwt_auth',
    packages=find_packages(include=['mt_jwt_authentification']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mt_jwt_auth',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
