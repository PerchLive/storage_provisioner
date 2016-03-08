#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='storage_provisioner',
    version='0.1.1',
    description="Provisions storage on pluggable backends, such as AWS S3.",
    long_description=readme + '\n\n' + history,
    author="Chris Ballinger, David Brodsky",
    author_email='chrisballinger@gmail.com, dbro@dbro.pro',
    url='https://github.com/PerchLive/storage_provisioner',
    download_url='https://github.com/PerchLive/storage_provisioner/tarball/0.1',
    packages=[
        'storage_provisioner',
    ],
    package_dir={'storage_provisioner':
                 'storage_provisioner'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache License 2.0",
    zip_safe=False,
    keywords='storage_provisioner, aws, boto',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=requirements
)
