#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session=False)
install_reqs_test = parse_requirements('requirements_dev.txt', session=False)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [str(ir.req) for ir in install_reqs]

setup_requirements = [
    # TODO: put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
    str(ir.req) for ir in install_reqs_test
]

setup(
    name='mt_jwt_auth',
    version='0.1.0',
    description="JWT authentication for Django based multi-tenant (microservices)  services",
    long_description=readme + '\n\n' + history,
    author="pss",
    author_email='pogorelov.ss@gmail.com',
    url='https://github.com/Decorist/mt_jwt_auth',
    packages=find_packages(include=['mt_jwt_auth']),
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
