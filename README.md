# StorageProvisioner

[![Build Status](https://img.shields.io/travis/PerchLive/storage_provisioner.svg)](https://travis-ci.org/PerchLive/storage_provisioner) [![PyPI Page](https://img.shields.io/pypi/v/storage_provisioner.svg)](https://pypi.python.org/pypi/storage_provisioner)

Provisions storage on pluggable backends, such as AWS S3.

## Installation

    $ pip3 install storage_provisioner
    
## Dependencies

* Python 3.5
* [boto3](https://github.com/boto/boto3) - AWS library 

## Usage

```python
import storage_provisioner
```

## Features

* AWS S3 backend

## TODO

* Local file storage backend
* FTP backend
* RTMP backend
* Your backend?

## Authors

* [Chris Ballinger](https://github.com/chrisballinger)
* [David Brodsky](https://github.com/onlyinamerica)


## License

Apache 2.0

```
Copyright 2015 Perch Innovations, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```