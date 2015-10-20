#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'boto3',
]

test_requirements = [
    'boto3',
]

setup(
    name='storage_provisioner',
    version='0.1.0',
    description="Provisions storage on pluggable backends, such as AWS S3.",
    long_description=readme + '\n\n' + history,
    author="Chris Ballinger",
    author_email='chrisballinger@gmail.com',
    url='https://github.com/PerchLive/storage_provisioner',
    packages=[
        'storage_provisioner',
    ],
    package_dir={'storage_provisioner':
                 'storage_provisioner'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache License 2.0",
    zip_safe=False,
    keywords='storage_provisioner',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
