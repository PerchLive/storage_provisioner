#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_storage
----------------------------------

Tests for `storage` module.
"""
import os

import unittest

from storage_provisioner.storage import S3Storage
from storage_provisioner.provisioner import AWSS3Region
try:
    from tests.secrets import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
except ImportError:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    if AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None:
        raise EnvironmentError("AWS Credentials not present!")


class TestS3Storage(unittest.TestCase):

    S3_BUCKET_NAME = 'MrBucket'
    S3_BUCKET_REGION = AWSS3Region.APSouthEast1
    # provided by import:
    # AWS_ACCESS_KEY_ID
    # AWS_SECRET_ACCESS_KEY
    AWS_SESSION_TOKEN = 'TOKE_SESSION'
    AWS_EXPIRATION = 129599
    AWS_FEDERATED_USER_ID = 'FED_USER_ID'
    AWS_ARN = 'ARN'
    AWS_POLICY = 'policy'

    s3_storage = None

    def setUp(self):
        self.s3_storage = S3Storage(self.S3_BUCKET_NAME,
                                    self.S3_BUCKET_REGION,
                                    AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY,
                                    self.AWS_SESSION_TOKEN,
                                    self.AWS_EXPIRATION,
                                    self.AWS_FEDERATED_USER_ID,
                                    self.AWS_ARN,
                                    self.AWS_POLICY)
        pass

    def tearDown(self):
        pass

    def test_s3_storage(self):
        self.assertEqual(self.s3_storage.s3_bucket_name, self.S3_BUCKET_NAME)
        self.assertEqual(self.s3_storage.s3_bucket_region, self.S3_BUCKET_REGION)
        self.assertEqual(self.s3_storage.aws_access_key_id, AWS_ACCESS_KEY_ID)
        self.assertEqual(self.s3_storage.aws_secret_access_key, AWS_SECRET_ACCESS_KEY)
        self.assertEqual(self.s3_storage.aws_session_token, self.AWS_SESSION_TOKEN)
        self.assertEqual(self.s3_storage.aws_expiration, self.AWS_EXPIRATION)
        self.assertEqual(self.s3_storage.aws_federated_user_id, self.AWS_FEDERATED_USER_ID)
        self.assertEqual(self.s3_storage.aws_arn, self.AWS_ARN)

if __name__ == '__main__':
    import sys

    sys.exit(unittest.main())
