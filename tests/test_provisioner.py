#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_provisioner
----------------------------------

Tests for `provisioner` module.
"""
import os
import unittest

from boto3.session import Session
from botocore.exceptions import ClientError

from storage_provisioner.provisioner import S3StorageProvisioner

try:
    from tests.secrets import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
except ImportError:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    if AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None:
        raise EnvironmentError("AWS Credentials not present!")


class TestS3StorageProvisioner(unittest.TestCase):
    s3_provisioner = None

    def setUp(self):
        self.s3_provisioner = S3StorageProvisioner(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    def tearDown(self):
        pass

    def test_provision_storage_default_policy(self):
        bucket_name = '9a5bb25e-783a-11e5-86ba-b8f6b11601af'
        tmp_download_path = '/tmp/hello.txt'
        test_file_name = 'test.txt'
        test_file_contents = 'hello.'.encode()
        user_name = 'test_user'
        storage_path = 'path/to/test/'

        unscoped_storage_path = 'path/to/'

        # Delete existing test bucket
        session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        self.delete_bucket(session, bucket_name)

        storage = self.s3_provisioner.provision_storage(user_name, bucket_name, storage_path, duration_sec=900)

        # Assert that new credentials were issued
        self.assertFalse(storage.aws_access_key_id == AWS_ACCESS_KEY_ID)
        self.assertFalse(storage.aws_secret_access_key == AWS_SECRET_ACCESS_KEY)

        # Federated User Id will be 123:USERNAME or
        self.assertEqual(user_name, storage.aws_federated_user_id.split(':')[1])

        # Assert that we can write within given path
        absolute_storage_path = os.path.join(storage_path, test_file_name)

        user_session = Session(storage.aws_access_key_id, storage.aws_secret_access_key, storage.aws_session_token)
        user_s3 = user_session.resource('s3')
        user_s3.Bucket(bucket_name).put_object(Key=absolute_storage_path, Body=test_file_contents)

        user_s3.Bucket(bucket_name).download_file(absolute_storage_path, tmp_download_path)

        downloaded_file_contents = open(tmp_download_path, 'rb').read()

        self.assertEqual(downloaded_file_contents, test_file_contents)
        user_s3.Object(bucket_name, absolute_storage_path).delete()
        os.remove(tmp_download_path)

        # Assert that we cannot write outside the given path

        try:
            absolute_unscoped_storage_path = os.path.join(unscoped_storage_path, test_file_name)
            user_s3.Bucket(bucket_name).put_object(Key=absolute_unscoped_storage_path, Body=test_file_contents)
            raise AssertionError('Wrote to unscoped path!')
        except ClientError as err:
            print('Got ClientError writing to unscoped path, as expected', err)

    def delete_bucket(self, session: Session, bucket_name: str):

        s3 = session.resource('s3')
        bucket = s3.Bucket(bucket_name)

        try:
            for key in bucket.objects.all():
                key.delete()

            bucket.delete()
        except ClientError as err:
            print('Unable to delete bucket:', err)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
