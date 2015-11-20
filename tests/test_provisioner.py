#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_provisioner
----------------------------------

Tests for `provisioner` module.
"""
import os
import unittest
from boto3.session import Session, botocore
from botocore.exceptions import ClientError
from storage_provisioner.provisioner import S3StorageProvisioner
from storage_provisioner.storage import S3Storage

try:
    from tests.secrets import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
except ImportError:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    if AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None:
        raise EnvironmentError("AWS Credentials not present!")


class TestS3StorageProvisioner(unittest.TestCase):
    s3_provisioner = None
    master_session = None  # Used to perform administrative AWS actions

    test_user_name = 'test_user'
    test_bucket_name = '9a5bb25e-783a-11e5-86ba-b8f6b11601af'
    test_file_name = 'test.txt'
    test_file_contents = 'hello.'.encode()
    tmp_download_file_path = '/tmp/hello.txt'

    def setUp(self):
        print('setup')
        self.s3_provisioner = S3StorageProvisioner(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        self.master_session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def tearDown(self):
        print('tearDown')
        # Ensure test bucket from previous test is deleted
        self.delete_bucket(self.master_session, self.test_bucket_name)

    def test_provision_storage_default_policy(self):
        """
        Test S3StorageProvisioner's provisioning of storage and credentials with a default user_policy.
        Assert that writing inside the specified storage_path succeeds, and writing outside this path fails.
        """
        storage_path = 'path/to/test/'

        storage = self.s3_provisioner.provision_storage(self.test_user_name,
                                                        self.test_bucket_name,
                                                        storage_path,
                                                        duration_sec=900)

        self.assert_storage_properly_initialized(storage)
        self.assert_storage_policy_valid(storage, storage_path)

    def test_provision_storage_custom_policy(self):

        storage_path = 'test/'

        # string.format requires us to escape braces ('{') by doubling ('{{')
        custom_user_policy = """{{
           "Version":"2012-10-17",
           "Statement":[
              {{
                 "Effect":"Allow",
                 "Action":[
                    "s3:PutObject",
                    "s3:PutObjectAcl",
                    "s3:PutObjectAclVersion",
                    "s3:GetObject",
                    "s3:DeleteObject"
                 ],
                 "Resource":"arn:aws:s3:::{0}/custom/{1}*"
              }},
              {{
                 "Effect":"Allow",
                 "Action":[
                    "s3:ListBucket",
                    "s3:GetBucketLocation",
                    "s3:ListAllMyBuckets"
                 ],
                 "Resource":"arn:aws:s3:::{0}/custom/{1}"
              }}
           ]
        }}
        """.format(self.test_bucket_name, storage_path)

        storage = self.s3_provisioner.provision_storage(self.test_user_name,
                                                        self.test_bucket_name,
                                                        storage_path,
                                                        user_policy=custom_user_policy,
                                                        duration_sec=900)

        # Custom policy restricts access to 'custom' subdirectory
        absolute_storage_path = os.path.join('custom', storage_path)

        self.assert_storage_properly_initialized(storage)
        self.assert_storage_policy_valid(storage, absolute_storage_path)

    def assert_storage_properly_initialized(self, storage: S3Storage):
        """
        Assert that :param storage was properly initialized with test fixture data,
        and that its functions operate as expected.

        :param storage: the Storage object under test
        """

        # Assert that new credentials were issued
        self.assertFalse(storage.aws_access_key_id == AWS_ACCESS_KEY_ID)
        self.assertFalse(storage.aws_secret_access_key == AWS_SECRET_ACCESS_KEY)

        # Federated User Id will be XXX:USERNAME
        self.assertEqual(self.test_user_name, storage.aws_federated_user_id.split(':')[1])

        test_key = 'folder/test_key.txt'
        self.assertEqual(storage.get_url_for_key(test_key),
                         "https://{}.s3.amazonaws.com/{}".format(storage.s3_bucket_name,
                                                                 test_key))

    def assert_storage_policy_valid(self,
                                    storage: S3Storage,
                                    storage_path: str):
        """
        Assert that the credentials in :param storage allow writing only within :param storage_path.

        :param storage: the Storage object providing access credentials
        :param storage_path: the path within which storage's credentials should allow write access
        """

        # Assert that we can write within storage_path
        absolute_storage_path = os.path.join(storage_path, self.test_file_name)

        user_session = Session(storage.aws_access_key_id,
                               storage.aws_secret_access_key,
                               storage.aws_session_token)

        user_s3 = user_session.resource('s3')
        user_s3.Bucket(self.test_bucket_name).put_object(Key=absolute_storage_path, Body=self.test_file_contents)

        user_s3.Bucket(self.test_bucket_name).download_file(absolute_storage_path, self.tmp_download_file_path)

        downloaded_file_contents = open(self.tmp_download_file_path, 'rb').read()

        self.assertEqual(downloaded_file_contents, self.test_file_contents)
        user_s3.Object(self.test_bucket_name, absolute_storage_path).delete()
        os.remove(self.tmp_download_file_path)

        # Assert that we cannot write to the parent directory of storage_path
        try:
            # Ensure the storage_path directory ends with a slash
            path_with_trailing_slash = os.path.join(storage_path, '')
            # The first dirname call removes the trailing slash, the subsequent traverses up a directory
            unscoped_storage_path = os.path.dirname(os.path.dirname(path_with_trailing_slash))
            absolute_unscoped_storage_path = os.path.join(unscoped_storage_path, self.test_file_name)
            user_s3.Bucket(self.test_bucket_name).put_object(Key=absolute_unscoped_storage_path,
                                                             Body=self.test_file_contents)
            raise AssertionError(
                'Wrote to path ({0}) outside storage_path ({1})!'.format(absolute_unscoped_storage_path,
                                                                         storage_path))
        except ClientError as err:
            print('Got ClientError writing outside storage_path, as expected: ', err)

    def delete_bucket(self, session: Session, bucket_name: str):

        s3 = session.resource('s3')

        bucket_exists = True
        try:
            s3.meta.client.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                bucket_exists = False

        if bucket_exists:
            bucket = s3.Bucket(bucket_name)

            try:
                for key in bucket.objects.all():
                    key.delete()

                bucket.delete()
                print('Deleted bucket {0}'.format(bucket_name))
            except ClientError as err:
                print('Unable to delete bucket:', err)

    if __name__ == '__main__':
        import sys

        sys.exit(unittest.main())
